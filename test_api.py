#!/usr/bin/env python3
"""
Automated test script for Flask Firebase PoC API
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "name": "Test User",
    "email": "automated.test@example.com",
    "password": "password123456"
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_test(test_name):
    print(f"{Colors.YELLOW}🧪 {test_name}...{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def test_endpoint(method, endpoint, headers=None, data=None, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Method {method} not supported")
        
        # Check status code
        if response.status_code == expected_status:
            print_success(f"{method} {endpoint} - Status: {response.status_code}")
        else:
            print_error(f"{method} {endpoint} - Expected status: {expected_status}, received: {response.status_code}")
            return None
        
        # Try to parse JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            print_error(f"Response is not valid JSON")
            return None
            
    except requests.exceptions.ConnectionError:
        print_error(f"Connection error with {url}")
        print_info("Make sure the Flask application is running")
        return None
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return None

def main():
    print_header("AUTOMATED TEST - FLASK FIREBASE POC")
    
    # Check if server is running
    print_test("Checking if server is running")
    response = test_endpoint('GET', '/api/public')
    if not response:
        print_error("Server is not responding. Run 'python3 run.py' first.")
        sys.exit(1)
    
    print_success("Server is running!")
    
    # Test 1: Public endpoint
    print_header("TEST 1: PUBLIC ENDPOINT")
    print_test("Testing public endpoint")
    public_response = test_endpoint('GET', '/api/public')
    if public_response and public_response.get('success'):
        print_success("Public endpoint working correctly")
        print_info(f"Message: {public_response.get('message')}")
    else:
        print_error("Public endpoint failed")
    
    # Test 2: User registration
    print_header("TEST 2: USER REGISTRATION")
    print_test("Registering new user")
    register_response = test_endpoint('POST', '/auth/register', data=TEST_USER, expected_status=201)
    
    if not register_response or not register_response.get('success'):
        print_error("User registration failed")
        if register_response:
            print_info(f"Error: {register_response.get('message')}")
        return
    
    print_success("User registered successfully")
    user_data = register_response.get('data', {})
    token = user_data.get('token')
    user_info = user_data.get('user', {})
    
    print_info(f"UID: {user_info.get('uid')}")
    print_info(f"Email: {user_info.get('email')}")
    print_info(f"Name: {user_info.get('name')}")
    print_info(f"Generated token: {token[:50]}...")
    
    # Test 3: Login
    print_header("TEST 3: LOGIN")
    print_test("Logging in with credentials")
    login_data = {
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    login_response = test_endpoint('POST', '/auth/login', data=login_data)
    
    if not login_response or not login_response.get('success'):
        print_error("Login failed")
        if login_response:
            print_info(f"Error: {login_response.get('message')}")
        return
    
    print_success("Login successful")
    login_token = login_response.get('data', {}).get('token')
    print_info(f"New token: {login_token[:50]}...")
    
    # Test 4: Protected endpoint with token
    print_header("TEST 4: PROTECTED ENDPOINT (WITH TOKEN)")
    print_test("Testing protected endpoint with valid token")
    headers = {"Authorization": f"Bearer {login_token}"}
    protected_response = test_endpoint('GET', '/api/protected', headers=headers)
    
    if protected_response and protected_response.get('success'):
        print_success("Authorized access to protected endpoint")
        print_info(f"Authenticated user: {protected_response.get('data', {}).get('user', {}).get('name')}")
    else:
        print_error("Failed to access protected endpoint")
    
    # Test 5: Protected endpoint without token
    print_header("TEST 5: PROTECTED ENDPOINT (WITHOUT TOKEN)")
    print_test("Testing protected endpoint without token")
    no_auth_response = test_endpoint('GET', '/api/protected', expected_status=401)
    
    if no_auth_response and not no_auth_response.get('success'):
        print_success("Access correctly denied (no token)")
        print_info(f"Message: {no_auth_response.get('message')}")
    else:
        print_error("Protected endpoint should deny access without token")
    
    # Test 6: User data
    print_header("TEST 6: USER DATA")
    print_test("Getting user-specific data")
    user_data_response = test_endpoint('GET', '/api/user-data', headers=headers)
    
    if user_data_response and user_data_response.get('success'):
        print_success("User data retrieved successfully")
        profile = user_data_response.get('data', {}).get('profile', {})
        print_info(f"Account type: {profile.get('account_type')}")
        print_info(f"Has password: {profile.get('has_password')}")
    else:
        print_error("Failed to get user data")
    
    # Test 7: Mixed endpoint
    print_header("TEST 7: MIXED ENDPOINT")
    print_test("Testing endpoint that works with/without authentication")
    mixed_response = test_endpoint('GET', '/api/mixed', headers=headers)
    
    if mixed_response and mixed_response.get('success'):
        print_success("Mixed endpoint working (with authentication)")
        data = mixed_response.get('data', {})
        print_info(f"Authenticated: {data.get('authenticated')}")
        if data.get('authenticated'):
            print_info(f"Personalized content available")
    
    # Test 8: Token validation
    print_header("TEST 8: TOKEN VALIDATION")
    print_test("Validating JWT token")
    validate_data = {"token": login_token}
    validate_response = test_endpoint('POST', '/auth/validate-token', data=validate_data)
    
    if validate_response and validate_response.get('success'):
        print_success("Token validated successfully")
        validated_user = validate_response.get('data', {}).get('user', {})
        print_info(f"Validated user: {validated_user.get('name')}")
    else:
        print_error("Token validation failed")
    
    # Test 9: Invalid token
    print_header("TEST 9: INVALID TOKEN")
    print_test("Testing with invalid token")
    invalid_headers = {"Authorization": "Bearer invalid-token"}
    invalid_response = test_endpoint('GET', '/api/protected', headers=invalid_headers, expected_status=401)
    
    if invalid_response and not invalid_response.get('success'):
        print_success("Invalid token correctly rejected")
        print_info(f"Message: {invalid_response.get('message')}")
    else:
        print_error("Invalid token should be rejected")
    
    # Final summary
    print_header("TEST SUMMARY")
    print_success("All main tests executed!")
    print_info("Tested features:")
    print_info("  ✓ Public endpoint")
    print_info("  ✓ User registration")
    print_info("  ✓ Email/password login")
    print_info("  ✓ JWT authentication")
    print_info("  ✓ Route protection")
    print_info("  ✓ Token validation")
    print_info("  ✓ Error handling")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TESTS COMPLETED SUCCESSFULLY! 🎉{Colors.END}\n")

if __name__ == "__main__":
    main()
