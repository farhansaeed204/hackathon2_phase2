import requests
import json

BASE_URL = "http://localhost:8001"

def test_signup_and_login():
    # Test signup
    print("Testing signup...")
    signup_data = {
        "email": "test2@example.com",
        "password": "shortpass",
        "name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    print(f"Signup response: {response.status_code}")
    print(f"Signup data: {response.json()}")
    
    if response.status_code == 200:
        print("Signup successful!")
    else:
        print(f"Signup failed: {response.json()}")
        return False

    # Test login
    print("\nTesting login...")
    login_data = {
        "email": "test2@example.com",
        "password": "shortpass"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login response: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"Login successful! Token: {token_data['access_token'][:20]}...")
        
        # Test getting user profile
        print("\nTesting get user profile...")
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Get user response: {response.status_code}")
        print(f"User data: {response.json()}")
        
        if response.status_code == 200:
            print("Get user profile successful!")
            return True
        else:
            print(f"Get user profile failed: {response.json()}")
            return False
    else:
        print(f"Login failed: {response.json()}")
        return False

if __name__ == "__main__":
    success = test_signup_and_login()
    if success:
        print("\nAll tests passed! Authentication is working correctly.")
    else:
        print("\nSome tests failed. Please check the implementation.")