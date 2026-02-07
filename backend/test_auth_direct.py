from src.api.auth import signup
from src.api.auth import UserCreateRequest

# Test the signup function directly
async def test_signup():
    # Use a shorter password to avoid bcrypt limitations
    user_data = UserCreateRequest(email="test@example.com", password="shortpass", name="Test User")
    try:
        result = await signup(user_data)
        print("Signup successful:", result)
    except Exception as e:
        print("Signup failed with error:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_signup())