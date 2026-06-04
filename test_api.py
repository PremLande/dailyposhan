#!/usr/bin/env python3
"""
Test API integration between frontend and backend
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"
TESTS_PASSED = 0
TESTS_FAILED = 0

def test(name, func):
    """Run a test function"""
    global TESTS_PASSED, TESTS_FAILED
    try:
        print(f"\n🧪 {name}...", end=" ")
        func()
        print("✅")
        TESTS_PASSED += 1
    except Exception as e:
        print(f"❌ {e}")
        TESTS_FAILED += 1

def test_products():
    """Test GET /api/products/"""
    res = requests.get(f"{BASE_URL}/products/", timeout=5)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert isinstance(data, list), "Expected list of products"
    assert len(data) > 0, "Expected at least one product"
    print(f"({len(data)} products found)")

def test_register():
    """Test POST /api/auth/register"""
    import time
    email = f"test{int(time.time())}@example.com"
    payload = {"email": email, "password": "pass123", "name": "Test User"}
    res = requests.post(f"{BASE_URL}/auth/register", json=payload, timeout=5)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert data["email"] == email, "Email mismatch"
    return email

def test_login():
    """Test POST /api/auth/login"""
    import time
    email = f"test{int(time.time())}@example.com"
    password = "pass123"
    
    # Register first
    requests.post(f"{BASE_URL}/auth/register", 
                 json={"email": email, "password": password, "name": "Test"}, timeout=5)
    
    # Then login
    res = requests.post(f"{BASE_URL}/auth/login",
                       json={"email": email, "password": password}, timeout=5)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert data["email"] == email, "Email mismatch"

def test_cors():
    """Test CORS headers"""
    res = requests.get(f"{BASE_URL}/products/",
                      headers={"Origin": "http://localhost:5173"},
                      timeout=5)
    cors_header = res.headers.get("access-control-allow-origin")
    assert cors_header is not None, "CORS header missing"

def main():
    print("\n" + "="*60)
    print("🧪 Daily Poshan - API Integration Tests")
    print("="*60)
    
    try:
        # Verify backend is running
        print("\n🔍 Checking backend connectivity...", end=" ")
        requests.get(f"{BASE_URL}/products/", timeout=5)
        print("✅ Backend is running")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("   Start backend with: python manage.py runserver")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    # Run tests
    test("GET /products/", test_products)
    test("POST /auth/register", test_register)
    test("POST /auth/login", test_login)
    test("CORS Headers", test_cors)
    
    # Summary
    print("\n" + "="*60)
    print(f"📊 Results: {TESTS_PASSED} passed, {TESTS_FAILED} failed")
    print("="*60 + "\n")
    
    return 0 if TESTS_FAILED == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
