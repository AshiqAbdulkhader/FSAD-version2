# School Equipment Lending Platform

A web-based Equipment Lending Portal to manage and track borrowing requests, approvals, and returns for schools.

## Features

- **User Authentication & Roles**: Login/signup for students, staff, and admins with role-based access control
- **Equipment Management**: Add, edit, delete, and view equipment with categories, conditions, and availability tracking
- **Borrowing & Return Requests**: Students can request equipment, staff/admin can approve/reject, and track returns
- **Overlap Prevention**: Prevents overlapping bookings for the same equipment
- **Dashboard**: Equipment listing with search/filter functionality and role-based dashboards
- **Responsive UI**: Modern React frontend with Material-UI components

## Tech Stack

### Backend
- **Python 3.11** with Flask
- **PostgreSQL** database
- **JWT** authentication
- **bcrypt** for password hashing

### Frontend
- **React 18** with React Router
- **Material-UI** for components
- **Axios** for API calls

### Infrastructure
- **Docker** and **Docker Compose** for containerization
- **PostgreSQL** in Docker container

## Project Structure

```
FSAD-version2/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend container definition
│   ├── config/
│   │   └── database.py        # Database connection pool
│   ├── middleware/
│   │   └── auth.py            # Authentication middleware
│   ├── routes/
│   │   ├── auth.py            # Authentication routes
│   │   ├── equipment.py       # Equipment management routes
│   │   ├── requests.py        # Borrowing request routes
│   │   └── dashboard.py       # Dashboard routes
│   └── db/
│       └── init.sql           # Database schema and initial data
├── frontend/
│   ├── src/
│   │   ├── App.js             # Main React app
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── context/          # React context (Auth)
│   │   └── services/         # API service layer
│   ├── package.json           # Frontend dependencies
│   └── Dockerfile             # Frontend container definition
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

## Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd FSAD-version2
```

### 2. Start the application with Docker Compose

```bash
docker-compose up --build
```

This will:
- Start PostgreSQL database
- Build and start the Python Flask backend
- Build and start the React frontend
- Initialize the database with schema and sample data

### 3. Access the application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Database**: localhost:5432

### 4. Create an admin user

1. Go to http://localhost:3000/signup
2. Register with role "admin"
3. Use this account to manage equipment and approve requests

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Equipment
- `GET /api/equipment` - List all equipment (with filters)
- `GET /api/equipment/:id` - Get equipment details
- `POST /api/equipment` - Create equipment (admin only)
- `PUT /api/equipment/:id` - Update equipment (admin only)
- `DELETE /api/equipment/:id` - Delete equipment (admin only)
- `GET /api/equipment/categories` - Get all categories

### Borrowing Requests
- `GET /api/requests` - List requests (filtered by role)
- `GET /api/requests/:id` - Get request details
- `POST /api/requests` - Create borrowing request
- `PUT /api/requests/:id/approve` - Approve request (staff/admin)
- `PUT /api/requests/:id/reject` - Reject request (staff/admin)
- `PUT /api/requests/:id/return` - Mark as returned (staff/admin)

### Dashboard
- `GET /api/dashboard/stats` - Get statistics (admin only)

## User Roles

- **Student**: Can view equipment, create borrowing requests, and view their own requests
- **Staff**: Can do everything students can, plus approve/reject requests and mark returns
- **Admin**: Full access including equipment management and dashboard statistics

## Environment Variables

### Backend (.env)
```
PORT=5000
DB_HOST=postgres
DB_PORT=5432
DB_NAME=equipment_lending
DB_USER=postgres
DB_PASSWORD=postgres
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRES_IN=7d
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Development

### Running without Docker

#### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

#### Database
Make sure PostgreSQL is running and update the connection settings in `backend/.env`

## Database Schema

- **users**: User accounts with email, password (hashed), name, and role
- **equipment**: Equipment items with name, category, condition, quantity, and description
- **borrowing_requests**: Requests linking users to equipment with dates and status

## Features Implemented

✅ User authentication with JWT tokens
✅ Role-based access control
✅ Equipment CRUD operations
✅ Borrowing request workflow
✅ Overlap prevention for bookings
✅ Search and filter functionality
✅ Responsive Material-UI design
✅ Docker containerization
✅ PostgreSQL database with proper schema

## Troubleshooting

### Database connection issues
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check database logs: `docker-compose logs postgres`

### Backend not starting
- Check Python dependencies: `docker-compose logs backend`
- Verify environment variables are set correctly

### Frontend not connecting to backend
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS settings in backend

## License

This project is for educational purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

