#!/usr/bin/env python3

from app.db.database import SessionLocal, engine
from app.models import Base, User, UserRole
from app.services.auth import get_password_hash

def init_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        
        if not admin_user:
            # Create default admin user
            admin_user = User(
                email="admin@example.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Created default admin user:")
            print("Email: admin@example.com")
            print("Password: admin123")
        else:
            print("Admin user already exists")
            
        # Create a test user
        test_user = db.query(User).filter(User.email == "user@example.com").first()
        
        if not test_user:
            test_user = User(
                email="user@example.com",
                username="testuser",
                hashed_password=get_password_hash("user123"),
                full_name="Test User",
                role=UserRole.USER,
                is_active=True
            )
            db.add(test_user)
            db.commit()
            print("Created default test user:")
            print("Email: user@example.com")
            print("Password: user123")
        else:
            print("Test user already exists")
            
    except Exception as e:
        print(f"Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    print("Database initialization completed!")
