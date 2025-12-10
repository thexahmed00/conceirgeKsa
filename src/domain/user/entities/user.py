"""User domain entity - encapsulating user business logic."""

from datetime import datetime
from typing import Optional

import bcrypt

from src.domain.shared.exceptions import InvalidPasswordError, InvalidUserError


class User:
    """User entity - encapsulates user business rules."""

    def __init__(
        self,
        user_id: int,
        email: str,
        hashed_password: str,
        first_name: str,
        last_name: str,
        phone_number: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        """Create a new User entity.
        
        Args:
            user_id: Unique user identifier
            email: User email
            hashed_password: Bcrypt hashed password
            first_name: User's first name
            last_name: User's last name
            phone_number: Optional phone number
            created_at: Account creation timestamp
            updated_at: Last update timestamp
        """
        self.user_id = user_id
        self.email = email
        self.hashed_password = hashed_password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    # ============ Business Logic Methods ============

    def authenticate(self, password: str) -> bool:
        """Verify password against bcrypt hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            True if password is correct, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                self.hashed_password.encode("utf-8"),
            )
        except Exception as e:
            raise InvalidPasswordError(f"Password verification failed: {str(e)}")

    def __eq__(self, other: object) -> bool:
        """Users are equal if they have the same ID."""
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id

    def __hash__(self) -> int:
        """Hash based on user ID."""
        return hash(self.user_id)

    def __str__(self) -> str:
        return f"User(id={self.user_id}, email={self.email})"

    def __repr__(self) -> str:
        return self.__str__()
