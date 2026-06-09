from Config import engine, SessionLocal, Base
from Auth.models import User
from Auth.Sign_up import signup


def database_init():
    print("Initializing the database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # You can add any initial data seeding here if necessary
        print("Database initialized successfully.")
    except Exception as e:
        print(f"An error occurred during database initialization: {e}")


def signup_user(user: User):
    
    print("Signup as a user")
    print("choose options")
    print("1. Signup as a user")
    print("2. Exit")
    choice = input("Enter your choice: ")
    if choice =='1':
        
        user.password = input("Enter password: ")
        if not user.password:
            print("Password is required.")
            return
        user.email = input("Enter email: ") 
        if not user.email:
            print("Email is required.")
            return
        if user.email.count('@') != 1 or user.email.startswith('@') or user.email.endswith('@') or user.email.count('@')==0:
            print("Invalid email format.")
            return
        user.roles = input("Enter role (Admin, Department Head, Officer, Registry): ")
        if not user.roles:
            print("Role is required.")
            return
        user.firstName = input("Enter first name: ")
        user.lastName = input("Enter last name: ")
        if user.roles == "Admin" or user.roles == "Registry":
            user.deptId = None
        else:
            user.deptId = input("Enter department ID: ")
        
        result = signup(user)
        print(result)
    elif choice == '2':
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")



if __name__ == "__main__":
    database_init()

    signup_user(User())
            
    