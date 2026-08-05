import hashlib
import secrets


TOKEN_LENGTH = 48


def generate_token() -> str:
    """
    Generate a cryptographically secure invitation token.
    """
    return secrets.token_urlsafe(TOKEN_LENGTH)


def hash_token(token: str) -> str:
    """
    Return the SHA-256 hash of the invitation token.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()