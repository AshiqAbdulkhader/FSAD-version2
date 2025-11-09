#!/usr/bin/env python3
"""Test admin endpoints"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

# Register admin user
print("\n[TEST] Register Admin User")
admin_data = {
    "email": "admin@test.com",
    "password": "admin123",
    "name": "Admin User",
    "role": "admin"
}
response = requests.post(f"{BASE_URL}/auth/register", json=admin_data)
print(f"Status: {response.status_code}")
if response.status_code in [201, 400]:
    print("Admin user ready")

# Login as admin
print("\n[TEST] Login as Admin")
login_data = {
    "email": "admin@test.com",
    "password": "admin123"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Admin logged in")
    
    # Create equipment
    print("\n[TEST] Create Equipment (Admin)")
    equipment_data = {
        "name": "Test Laptop",
        "category": "Electronics",
        "condition": "excellent",
        "quantity": 3,
        "description": "Test laptop created by admin"
    }
    response = requests.post(f"{BASE_URL}/equipment", headers=headers, json=equipment_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✓ Equipment created")
    
    # Get dashboard stats
    print("\n[TEST] Get Dashboard Stats (Admin)")
    response = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"✓ Stats retrieved:")
        print(f"  - Total Equipment: {stats.get('total_equipment')}")
        print(f"  - Total Users: {stats.get('total_users')}")
        print(f"  - Pending Requests: {stats.get('pending_requests')}")
        print(f"  - Active Borrowings: {stats.get('active_borrowings')}")

print("\n✓ Admin endpoint tests complete!")

