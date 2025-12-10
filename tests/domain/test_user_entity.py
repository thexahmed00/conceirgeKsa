"""Unit tests for User aggregate root."""

import pytest
from datetime import datetime

from src.domain.user.entities.user import User
from src.domain.shared.value_objects import UserId, Email, FullName, UserTier, HashedPassword
from src.domain.shared.exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUserError,
    InvalidUserTierError,
)
from src.infrastructure.auth.password_hasher import PasswordHasher


class TestUserCreation:
    """Test User aggregate creation and invariant validation."""
    
    def test_create_valid_user(self):
        """Test creating a valid user."""
        user_id = UserId(1)
        email = Email("john@example.com")
        password_hash = PasswordHasher.hash_password("SecurePassword123")
        hashed_password = HashedPassword(password_hash)
        full_name = FullName("John", "Doe")
        tier = UserTier(5000)
        
        user = User(
            user_id=user_id,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            tier=tier,
            phone_number="+966501234567",
        )
        
        assert user.user_id == user_id
        assert user.email == email
        assert user.full_name == full_name
        assert user.tier == tier
        assert user.is_active is True
    
    def test_invalid_email_format(self):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("not-an-email")
    
    def test_invalid_user_tier(self):
        """Test that invalid tier raises ValueError."""
        with pytest.raises(ValueError, match="Invalid tier"):
            UserTier(10000)
    
    def test_invalid_user_id(self):
        """Test that negative user ID raises ValueError."""
        with pytest.raises(ValueError):
            UserId(-1)


class TestUserAuthentication:
    """Test User authentication business logic."""
    
    def test_authenticate_with_correct_password(self):
        """Test authentication with correct password."""
        password = "SecurePassword123"
        hashed = PasswordHasher.hash_password(password)
        
        user = User(
            user_id=UserId(1),
            email=Email("john@example.com"),
            hashed_password=HashedPassword(hashed),
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
        )
        
        assert user.authenticate(password) is True
    
    def test_authenticate_with_wrong_password(self):
        """Test authentication with wrong password."""
        password = "SecurePassword123"
        hashed = PasswordHasher.hash_password(password)
        
        user = User(
            user_id=UserId(1),
            email=Email("john@example.com"),
            hashed_password=HashedPassword(hashed),
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
        )
        
        assert user.authenticate("WrongPassword") is False
    
    def test_cannot_authenticate_inactive_user(self):
        """Test that inactive user cannot authenticate."""
        password = "SecurePassword123"
        hashed = PasswordHasher.hash_password(password)
        
        user = User(
            user_id=UserId(1),
            email=Email("john@example.com"),
            hashed_password=HashedPassword(hashed),
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
            is_active=False,
        )
        
        with pytest.raises(InvalidUserError):
            user.authenticate(password)


class TestUserAccountManagement:
    """Test User account activation/deactivation."""
    
    def setup_method(self):
        """Setup a test user."""
        password_hash = PasswordHasher.hash_password("SecurePassword123")
        self.user = User(
            user_id=UserId(1),
            email=Email("john@example.com"),
            hashed_password=HashedPassword(password_hash),
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
        )
    
    def test_deactivate_active_user(self):
        """Test deactivating an active user."""
        assert self.user.is_active is True
        self.user.deactivate()
        assert self.user.is_active is False
    
    def test_cannot_deactivate_already_inactive_user(self):
        """Test that deactivating inactive user raises error."""
        self.user.deactivate()
        with pytest.raises(InvalidUserError):
            self.user.deactivate()
    
    def test_activate_inactive_user(self):
        """Test activating an inactive user."""
        self.user.deactivate()
        assert self.user.is_active is False
        self.user.activate()
        assert self.user.is_active is True
    
    def test_cannot_activate_already_active_user(self):
        """Test that activating active user raises error."""
        with pytest.raises(InvalidUserError):
            self.user.activate()


class TestUserUpdates:
    """Test User profile updates."""
    
    def setup_method(self):
        """Setup a test user."""
        password_hash = PasswordHasher.hash_password("SecurePassword123")
        self.user = User(
            user_id=UserId(1),
            email=Email("john@example.com"),
            hashed_password=HashedPassword(password_hash),
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
        )
    
    def test_update_phone_number(self):
        """Test updating phone number."""
        original_updated_at = self.user.updated_at
        self.user.update_phone_number("+966501234567")
        
        assert self.user.phone_number == "+966501234567"
        assert self.user.updated_at > original_updated_at
    
    def test_update_tier(self):
        """Test updating user tier."""
        original_tier = self.user.tier
        new_tier = UserTier(25000)
        
        self.user.update_tier(new_tier)
        
        assert self.user.tier == new_tier
        assert self.user.tier != original_tier


class TestUserComparison:
    """Test User comparison and hashing."""
    
    def test_users_equal_by_id(self):
        """Test that users with same ID are equal."""
        password_hash = PasswordHasher.hash_password("SecurePassword123")
        hashed = HashedPassword(password_hash)
        
        user1 = User(
            user_id=UserId(1),
            email=Email("john@example.com"),
            hashed_password=hashed,
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
        )
        
        user2 = User(
            user_id=UserId(1),
            email=Email("different@example.com"),
            hashed_password=hashed,
            full_name=FullName("Jane", "Smith"),
            tier=UserTier(25000),
        )
        
        assert user1 == user2
    
    def test_users_not_equal_different_id(self):
        """Test that users with different IDs are not equal."""
        password_hash = PasswordHasher.hash_password("SecurePassword123")
        hashed = HashedPassword(password_hash)
        
        user1 = User(
            user_id=UserId(1),
            email=Email("john@example.com"),
            hashed_password=hashed,
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
        )
        
        user2 = User(
            user_id=UserId(2),
            email=Email("john@example.com"),
            hashed_password=hashed,
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
        )
        
        assert user1 != user2
    
    def test_user_hashable(self):
        """Test that users can be used in sets and dicts."""
        password_hash = PasswordHasher.hash_password("SecurePassword123")
        hashed = HashedPassword(password_hash)
        
        user = User(
            user_id=UserId(1),
            email=Email("john@example.com"),
            hashed_password=hashed,
            full_name=FullName("John", "Doe"),
            tier=UserTier(5000),
        )
        
        user_set = {user}
        user_dict = {user: "active"}
        
        assert user in user_set
        assert user_dict[user] == "active"
