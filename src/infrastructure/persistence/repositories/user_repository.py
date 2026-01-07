"""UserRepository implementation - PostgreSQL persistence."""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.domain.user.entities.user import User
from src.domain.shared.exceptions import DuplicateResourceError
from src.infrastructure.persistence.models.user import UserModel


class PostgreSQLUserRepository:
    """SQLAlchemy-based UserRepository for PostgreSQL."""

    def __init__(self, db_session: Session):
        """Initialize repository with database session."""
        self._session = db_session

    def save(self, user: User) -> User:
        """Save a new user to database.
        
        Args:
            user: Domain User entity to persist
            
        Returns:
            Saved user with persistence ID
            
        Raises:
            DuplicateResourceError: If email already exists
        """
        try:
            # Create ORM model (skip ID for autoincrement)
            model = UserModel(
                email=user.email,
                hashed_password=user.hashed_password,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=f"{user.first_name} {user.last_name}",
                phone_number=user.phone_number,
                tier=5000,
                is_active=True,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            self._session.add(model)
            self._session.flush()  # Get ID from autoincrement
            # Update domain entity with generated ID
            user.user_id = model.id
            self._session.commit()
            return user
        except IntegrityError as e:
            self._session.rollback()
            if "users_email_key" in str(e) or "duplicate" in str(e).lower():
                raise DuplicateResourceError(f"User with email {user.email} already exists")
            raise

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID.
        
        Args:
            user_id: User ID to find
            
        Returns:
            User domain entity or None if not found
        """
        model = self._session.query(UserModel).filter(
            UserModel.id == user_id
        ).first()

        return self._to_entity(model) if model else None

    def find_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email.
        
        Args:
            email: Email string
            
        Returns:
            User domain entity or None if not found
        """
        model = self._session.query(UserModel).filter(
            UserModel.email == email
        ).first()

        return self._to_entity(model) if model else None

    def _to_entity(self, model: UserModel) -> User:
        """Convert SQLAlchemy UserModel to domain User entity."""
        user = User(
            user_id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            first_name=model.first_name,
            last_name=model.last_name,
            phone_number=model.phone_number,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        user.tier = model.tier
        user.is_active = model.is_active
        user.is_admin = getattr(model, 'is_admin', False)
        return user

    def update(self, user: User) -> User:
        """Update an existing user.
        
        Args:
            user: Domain User entity with updated fields
            
        Returns:
            Updated user entity
        """
        model = self._session.query(UserModel).filter(
            UserModel.id == user.user_id
        ).first()
        
        if model:
            model.first_name = user.first_name
            model.last_name = user.last_name
            model.full_name = f"{user.first_name} {user.last_name}"
            model.phone_number = user.phone_number
            model.hashed_password = user.hashed_password  # Allow password updates
            self._session.commit()
            self._session.refresh(model)
            return self._to_entity(model)
        
        return user

    def delete(self, user_id: int) -> bool:
        """Delete a user by ID.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        model = self._session.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        
        return False

    def find_all_admins(self):
        """Find all admin users.
        
        Returns:
            List of admin User entities
        """
        models = self._session.query(UserModel).filter(
            UserModel.is_admin == True
        ).all()
        
        return [self._to_entity(m) for m in models]
