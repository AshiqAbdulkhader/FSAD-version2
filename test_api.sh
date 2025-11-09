#!/bin/bash
# API Testing Script for Equipment Lending Platform

echo "=========================================="
echo "Testing Equipment Lending Platform API"
echo "=========================================="
echo ""

BASE_URL="http://localhost:5000/api"
TOKEN=""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test health endpoint
echo "1. Testing Health Endpoint..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
if [ "$response" == "200" ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed (Status: $response)${NC}"
fi
echo ""

# Test user registration
echo "2. Testing User Registration..."
register_response=$(curl -s -X POST "$BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test@example.com",
        "password": "test123",
        "name": "Test User",
        "role": "student"
    }')
echo "Response: $register_response"
echo ""

# Test user login
echo "3. Testing User Login..."
login_response=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test@example.com",
        "password": "test123"
    }')
TOKEN=$(echo $login_response | grep -o '"token":"[^"]*' | cut -d'"' -f4)
if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ Login successful, token received${NC}"
else
    echo -e "${RED}✗ Login failed${NC}"
    echo "Response: $login_response"
fi
echo ""

# Test get equipment (requires auth)
if [ -n "$TOKEN" ]; then
    echo "4. Testing Get Equipment List..."
    equipment_response=$(curl -s -X GET "$BASE_URL/equipment" \
        -H "Authorization: Bearer $TOKEN")
    if echo "$equipment_response" | grep -q "id"; then
        echo -e "${GREEN}✓ Equipment list retrieved${NC}"
    else
        echo -e "${RED}✗ Failed to get equipment${NC}"
        echo "Response: $equipment_response"
    fi
    echo ""
    
    echo "5. Testing Get Categories..."
    categories_response=$(curl -s -X GET "$BASE_URL/equipment/categories" \
        -H "Authorization: Bearer $TOKEN")
    echo "Categories: $categories_response"
    echo ""
fi

echo "=========================================="
echo "Testing Complete"
echo "=========================================="

