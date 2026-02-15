"""
Authentication and authorization utilities.

Provides password hashing, token generation, and other auth features
for securing the web interface and API endpoints.
"""

import os
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from utils.logger import get_logger

logger = get_logger(__name__)


def generate_secret_key(length: int = 32) -> str:
    """
    Generate a cryptographically secure secret key.
    
    Args:
        length: Length of the secret key in bytes
        
    Returns:
        Hex-encoded secret key
    """
    return secrets.token_hex(length)


def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    
    Args:
        password: Plain text password
        salt: Optional salt (generated if not provided)
        
    Returns:
        Tuple of (hashed_password, salt) as hex strings
    """
    if salt is None:
        salt = os.urandom(32)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    
    # Use PBKDF2-HMAC-SHA256 with 100,000 iterations
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    
    return hashed.hex(), salt.hex()


def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        hashed_password: Hex-encoded hashed password
        salt: Hex-encoded salt
        
    Returns:
        True if password matches
    """
    try:
        new_hash, _ = hash_password(password, salt)
        return hmac.compare_digest(new_hash, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False


def create_access_token(data: Dict[str, Any], secret_key: str, 
                       expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a simple access token (for basic auth).
    
    Note: For production use, consider using JWT tokens with proper signing.
    
    Args:
        data: Data to encode in token
        secret_key: Secret key for signing
        expires_delta: Token expiration time
        
    Returns:
        Signed access token
    """
    if expires_delta is None:
        expires_delta = timedelta(hours=24)
    
    expire = datetime.utcnow() + expires_delta
    
    # Create token payload
    payload = {
        **data,
        "exp": expire.isoformat()
    }
    
    # Simple signing (for production, use JWT library)
    payload_str = str(sorted(payload.items()))
    signature = hmac.new(
        secret_key.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Encode as hex
    token = f"{payload_str}:{signature}".encode().hex()
    
    return token


def verify_access_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode an access token.
    
    Args:
        token: Access token to verify
        secret_key: Secret key for verification
        
    Returns:
        Decoded token data if valid, None otherwise
    """
    try:
        # Decode from hex
        decoded = bytes.fromhex(token).decode()
        payload_str, signature = decoded.rsplit(':', 1)
        
        # Verify signature
        expected_signature = hmac.new(
            secret_key.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            logger.warning("Token signature verification failed")
            return None
        
        # Parse payload
        payload_dict = eval(payload_str)  # Simple parsing (use JSON in production)
        payload = dict(payload_dict)
        
        # Check expiration
        exp = datetime.fromisoformat(payload.get('exp', ''))
        if datetime.utcnow() > exp:
            logger.warning("Token expired")
            return None
        
        return payload
        
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return None


def generate_api_key(prefix: str = "abk") -> str:
    """
    Generate an API key for external access.
    
    Args:
        prefix: Prefix for the API key
        
    Returns:
        Generated API key
    """
    random_part = secrets.token_urlsafe(32)
    return f"{prefix}_{random_part}"


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for storage.
    
    Args:
        api_key: API key to hash
        
    Returns:
        Hashed API key
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    """
    Verify an API key against its hash.
    
    Args:
        api_key: API key to verify
        hashed_key: Stored hashed API key
        
    Returns:
        True if API key matches
    """
    return hmac.compare_digest(hash_api_key(api_key), hashed_key)

