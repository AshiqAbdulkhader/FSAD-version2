# School Equipment Lending Platform - Implementation Plan

## Project Overview
A web-based Equipment Lending Portal to manage borrowing requests, approvals, and returns for schools.

## Project Structure
```
FSAD-version2/
├── backend/
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── server.js
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   ├── utils/
│   │   └── App.js
│   ├── Dockerfile
│   ├── package.json
│   └── public/
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Phase 1: Project Setup & Infrastructure

### Step 1.1: Initialize Backend Structure
- [ ] Create `backend/` folder
- [ ] Initialize Node.js project with `package.json`
- [ ] Install dependencies:
  - Express.js (web framework)
  - PostgreSQL client (pg or sequelize)
  - JWT (jsonwebtoken) for authentication
  - bcrypt for password hashing
  - dotenv for environment variables
  - cors for cross-origin requests
  - express-validator for input validation
- [ ] Create basic Express server structure
- [ ] Set up environment variables (.env.example)

### Step 1.2: Initialize Frontend Structure
- [ ] Create `frontend/` folder
- [ ] Initialize React app (Create React App or Vite)
- [ ] Install dependencies:
  - React Router for navigation
  - Axios for API calls
  - Context API or Redux for state management
  - Material-UI or Tailwind CSS for styling
- [ ] Set up basic routing structure

### Step 1.3: Database Schema Design
- [ ] Design PostgreSQL schema:
  - **users** table:
    - id (primary key)
    - email (unique)
    - password (hashed)
    - name
    - role (student, staff, admin)
    - created_at, updated_at
  - **equipment** table:
    - id (primary key)
    - name
    - category
    - condition (excellent, good, fair, poor)
    - quantity (total available)
    - description
    - created_at, updated_at
  - **borrowing_requests** table:
    - id (primary key)
    - user_id (foreign key to users)
    - equipment_id (foreign key to equipment)
    - request_date
    - start_date
    - end_date
    - status (pending, approved, rejected, returned)
    - approved_by (foreign key to users, nullable)
    - approval_date
    - return_date
    - created_at, updated_at
- [ ] Create migration files or SQL scripts

### Step 1.4: Docker Setup
- [ ] Create `docker-compose.yml`:
  - PostgreSQL service (with volume for data persistence)
  - Backend service (Node.js)
  - Frontend service (React)
  - Network configuration
- [ ] Create `backend/Dockerfile`
- [ ] Create `frontend/Dockerfile`
- [ ] Configure environment variables for containers

---

## Phase 2: Backend Development

### Step 2.1: Database Connection & Models
- [ ] Set up PostgreSQL connection pool
- [ ] Create database models/ORM setup
- [ ] Create database initialization script
- [ ] Test database connection

### Step 2.2: Authentication System
- [ ] Create authentication middleware (JWT verification)
- [ ] Implement `/api/auth/register` endpoint:
  - Hash passwords with bcrypt
  - Validate input (email, password, role)
  - Create user in database
- [ ] Implement `/api/auth/login` endpoint:
  - Verify credentials
  - Generate JWT token
  - Return token and user info
- [ ] Create role-based authorization middleware

### Step 2.3: Equipment Management API
- [ ] Implement `/api/equipment` endpoints:
  - `GET /api/equipment` - List all equipment (with filters)
  - `GET /api/equipment/:id` - Get single equipment
  - `POST /api/equipment` - Create equipment (admin only)
  - `PUT /api/equipment/:id` - Update equipment (admin only)
  - `DELETE /api/equipment/:id` - Delete equipment (admin only)
- [ ] Add validation for equipment data
- [ ] Implement search/filter functionality (by category, availability)

### Step 2.4: Borrowing Request API
- [ ] Implement `/api/requests` endpoints:
  - `GET /api/requests` - List requests (filtered by user role)
  - `GET /api/requests/:id` - Get single request
  - `POST /api/requests` - Create borrowing request (student/staff)
  - `PUT /api/requests/:id/approve` - Approve request (staff/admin)
  - `PUT /api/requests/:id/reject` - Reject request (staff/admin)
  - `PUT /api/requests/:id/return` - Mark as returned (staff/admin)
- [ ] Implement overlap prevention logic:
  - Check if equipment is available for requested dates
  - Validate start_date < end_date
  - Prevent double-booking

### Step 2.5: Dashboard & Analytics API
- [ ] Implement `/api/dashboard` endpoints:
  - `GET /api/dashboard/stats` - Get statistics (admin)
  - Equipment availability counts
  - Pending requests count
  - Active borrowings count

### Step 2.6: Error Handling & Validation
- [ ] Create centralized error handling middleware
- [ ] Add input validation for all endpoints
- [ ] Create custom error classes
- [ ] Add request logging

---

## Phase 3: Frontend Development

### Step 3.1: Authentication UI
- [ ] Create Login page component
- [ ] Create Signup page component
- [ ] Implement authentication context/state management
- [ ] Create protected route wrapper
- [ ] Store JWT token in localStorage/sessionStorage
- [ ] Add logout functionality

### Step 3.2: Navigation & Layout
- [ ] Create main layout component with navigation
- [ ] Implement role-based navigation menu
- [ ] Create header/footer components
- [ ] Add responsive design

### Step 3.3: Equipment Management UI
- [ ] Create Equipment List page:
  - Display all equipment in cards/table
  - Search bar
  - Filter by category
  - Filter by availability
- [ ] Create Equipment Detail page
- [ ] Create Add/Edit Equipment form (admin only)
- [ ] Implement delete confirmation modal

### Step 3.4: Borrowing Request UI
- [ ] Create Request Equipment page:
  - Equipment selection
  - Date picker (start_date, end_date)
  - Submit request form
- [ ] Create My Requests page:
  - List user's requests
  - Show request status
  - Cancel pending requests
- [ ] Create Admin Requests Management page:
  - List all pending requests
  - Approve/Reject buttons
  - Mark as returned functionality
  - Filter by status

### Step 3.5: Dashboard UI
- [ ] Create Dashboard page:
  - Statistics cards (for admin)
  - Recent requests
  - Equipment availability overview
- [ ] Create different dashboard views per role:
  - Student: My requests, available equipment
  - Staff: Pending approvals, equipment list
  - Admin: Full dashboard with stats

### Step 3.6: API Integration
- [ ] Create API service layer (axios instance)
- [ ] Implement API calls for all endpoints
- [ ] Add request interceptors (attach JWT token)
- [ ] Add response interceptors (handle errors)
- [ ] Create custom hooks for data fetching

### Step 3.7: UI/UX Polish
- [ ] Add loading states
- [ ] Add error messages/toasts
- [ ] Add success notifications
- [ ] Implement form validation
- [ ] Add responsive design for mobile
- [ ] Add loading spinners/skeletons

---

## Phase 4: Integration & Testing

### Step 4.1: Docker Integration
- [ ] Test backend container builds
- [ ] Test frontend container builds
- [ ] Test docker-compose up (all services)
- [ ] Verify database connection from backend
- [ ] Verify API connection from frontend
- [ ] Test environment variable injection

### Step 4.2: End-to-End Testing
- [ ] Test user registration and login
- [ ] Test equipment CRUD operations
- [ ] Test borrowing request flow:
  - Create request
  - Approve request
  - Mark as returned
- [ ] Test overlap prevention
- [ ] Test role-based access control

### Step 4.3: Error Scenarios
- [ ] Test invalid login credentials
- [ ] Test unauthorized access attempts
- [ ] Test overlapping booking prevention
- [ ] Test form validation errors
- [ ] Test network error handling

---

## Phase 5: Documentation & Deployment

### Step 5.1: Documentation
- [ ] Create README.md with:
  - Project description
  - Setup instructions
  - API documentation
  - Environment variables
  - Docker commands
- [ ] Add code comments
- [ ] Document database schema

### Step 5.2: Final Polish
- [ ] Code cleanup and optimization
- [ ] Remove console.logs
- [ ] Add .gitignore entries
- [ ] Verify all features work together
- [ ] Performance optimization

---

## Technical Stack Summary

### Backend
- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: PostgreSQL
- **Authentication**: JWT (jsonwebtoken)
- **Password Hashing**: bcrypt
- **Validation**: express-validator

### Frontend
- **Framework**: React
- **Routing**: React Router
- **HTTP Client**: Axios
- **State Management**: Context API or Redux
- **Styling**: Material-UI or Tailwind CSS

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Database**: PostgreSQL (containerized)

---

## API Endpoints Summary

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Equipment
- `GET /api/equipment` - List equipment (with filters)
- `GET /api/equipment/:id` - Get equipment details
- `POST /api/equipment` - Create equipment (admin)
- `PUT /api/equipment/:id` - Update equipment (admin)
- `DELETE /api/equipment/:id` - Delete equipment (admin)

### Borrowing Requests
- `GET /api/requests` - List requests
- `GET /api/requests/:id` - Get request details
- `POST /api/requests` - Create request
- `PUT /api/requests/:id/approve` - Approve request (staff/admin)
- `PUT /api/requests/:id/reject` - Reject request (staff/admin)
- `PUT /api/requests/:id/return` - Mark as returned (staff/admin)

### Dashboard
- `GET /api/dashboard/stats` - Get statistics (admin)

---

## Database Schema Details

### users
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'staff', 'admin')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### equipment
```sql
CREATE TABLE equipment (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(100) NOT NULL,
  condition VARCHAR(50) NOT NULL CHECK (condition IN ('excellent', 'good', 'fair', 'poor')),
  quantity INTEGER NOT NULL DEFAULT 1,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### borrowing_requests
```sql
CREATE TABLE borrowing_requests (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  equipment_id INTEGER REFERENCES equipment(id) ON DELETE CASCADE,
  request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'returned')),
  approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
  approval_date TIMESTAMP,
  return_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (start_date <= end_date)
);
```

### Indexes
```sql
CREATE INDEX idx_borrowing_requests_equipment ON borrowing_requests(equipment_id);
CREATE INDEX idx_borrowing_requests_user ON borrowing_requests(user_id);
CREATE INDEX idx_borrowing_requests_dates ON borrowing_requests(start_date, end_date);
CREATE INDEX idx_equipment_category ON equipment(category);
```

---

## Environment Variables

### Backend (.env)
```
PORT=5000
DB_HOST=postgres
DB_PORT=5432
DB_NAME=equipment_lending
DB_USER=postgres
DB_PASSWORD=postgres
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=7d
NODE_ENV=development
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

---

## Docker Compose Configuration

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: equipment_lending
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=development
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=equipment_lending
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - JWT_SECRET=your-secret-key-change-in-production
      - FRONTEND_URL=http://localhost:3000
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - /app/node_modules

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5000/api
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

---

## Implementation Order Priority

1. **Critical Path** (Must have first):
   - Database setup
   - Authentication system
   - Basic equipment CRUD
   - Basic borrowing request flow

2. **High Priority**:
   - Overlap prevention
   - Role-based access
   - Dashboard

3. **Medium Priority**:
   - Search/filter functionality
   - UI polish
   - Error handling

4. **Nice to Have**:
   - Advanced analytics
   - Email notifications
   - Equipment images

---

## Estimated Timeline

- **Phase 1** (Setup): 1-2 days
- **Phase 2** (Backend): 3-4 days
- **Phase 3** (Frontend): 4-5 days
- **Phase 4** (Integration): 1-2 days
- **Phase 5** (Documentation): 1 day

**Total**: ~10-14 days for complete implementation

---

## Next Steps

1. Review and approve this plan
2. Start with Phase 1: Project Setup
3. Set up version control (Git)
4. Begin implementation following the step-by-step checklist

