"""Security utilities for JWT tokens and password hashing."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
import bcrypt

from app.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "iss": settings.app_name,
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "iss": settings.app_name,
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    if not hashed_password:
        return False
    
    # Try bcrypt directly first (since we're using bcrypt directly for hashing)
    try:
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        # Fallback to passlib for compatibility
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    # bcrypt has a maximum password length of 72 bytes
    # Convert to bytes and truncate if necessary
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes
        password_bytes = password_bytes[:72]
    
    # Use bcrypt directly to avoid passlib initialization issues
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string (bcrypt hash is always 60 bytes)
    return hashed.decode('utf-8')


def create_tokens(user_id: int, email: str) -> Dict[str, str]:
    """Create both access and refresh tokens for a user."""
    token_data = {"sub": str(user_id), "email": email}
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def create_tokens_with_expiry(user_id: int, email: str) -> Dict[str, Any]:
    """Create tokens with expiry information."""
    token_data = {"sub": str(user_id), "email": email}
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Get expiry times
    access_payload = verify_token(access_token)
    refresh_payload = verify_token(refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": int((access_payload["exp"] - datetime.utcnow().timestamp())),
        "refresh_expires_in": int((refresh_payload["exp"] - datetime.utcnow().timestamp()))
    }


def create_shop_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token for shop."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "iss": settings.app_name,
        "type": "shop_access"
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_shop_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token for shop."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "iss": settings.app_name,
        "type": "shop_refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_shop_tokens(shop_id: int, email: str) -> Dict[str, str]:
    """Create both access and refresh tokens for a shop."""
    token_data = {"sub": str(shop_id), "email": email}
    
    access_token = create_shop_access_token(token_data)
    refresh_token = create_shop_refresh_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
