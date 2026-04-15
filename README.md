# Scalable FastAPI Assignment

A scalable REST API with authentication, role-based access control, and a React frontend for task management.

## Features

### Backend (FastAPI)
- **Authentication**: JWT-based authentication with secure password hashing
- **Role-Based Access Control**: User and Admin roles with different permissions
- **Task Management**: Complete CRUD operations for tasks with status and priority
- **API Versioning**: Versioned API endpoints (`/api/v1/`)
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Validation**: Pydantic models for request/response validation

### Frontend (React)
- **Authentication**: Login/Register forms with JWT token management
- **Task Dashboard**: Create, read, update, and delete tasks
- **Role-Based UI**: Different interfaces for users and admins
- **Responsive Design**: Mobile-friendly interface
- **Error Handling**: User-friendly error messages
- **State Management**: React Context for authentication state

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **JWT**: JSON Web Tokens for authentication
- **bcrypt**: Password hashing
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React**: JavaScript library for building user interfaces
- **TypeScript**: Type-safe JavaScript
- **Axios**: HTTP client for API requests
- **CSS3**: Modern styling with responsive design

## Project Structure

```
scalable-fastapi-assignment/
|
+-- backend/
|   +-- app/
|   |   +-- core/           # Configuration and security
|   |   +-- db/             # Database setup
|   |   +-- models/         # SQLAlchemy models
|   |   +-- routers/        # API endpoints
|   |   +-- schemas/        # Pydantic models
|   |   +-- services/       # Business logic
|   |   +-- main.py         # FastAPI application
|   +-- requirements.txt    # Python dependencies
|   +-- init_db.py         # Database initialization
|   +-- .env.example       # Environment variables template
|
+-- frontend/
|   +-- src/
|   |   +-- components/     # React components
|   |   +-- contexts/       # React contexts
|   |   +-- services/       # API services
|   |   +-- types/          # TypeScript types
|   |   +-- App.tsx         # Main React component
|   +-- package.json        # Node.js dependencies
|
+-- README.md               # This file
```

## Quick Start

### Option 1: One-Click Startup (Recommended)
```bash
# Navigate to project root
cd scalable-fastapi-assignment

# Run the startup script
.\start_all.bat
```

This will automatically start both backend and frontend servers in separate windows.

### Option 2: Manual Startup
```bash
# Backend (Terminal 1)
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (Terminal 2)
cd frontend
npm start
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Demo Login Credentials
- **Admin**: admin@demo.com / admin
- **Users**: john@demo.com / john, jane@demo.com / jane, bob@demo.com / bob

### Demo Database Setup
To populate the database with sample data:
```bash
cd backend
venv\Scripts\activate
python create_demo_data.py
```

This creates:
- 4 demo users (1 admin, 3 regular users)
- 10 sample tasks with various priorities and statuses
- Realistic task descriptions for testing

Or use the quick setup script:
```bash
cd backend
setup_demo.bat
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd scalable-fastapi-assignment
```

2. **Set up Python virtual environment**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials and JWT secret
```

5. **Set up PostgreSQL database**
```sql
CREATE DATABASE your_database_name;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_user;
```

6. **Initialize the database**
```bash
python init_db.py
```

7. **Run the backend server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Default Users

After running `init_db.py`, two default users are created:

### Admin User
- **Email**: admin@example.com
- **Password**: admin123
- **Role**: Admin

### Test User
- **Email**: user@example.com
- **Password**: user123
- **Role**: User

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Users
- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/users/` - Get all users (Admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID (Admin only)

### Tasks
- `GET /api/v1/tasks/` - Get all tasks (user's tasks or all if admin)
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/{task_id}` - Get task by ID
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

## Usage Examples

### Register a new user
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
-H "Content-Type: application/json" \
-d '{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "password123",
  "full_name": "New User"
}'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=newuser@example.com&password=password123"
```

### Create a task (with JWT token)
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "title": "Complete assignment",
  "description": "Finish the scalable FastAPI assignment",
  "priority": "high"
}'
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication with configurable expiration
- **Role-Based Access Control**: Different permissions for users and admins
- **Input Validation**: Pydantic models validate all inputs
- **CORS Protection**: Configurable CORS origins
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Scalability Considerations

### Current Implementation
- **Database Indexing**: Proper indexes on frequently queried fields
- **Connection Pooling**: SQLAlchemy connection pooling
- **JWT Stateless**: No server-side session storage
- **Modular Architecture**: Clean separation of concerns

### Future Enhancements
- **Caching**: Redis for frequently accessed data
- **Load Balancing**: Multiple API instances behind a load balancer
- **Microservices**: Split into separate services (auth, tasks, users)
- **Database Sharding**: Horizontal database scaling
- **Message Queue**: Async task processing with Celery/RabbitMQ
- **Containerization**: Docker for easy deployment
- **Monitoring**: Application monitoring and logging

## Deployment

### Docker Deployment (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment
1. Set up production database
2. Configure environment variables
3. Build frontend: `npm run build`
4. Run backend with production WSGI server (Gunicorn)
5. Set up reverse proxy (Nginx)
6. Configure SSL certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on the GitHub repository.