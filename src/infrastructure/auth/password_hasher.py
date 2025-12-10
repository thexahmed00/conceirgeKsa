"""Password hashing service - utility for use cases."""

import bcrypt

from src.domain.shared.exceptions import InvalidPasswordError


class PasswordHasher:
    """Service for hashing and verifying passwords with bcrypt."""
    
    ROUNDS = 12  # Bcrypt rounds for password hashing
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password using bcrypt.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            Bcrypt hashed password
            
        Raises:
            InvalidPasswordError: If hashing fails
        """
        try:
            if not password or len(password) < 8:
                raise InvalidPasswordError("Password must be at least 8 characters")
            
            salt = bcrypt.gensalt(rounds=PasswordHasher.ROUNDS)
            hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
            return hashed.decode("utf-8")
        except Exception as e:
            raise InvalidPasswordError(f"Password hashing failed: {str(e)}")
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify plain text password against hash.
        
        Args:
            password: Plain text password to verify
            hashed: Bcrypt hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                hashed.encode("utf-8"),
            )
        except Exception:
            return False
