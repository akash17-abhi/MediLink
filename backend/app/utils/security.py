"""
Security and sanitization helpers for MediLink.
"""

import re
from werkzeug.security import generate_password_hash, check_password_hash


def sanitize_string(text, max_length=255):
    """Strip dangerous characters and trim to max length."""
    if not text:
        return ""
    # Strip HTML tags and control characters
    clean = re.sub(r"<[^>]*>", "", str(text))
    return clean.strip()[:max_length]


def hash_password(password: str) -> str:
    """Hash password using Werkzeug security."""
    return generate_password_hash(password)


def verify_password(hashed: str, password: str) -> bool:
    """Verify password against Werkzeug hash."""
    return check_password_hash(hashed, password)
