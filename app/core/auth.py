from fastapi import Header, HTTPException

VALID_API_KEYS = {
    "demo-key-123",
    "student-key-456"
}

def verify_api_key(authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing API key")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    api_key = authorization.split(" ")[1]

    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return api_key