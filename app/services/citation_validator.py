import re
from enum import Enum
from typing import List, Tuple, Optional
from pydantic import BaseModel


# =========================
# MODELS & ENUMS
# =========================

class CitationStyle(str, Enum):
    APA = "APA"
    HARVARD = "Harvard"
    MLA = "MLA"
    CHICAGO = "Chicago"
    VANCOUVER = "Vancouver"


class Citation(BaseModel):
    """Represents a single extracted citation."""
    text: str
    style: str
    is_suspicious: bool
    confidence: float  # 0.0-1.0
    reason: Optional[str] = None


class ValidationReport(BaseModel):
    """Report on all citations in a text."""
    total_citations: int
    valid_citations: int
    suspicious_citations: int
    hallucination_score: float  # 0.0-1.0 (higher = more suspicious)
    issues: List[str]
    recommendations: List[str]


# =========================
# HALLUCINATION PATTERNS
# =========================

HALLUCINATION_PATTERNS = {
    # Fake publisher patterns
    "fake_publisher": re.compile(
        r"\b(Fake|Mock|Test|Sample|Example|Placeholder|TBD)\s+(University|Press|Journal|Publications?)\b",
        re.IGNORECASE
    ),

    # Suspicious author names
    "placeholder_author": re.compile(
        r"\b(et al\.|Anonymous|Unknown|Author|Researcher|Scholar)\b(?:\s*\(?\d{4}\))?",
        re.IGNORECASE
    ),

    # Incomplete citations
    "incomplete_citation": re.compile(
        r"\([A-Z][a-z]+\s+\d{1,2},?\s*n\.d\.\)",  # (Smith, n.d.)
        re.IGNORECASE
    ),

    # Fake URLs
    "fake_url": re.compile(
        r"https?://(example|test|fake|placeholder|sample|mock)\.(com|org|net|edu)",
        re.IGNORECASE
    ),

    # Year anomalies (future dates, way too old without context)
    "future_year": re.compile(r"\b(20[3-9]\d|21\d{2})\b"),  # Future dates
    "ancient_year": re.compile(r"\b(1[0-8]\d{2})\b"),  # Pre-1900

    # Repeated citations (lazy hallucination)
    "repeated_exact": None,  # Checked separately
}


# =========================
# CITATION EXTRACTORS BY STYLE
# =========================

def extract_apa_citations(text: str) -> List[str]:
    """
    Extract APA-style citations.
    Pattern: (Author Year) or Author (Year)
    """
    pattern = r"\(([A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)*),?\s+(\d{4}|n\.d\.)\)|([A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)*)\s+\((\d{4}|n\.d\.)\)"
    matches = re.findall(pattern, text)
    return [f"({m[0]}, {m[1]})" if m[0] else f"{m[2]} ({m[3]})" for m in matches]


def extract_harvard_citations(text: str) -> List[str]:
    """
    Extract Harvard-style citations.
    Pattern: Author Year or (Author, Year)
    """
    pattern = r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(\d{4}|n\.d\.)|(\(([A-Z][a-z]+),?\s+(\d{4}|n\.d\.)\))"
    matches = re.findall(pattern, text)
    return [m[0] + " " + m[1] if m[0] else m[3] for m in matches]


def extract_mla_citations(text: str) -> List[str]:
    """
    Extract MLA-style citations.
    Pattern: (Author Page) or (Author)
    """
    pattern = r"\(([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(\d+|\d+\-\d+)?\)"
    matches = re.findall(pattern, text)
    return [m[0] for m in matches]


def extract_citations_by_style(text: str, style: str) -> List[str]:
    """Route to appropriate extractor."""
    extractors = {
        "APA": extract_apa_citations,
        "Harvard": extract_harvard_citations,
        "MLA": extract_mla_citations,
        "Chicago": lambda t: extract_apa_citations(t),  # Similar to APA for now
        "Vancouver": lambda t: re.findall(r"\[(\d+)\]", t),  # [1], [2], etc.  # [1], [2], etc.
    }
    return extractors.get(style, extract_apa_citations)(text)


# =========================
# HALLUCINATION DETECTION
# =========================

def check_hallucination_patterns(text: str) -> Tuple[bool, List[str]]:
    """
    Check if text contains known hallucination patterns.
    Returns: (is_suspicious, reasons)
    """
    reasons = []

    # Check each pattern
    for pattern_name, pattern in HALLUCINATION_PATTERNS.items():
        if pattern_name == "repeated_exact":
            continue  # Handle separately

        if pattern and pattern.search(text):
            reasons.append(f"Detected {pattern_name.replace('_', ' ')}")

    # Check for repeated citations
    citations = extract_apa_citations(text)
    if len(citations) > len(set(citations)):
        reasons.append("Repeated citations (possible hallucination)")

    return len(reasons) > 0, reasons


def check_citation_age(citation_text: str, allow_old: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Check if citation year is within acceptable range.
    Returns: (is_valid, reason)
    """
    year_match = re.search(r"\b(\d{4})\b", citation_text)
    if not year_match:
        return True, None

    year = int(year_match.group(1))
    current_year = 2026

    # Future dates = hallucination
    if year > current_year:
        return False, f"Citation year {year} is in the future (hallucination indicator)"

    # Old dates (before 1900) without context = suspicious
    if year < 1900:
        return False, f"Citation year {year} is pre-1900 (verify accuracy)"

    # Default: last 5 years only
    if not allow_old and (current_year - year) > 5:
        return False, f"Citation from {year} is older than 5 years (override with allow_old_citations=True)"

    return True, None


def validate_citation_format(citation: str, style: str) -> Tuple[bool, Optional[str]]:
    """
    Validate citation format matches style rules.
    Returns: (is_valid, reason)
    """
    style_rules = {
        "APA": r"^\([A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)*,\s+\d{4}\)$|^[A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)*\s+\(\d{4}\)$",
        "Harvard": r"^[A-Z][a-z]+,\s+\d{4}$",
        "MLA": r"^\([A-Z][a-z]+(?:\s+\d+)?\)$",
        "Chicago": r"^\d+\.",
        "Vancouver": r"^\[\d+\]$",
    }

    pattern = style_rules.get(style)
    if not pattern:
        return True, None

    if re.match(pattern, citation.strip()):
        return True, None
    else:
        return False, f"Citation does not match {style} format"


# =========================
# MAIN VALIDATOR
# =========================

def validate_citations(
    text: str,
    style: str,
    allow_old_citations: bool = False
) -> ValidationReport:
    """
    Complete citation validation pipeline.
    """
    issues = []
    recommendations = []

    # Extract citations
    citations_list = extract_citations_by_style(text, style)
    total_citations = len(citations_list)

    valid_count = 0
    suspicious_count = 0
    suspicious_details = []

    # Check each citation
    for citation_text in citations_list:
        # 1. Check for hallucination patterns
        is_sus_pattern, pattern_reasons = check_hallucination_patterns(citation_text)

        # 2. Check citation age
        age_valid, age_reason = check_citation_age(citation_text, allow_old_citations)

        # 3. Check format
        format_valid, format_reason = validate_citation_format(citation_text, style)

        # Tally results
        if is_sus_pattern or not age_valid or not format_valid:
            suspicious_count += 1
            reasons = []
            if pattern_reasons:
                reasons.extend(pattern_reasons)
            if age_reason:
                reasons.append(age_reason)
            if format_reason:
                reasons.append(format_reason)
            suspicious_details.append({
                "citation": citation_text,
                "reasons": reasons
            })
        else:
            valid_count += 1

    # Calculate hallucination score (0.0 - 1.0)
    hallucination_score = (
        (suspicious_count / total_citations) if total_citations > 0 else 0.0
    )

    # Build issues report
    if suspicious_count > 0:
        issues.append(f"{suspicious_count}/{total_citations} citations flagged as suspicious")
        for detail in suspicious_details:
            issues.append(f"  → {detail['citation']}: {', '.join(detail['reasons'])}")

    if hallucination_score > 0.3:
        issues.append("⚠️ HIGH HALLUCINATION RISK: >30% of citations are suspicious")
        recommendations.append("Review all flagged citations manually")
        recommendations.append("Consider asking Gemini to regenerate with stricter citation rules")

    if hallucination_score > 0.5:
        issues.append("🚨 CRITICAL: >50% hallucination score. Do NOT publish without verification.")
        recommendations.append("Request regeneration with allow_old_citations=False")

    if total_citations == 0:
        recommendations.append("No citations detected. For academic writing, this may be insufficient.")

    return ValidationReport(
        total_citations=total_citations,
        valid_citations=valid_count,
        suspicious_citations=suspicious_count,
        hallucination_score=hallucination_score,
        issues=issues,
        recommendations=recommendations,
    )


def filter_safe_citations(text: str, style: str, allow_old: bool = False) -> str:
    """
    Remove or flag suspicious citations in generated text.
    Used as a safety layer before returning to user.
    """
    report = validate_citations(text, style, allow_old)

    if report.hallucination_score > 0.3:
        # Flag the text with a warning
        issues_text = "\n".join(f"  • {issue}" for issue in report.issues)
        recommendations_text = "\n".join(f"  • {rec}" for rec in report.recommendations)

        warning = (
            f"\n\n⚠️ CITATION QUALITY WARNING ⚠️\n"
            f"Hallucination Score: {report.hallucination_score:.1%}\n"
            f"Valid Citations: {report.valid_citations}/{report.total_citations}\n"
            f"Issues:\n{issues_text}\n"
            f"Recommendations:\n{recommendations_text}"
        )
        return text + warning

    return text