#!/usr/bin/env python3
"""Test script for Equipment Lending Platform API endpoints"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api"
token = None

def print_response(name, response):
    """Print formatted response"""
    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_health():
    """Test health endpoint"""
    print("\n[TEST 1] Health Check")
    response = requests.get("http://localhost:5000/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n[TEST 2] User Registration")
    data = {
        "email": "testuser@example.com",
        "password": "test123",
        "name": "Test User",
        "role": "student"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print_response("User Registration", response)
    return response.status_code in [201, 400]  # 400 if user already exists

def test_login():
    """Test user login"""
    global token
    print("\n[TEST 3] User Login")
    data = {
        "email": "testuser@example.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print_response("User Login", response)
    
    if response.status_code == 200:
        token = response.json().get("token")
        print(f"\n✓ Token received: {token[:30]}...")
        return True
    return False

def test_get_equipment():
    """Test get equipment list"""
    global token
    print("\n[TEST 4] Get Equipment List")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/equipment", headers=headers)
    print_response("Get Equipment", response)
    if response.status_code == 200:
        equipment = response.json()
        print(f"\n✓ Found {len(equipment)} equipment items")
        return True
    return False

def test_get_categories():
    """Test get categories"""
    global token
    print("\n[TEST 5] Get Categories")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/equipment/categories", headers=headers)
    print_response("Get Categories", response)
    return response.status_code == 200

def test_create_equipment():
    """Test create equipment (admin only)"""
    global token
    print("\n[TEST 6] Create Equipment")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Test Microscope",
        "category": "Lab Equipment",
        "condition": "excellent",
        "quantity": 5,
        "description": "Test equipment created via API"
    }
    response = requests.post(f"{BASE_URL}/equipment", headers=headers, json=data)
    print_response("Create Equipment", response)
    return response.status_code in [201, 403]  # 403 if not admin

def test_create_request():
    """Test create borrowing request"""
    global token
    print("\n[TEST 7] Create Borrowing Request")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "equipment_id": 1,
        "start_date": "2024-12-01",
        "end_date": "2024-12-05"
    }
    response = requests.post(f"{BASE_URL}/requests", headers=headers, json=data)
    print_response("Create Request", response)
    return response.status_code in [201, 400]  # 400 if overlap or invalid

def test_get_requests():
    """Test get requests"""
    global token
    print("\n[TEST 8] Get Requests")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/requests", headers=headers)
    print_response("Get Requests", response)
    if response.status_code == 200:
        requests_list = response.json()
        print(f"\n✓ Found {len(requests_list)} requests")
        return True
    return False

def test_get_me():
    """Test get current user"""
    global token
    print("\n[TEST 9] Get Current User")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response("Get Current User", response)
    return response.status_code == 200

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("EQUIPMENT LENDING PLATFORM - API TESTING")
    print("="*60)
    
    # Wait for services to be ready
    print("\nWaiting for services to be ready...")
    time.sleep(5)
    
    results = []
    
    results.append(("Health Check", test_health()))
    results.append(("User Registration", test_register()))
    results.append(("User Login", test_login()))
    
    if token:
        results.append(("Get Equipment", test_get_equipment()))
        results.append(("Get Categories", test_get_categories()))
        results.append(("Create Equipment", test_create_equipment()))
        results.append(("Create Request", test_create_request()))
        results.append(("Get Requests", test_get_requests()))
        results.append(("Get Current User", test_get_me()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)

if __name__ == "__main__":
    main()

