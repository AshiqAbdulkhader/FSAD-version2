# Testing Guide

This document outlines how to test the Equipment Lending Platform.

## Prerequisites

1. Docker and Docker Compose installed
2. All services running via `docker-compose up`

## Manual Testing Steps

### 1. Start the Application

```bash
docker-compose up --build
```

Wait for all services to be healthy:
- PostgreSQL: Check logs with `docker-compose logs postgres`
- Backend: Check logs with `docker-compose logs backend`
- Frontend: Check logs with `docker-compose logs frontend`

### 2. Test Backend API

#### Health Check
```bash
curl http://localhost:5000/health
```
Expected: `{"status": "OK", "message": "Server is running"}`

#### Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@school.edu",
    "password": "admin123",
    "name": "Admin User",
    "role": "admin"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@school.edu",
    "password": "admin123"
  }'
```
Save the token from the response.

#### Get Equipment List (requires token)
```bash
curl -X GET http://localhost:5000/api/equipment \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Create Equipment (admin only)
```bash
curl -X POST http://localhost:5000/api/equipment \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Equipment",
    "category": "Test Category",
    "condition": "good",
    "quantity": 5,
    "description": "Test description"
  }'
```

#### Create Borrowing Request
```bash
curl -X POST http://localhost:5000/api/requests \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": 1,
    "start_date": "2024-12-01",
    "end_date": "2024-12-05"
  }'
```

### 3. Test Frontend

1. Open browser: http://localhost:3000
2. Test user registration
3. Test login
4. Browse equipment
5. Create a borrowing request
6. Test admin features (if logged in as admin)

## Automated Testing

Run the test script (requires curl):
```bash
chmod +x test_api.sh
./test_api.sh
```

## Test Scenarios

### Scenario 1: User Registration and Login
1. Register a new student user
2. Login with credentials
3. Verify token is received
4. Access protected endpoint with token

### Scenario 2: Equipment Management (Admin)
1. Login as admin
2. Create new equipment
3. View equipment list
4. Update equipment
5. Delete equipment

### Scenario 3: Borrowing Request Flow
1. Login as student
2. Browse available equipment
3. Create a borrowing request
4. Login as staff/admin
5. Approve the request
6. Mark equipment as returned

### Scenario 4: Overlap Prevention
1. Create a request for dates Dec 1-5
2. Try to create another request for the same equipment on Dec 3-7
3. Should fail if quantity is insufficient

### Scenario 5: Role-Based Access
1. Login as student - verify limited access
2. Login as staff - verify can approve requests
3. Login as admin - verify full access

## Expected Results

- All API endpoints return appropriate status codes
- Authentication works correctly
- Role-based access is enforced
- Equipment CRUD operations work
- Borrowing requests can be created, approved, and marked returned
- Overlap prevention prevents double-booking
- Frontend displays data correctly
- Navigation works between pages

## Troubleshooting

### Backend not starting
- Check database connection: `docker-compose logs backend`
- Verify environment variables
- Check if PostgreSQL is healthy: `docker-compose ps`

### Frontend not connecting
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS settings in backend
- Check browser console for errors

### Database errors
- Check PostgreSQL logs: `docker-compose logs postgres`
- Verify database is initialized: Check if tables exist
- Restart database: `docker-compose restart postgres`

