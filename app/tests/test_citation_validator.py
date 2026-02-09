"""
Test citation validation with real and fake citations.
"""

from app.services.citation_validator import (
    validate_citations,
    extract_citations_by_style,
    check_hallucination_patterns,
    check_citation_age,
)

# =========================
# TEST DATA
# =========================

VALID_APA_TEXT = """
Research shows that machine learning improves efficiency (Smith & Johnson, 2023).
According to recent studies (Lee, 2024), AI adoption is growing rapidly.
"""

FAKE_CITATIONS_TEXT = """
The Fake University Press (2025) published groundbreaking research.
Anonymous (n.d.) suggested that this was important.
As stated in https://example.com/fake-study, the results were significant.
"""

MIXED_TEXT = """
Valid citation: (Anderson, 2022) shows effectiveness.
Suspicious: (Future University, 2030) discovered something.
Valid: (Brown, 2023) confirms the findings.
Fake author: (Anonymous, 2020) reported results.
"""


# =========================
# TESTS
# =========================

def test_valid_apa_citations():
    """Test extraction of valid APA citations."""
    citations = extract_citations_by_style(VALID_APA_TEXT, "APA")
    print(f"✅ Valid APA citations: {citations}")
    assert len(citations) > 0


def test_detect_fake_citations():
    """Test hallucination detection."""
    is_sus, reasons = check_hallucination_patterns(FAKE_CITATIONS_TEXT)
    print(f"✅ Hallucination detected: {is_sus}")
    print(f"   Reasons: {reasons}")
    assert is_sus


def test_future_year_detection():
    """Test detection of future citation dates."""
    is_valid, reason = check_citation_age("(Future University, 2030)")
    print(f"✅ Future year detected: {not is_valid}")
    print(f"   Reason: {reason}")
    assert not is_valid


def test_mixed_citations():
    """Test validation report on mixed citations."""
    report = validate_citations(MIXED_TEXT, "APA", allow_old_citations=False)
    print(f"✅ Mixed citations report:")
    print(f"   Total: {report.total_citations}")
    print(f"   Valid: {report.valid_citations}")
    print(f"   Suspicious: {report.suspicious_citations}")
    print(f"   Hallucination Score: {report.hallucination_score:.0%}")
    print(f"   Issues: {report.issues}")
    assert report.suspicious_citations > 0


def test_citation_age_validation():
    """Test citation age constraints."""
    # Recent citation (valid)
    is_valid, _ = check_citation_age("(Smith, 2024)", allow_old=False)
    assert is_valid

    # Old citation (invalid without allow_old)
    is_valid, _ = check_citation_age("(Smith, 2018)", allow_old=False)
    assert not is_valid

    # Old citation allowed
    is_valid, _ = check_citation_age("(Smith, 2018)", allow_old=True)
    assert is_valid

    print("✅ Citation age validation passed")


# =========================
# RUN ALL TESTS
# =========================

if __name__ == "__main__":
    print("🧪 Running Citation Validator Tests...\n")

    test_valid_apa_citations()
    print()

    test_detect_fake_citations()
    print()

    test_future_year_detection()
    print()

    test_mixed_citations()
    print()

    test_citation_age_validation()
    print()

    print("✅ All tests passed!")