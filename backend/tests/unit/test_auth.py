import pytest
from fastapi import HTTPException
from jose import jwt
from src.services.auth import verify_token, TokenData
from src.core.config import settings

def test_verify_token_valid():
    """Test that a valid token can be verified and user_id extracted"""
    # Create a test token
    test_user_id = "test_user_123"
    token_data = {"userId": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Verify the token
    result = verify_token(token)
    
    # Assert the result
    assert isinstance(result, TokenData)
    assert result.user_id == test_user_id

def test_verify_token_with_sub_field():
    """Test that a token with 'sub' field instead of 'userId' works"""
    # Create a test token using 'sub' field
    test_user_id = "test_user_456"
    token_data = {"sub": test_user_id}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Verify the token
    result = verify_token(token)
    
    # Assert the result
    assert isinstance(result, TokenData)
    assert result.user_id == test_user_id

def test_verify_token_invalid():
    """Test that an invalid token raises HTTPException"""
    # Create an invalid token
    invalid_token = "invalid.token.here"
    
    # Verify the token and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        verify_token(invalid_token)
    
    # Assert the exception details
    assert exc_info.value.status_code == 401

def test_verify_token_missing_user_id():
    """Test that a token without user_id raises HTTPException"""
    # Create a token without userId or sub
    token_data = {"some_other_claim": "value"}
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Verify the token and expect an exception
    with pytest.raises(HTTPException) as exc_info:
        verify_token(token)
    
    # Assert the exception details
    assert exc_info.value.status_code == 401