import pytest
from datetime import datetime, timedelta
from pyserver.storage.user.user_storage import UserStorage
from pyserver.storage.user.user import User
from pyserver.system.redis import RedisManager, map_get, map_delete, map_insert

@pytest.fixture
def test_user():
    return User(
        id="test_user_123",
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

@pytest.fixture
def user_storage():
    # Create a new storage instance for each test
    return UserStorage()

@pytest.fixture
def clean_redis():
    """Fixture to clean up Redis after each test."""
    yield
    # Clean up Redis after each test
    with RedisManager().get_connection() as conn:
        # Delete all test keys
        keys = [
            "urlife:users:test_user_123",
            "urlife:users:email:test@example.com",
            "urlife:users:test_user"
        ]
        for key in keys:
            map_delete(conn, key, "data")
            map_delete(conn, key, "user_id")

def test_create_user(user_storage, test_user, clean_redis):
    """Test creating a new user."""
    result = user_storage.create_user(test_user)
    assert result.id == test_user.id
    assert result.email == test_user.email
    assert result.name == test_user.name
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)
    
    # Verify user exists in Redis
    with RedisManager().get_connection() as conn:
        user_data = map_get(conn, user_storage._get_user_key(test_user.id), "data")
        assert user_data is not None
        
        email_data = map_get(conn, user_storage._get_email_key(test_user.email), "user_id")
        assert email_data == test_user.id

def test_get_user(user_storage, test_user, clean_redis):
    """Test getting a user by email."""
    # Create user first
    user_storage.create_user(test_user)
    
    # Get user by email
    result = user_storage.get_user(test_user.email)
    assert result is not None
    assert result.id == test_user.id
    assert result.email == test_user.email
    assert result.name == test_user.name
    
    # Test non-existent user
    non_existent = user_storage.get_user("nonexistent@example.com")
    assert non_existent is None

def test_update_user(user_storage, test_user, clean_redis):
    """Test updating a user's information."""
    # Create user first
    user_storage.create_user(test_user)
    
    # Update user
    updates = {
        "name": "Updated Name",
        "email": "updated@example.com"
    }
    result = user_storage.update_user(test_user.id, updates)
    
    assert result is not None
    assert result.name == "Updated Name"
    assert result.email == "updated@example.com"
    assert result.updated_at > test_user.updated_at  # Should be updated
    
    # Verify in Redis
    with RedisManager().get_connection() as conn:
        user_data = map_get(conn, user_storage._get_user_key(test_user.id), "data")
        assert user_data is not None
        
        # Check email index was updated
        old_email_data = map_get(conn, user_storage._get_email_key(test_user.email), "user_id")
        assert old_email_data is None
        
        new_email_data = map_get(conn, user_storage._get_email_key("updated@example.com"), "user_id")
        assert new_email_data == test_user.id

def test_delete_user(user_storage, test_user, clean_redis):
    """Test deleting a user."""
    # Create user first
    user_storage.create_user(test_user)
    
    # Delete user
    user_storage.delete_user(test_user.id)
    
    # Verify user is gone
    with RedisManager().get_connection() as conn:
        user_data = map_get(conn, user_storage._get_user_key(test_user.id), "data")
        assert user_data is None
        
        email_data = map_get(conn, user_storage._get_email_key(test_user.email), "user_id")
        assert email_data is None

def test_create_user_with_existing_email(user_storage, test_user, clean_redis):
    """Test creating a user with an existing email."""
    # Create user first
    user_storage.create_user(test_user)
    
    # Try to create another user with same email
    duplicate_user = User(
        id="different_id",
        email=test_user.email,
        password_hash="different_hash",
        name="Different User",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )  
    # This should succeed because we're not enforcing email uniqueness
    # in the storage layer (that's handled by the API layer)
    result = user_storage.create_user(duplicate_user)
    assert result.id == duplicate_user.id
    assert result.email == duplicate_user.email
    
    # Verify both users exist in Redis
    with RedisManager().get_connection() as conn:
        # Both users should exist
        user1_data = map_get(conn, user_storage._get_user_key(test_user.id), "data")
        assert user1_data is not None
        
        user2_data = map_get(conn, user_storage._get_user_key(duplicate_user.id), "data")
        assert user2_data is not None
        
        # Email index should point to the last created user
        email_data = map_get(conn, user_storage._get_email_key(test_user.email), "user_id")
        assert email_data == duplicate_user.id

def test_update_nonexistent_user(user_storage, clean_redis):
    """Test updating a non-existent user."""
    result = user_storage.update_user("nonexistent_id", {"name": "New Name"})
    assert result is None

def test_get_nonexistent_user(user_storage, clean_redis):
    """Test getting a non-existent user."""
    result = user_storage.get_user("nonexistent@example.com")
    assert result is None
