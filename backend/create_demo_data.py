#!/usr/bin/env python3

from app.db.database import SessionLocal, engine
from app.models import Base, User, Task, UserRole, TaskStatus, TaskPriority
from app.services.auth import get_password_hash
from datetime import datetime, timedelta
import random

def create_demo_data():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Task).delete()
        db.query(User).delete()
        db.commit()
        
        # Create demo users
        demo_users = [
            {
                "email": "admin@demo.com",
                "username": "admin",
                "password": "admin",
                "full_name": "Demo Administrator",
                "role": UserRole.ADMIN
            },
            {
                "email": "john@demo.com", 
                "username": "john_doe",
                "password": "john",
                "full_name": "John Doe",
                "role": UserRole.USER
            },
            {
                "email": "jane@demo.com",
                "username": "jane_smith", 
                "password": "jane",
                "full_name": "Jane Smith",
                "role": UserRole.USER
            },
            {
                "email": "bob@demo.com",
                "username": "bob_wilson",
                "password": "bob", 
                "full_name": "Bob Wilson",
                "role": UserRole.USER
            }
        ]
        
        created_users = []
        for user_data in demo_users:
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=get_password_hash(user_data["password"]),
                full_name=user_data["full_name"],
                role=user_data["role"],
                is_active=True
            )
            db.add(user)
            created_users.append(user)
        
        db.commit()
        
        # Refresh users to get their IDs
        for user in created_users:
            db.refresh(user)
        
        print(f"Created {len(created_users)} demo users:")
        for user in created_users:
            role_display = "Admin" if user.role == UserRole.ADMIN else "User"
            print(f"  - {user.full_name} ({user.email}) - {role_display}")
        
        # Create demo tasks
        task_templates = [
            {
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the API endpoints and frontend components",
                "priority": TaskPriority.HIGH,
                "status": TaskStatus.IN_PROGRESS
            },
            {
                "title": "Fix authentication bug",
                "description": "Users are reporting login issues with the JWT token expiration",
                "priority": TaskPriority.HIGH,
                "status": TaskStatus.TODO
            },
            {
                "title": "Implement password reset feature",
                "description": "Add functionality for users to reset their forgotten passwords",
                "priority": TaskPriority.MEDIUM,
                "status": TaskStatus.TODO
            },
            {
                "title": "Add unit tests",
                "description": "Write comprehensive unit tests for all API endpoints",
                "priority": TaskPriority.MEDIUM,
                "status": TaskStatus.TODO
            },
            {
                "title": "Optimize database queries",
                "description": "Review and optimize slow database queries for better performance",
                "priority": TaskPriority.LOW,
                "status": TaskStatus.TODO
            },
            {
                "title": "Update dependencies",
                "description": "Update all npm and pip packages to their latest stable versions",
                "priority": TaskPriority.LOW,
                "status": TaskStatus.COMPLETED
            },
            {
                "title": "Design new dashboard UI",
                "description": "Create mockups and implement the new dashboard design",
                "priority": TaskPriority.MEDIUM,
                "status": TaskStatus.IN_PROGRESS
            },
            {
                "title": "Setup CI/CD pipeline",
                "description": "Configure GitHub Actions for automated testing and deployment",
                "priority": TaskPriority.HIGH,
                "status": TaskStatus.TODO
            },
            {
                "title": "Add user profile page",
                "description": "Create a page where users can view and edit their profile information",
                "priority": TaskPriority.MEDIUM,
                "status": TaskStatus.TODO
            },
            {
                "title": "Implement search functionality",
                "description": "Add search feature to find tasks by title or description",
                "priority": TaskPriority.LOW,
                "status": TaskStatus.TODO
            }
        ]
        
        created_tasks = []
        for i, task_template in enumerate(task_templates):
            # Randomly assign tasks to users (excluding admin)
            user = random.choice([u for u in created_users if u.role == UserRole.USER])
            
            # Random creation times within the last 30 days
            days_ago = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            # Set completed_at for completed tasks
            completed_at = None
            if task_template["status"] == TaskStatus.COMPLETED:
                completed_at = created_at + timedelta(days=random.randint(1, min(days_ago, 5)))
            
            task = Task(
                title=task_template["title"],
                description=task_template["description"],
                priority=task_template["priority"],
                status=task_template["status"],
                is_completed=task_template["status"] == TaskStatus.COMPLETED,
                owner_id=user.id,
                created_at=created_at,
                completed_at=completed_at
            )
            db.add(task)
            created_tasks.append(task)
        
        db.commit()
        
        print(f"\nCreated {len(created_tasks)} demo tasks:")
        for task in created_tasks:
            owner = next(u for u in created_users if u.id == task.owner_id)
            status_icon = "completed" if task.is_completed else "pending"
            print(f"  - {task.title} (Owner: {owner.full_name}, Priority: {task.priority}, Status: {task.status})")
        
        print("\n" + "="*50)
        print("DEMO DATABASE CREATED SUCCESSFULLY!")
        print("="*50)
        print("\nLogin Credentials:")
        print("Admin User:")
        print("  Email: admin@demo.com")
        print("  Password: admin")
        print("\nRegular Users:")
        print("  Email: john@demo.com     Password: john")
        print("  Email: jane@demo.com     Password: jane") 
        print("  Email: bob@demo.com      Password: bob")
        print("\nAccess the application at:")
        print("  Frontend: http://localhost:3000")
        print("  Backend API: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"Error creating demo data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating demo database with sample data...")
    create_demo_data()
    print("\nDemo database setup completed!")
