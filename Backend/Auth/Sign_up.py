from Auth.models import User
from Config import SessionLocal

def signup(user:User):
    db = SessionLocal()
    try:
    
        existing_user = db.query(User).filter( (User.email == user.email)).first()
        if existing_user:
            return {"error": "Email already exists"}
        

        # Create a new user instance
        new_user = User(
            
            password=user.password,  # In production, ensure to hash the password
            email=user.email,
            roles=user.roles,
            firstName=user.firstName,
            lastName=user.lastName,
            deptId=user.deptId
        )

        # Add the new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully", "user_id": new_user.UserId}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()