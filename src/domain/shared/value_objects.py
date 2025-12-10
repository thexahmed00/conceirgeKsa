"""Shared Value Objects across the domain."""

from typing import Optional
import re
from datetime import datetime


class ValueObject:
    """Base class for all value objects - immutable and compared by value."""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))


class UserId(ValueObject):
    """User ID value object - immutable and validated."""

    def __init__(self, value: int):
        if value <= 0:
            raise ValueError("UserId must be a positive integer")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"UserId({self._value})"


class Email(ValueObject):
    """Email value object - immutable and validated."""

    # RFC 5322 simplified regex for email validation
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def __init__(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Email must be a non-empty string")
        
        value = value.strip().lower()
        
        if not re.match(self.EMAIL_REGEX, value):
            raise ValueError(f"Invalid email format: {value}")
        
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"Email({self._value})"


class FullName(ValueObject):
    """Full name value object - immutable and validated."""

    def __init__(self, first_name: str, last_name: str):
        if not first_name or not isinstance(first_name, str):
            raise ValueError("First name must be a non-empty string")
        if not last_name or not isinstance(last_name, str):
            raise ValueError("Last name must be a non-empty string")
        
        self._first_name = first_name.strip()
        self._last_name = last_name.strip()

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self) -> str:
        return f"FullName({self._first_name}, {self._last_name})"


class UserTier(ValueObject):
    """User tier value object - immutable and validated."""

    VALID_TIERS = {5000, 25000, 100000}

    def __init__(self, value: int):
        if value not in self.VALID_TIERS:
            raise ValueError(f"Invalid tier: {value}. Must be one of {self.VALID_TIERS}")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"UserTier({self._value})"


class HashedPassword(ValueObject):
    """Hashed password value object - immutable."""

    def __init__(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Hashed password must be a non-empty string")
        if len(value) < 20:
            raise ValueError("Invalid hashed password format")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return "HashedPassword(***)"
