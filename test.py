import requests

BASE_URL = "http://127.0.0.1:8000"

def test_signup():
    print("Testing Signup...")
    response = requests.post(f"{BASE_URL}/signup", data={"username": "test_user_py", "password": "password123"})
    print(f"Status: {response.status_code}, Response: {response.json()}")

def test_login_success():
    print("\nTesting Login (Success)...")
    response = requests.post(f"{BASE_URL}/login", data={"username": "test_user_py", "password": "password123"})
    print(f"Status: {response.status_code}, Response: {response.json()}")

def test_login_fail():
    print("\nTesting Login (Fail)...")
    response = requests.post(f"{BASE_URL}/login", data={"username": "test_user_py", "password": "wrongpassword"})
    print(f"Status: {response.status_code}, Response: {response.json()}")

if __name__ == "__main__":
    try:
        test_signup()
        test_login_success()
        test_login_fail()
    except Exception as e:
        print(f"Test failed: {e}")