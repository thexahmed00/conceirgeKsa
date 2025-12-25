"""Domain exceptions - used across all domain entities."""


class DomainException(Exception):
    """Base exception for all domain-level errors."""
    pass


class InvalidEmailError(DomainException):
    """Raised when email is invalid."""
    pass


class InvalidPasswordError(DomainException):
    """Raised when password is invalid or authentication fails."""
    pass


class InvalidUserError(DomainException):
    """Raised when user state is invalid."""
    pass


class UserNotFoundError(DomainException):
    """Raised when user is not found."""
    pass


class UserAlreadyExistsError(DomainException):
    """Raised when trying to create a user that already exists."""
    pass


class InvalidUserTierError(DomainException):
    """Raised when user tier is invalid."""
    pass


class ResourceNotFoundError(DomainException):
    """Raised when a requested resource is not found."""
    pass


class DuplicateResourceError(DomainException):
    """Raised when trying to create a resource that already exists."""
    pass


class AccessDeniedError(DomainException):
    """Raised when a user is not allowed to access a resource."""
    pass


class ValidationError(DomainException):
    """Raised when validation fails."""
    pass
