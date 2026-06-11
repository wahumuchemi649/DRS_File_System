from Auth.models import User
from Config import SessionLocal

def login(email: str, password: str):
  db = SessionLocal()
  try:

    existing_user = db.query(User).filter((User.email == email)).first()
    if not existing_user:
      return{"error": "Email not found"}

    if existing_user.password == password:
      return{"message": "Successful login", "email": existing_user.email, "roles": existing_user.roles}
    else:
      return{"error": "Incorrect Password"}

  
  except Exception as e:
    return {"error": str(e)}


# testing purposes
if __name__ == "__main__":
  result = login("test@example.com", "test1234")
  print(result)

  