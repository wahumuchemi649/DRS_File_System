from sqlalchemy import Column, Integer, String, Enum
from Config import Base  
class User(Base):
    
    __tablename__ = "Users"

    
    UserId = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    roles = Column(Enum('Admin', 'Department Head', 'Officer', 'Registry'), nullable=False)
    firstName = Column(String(30))
    lastName = Column(String(30))
    deptId = Column(String(20))

    # Tell SQLAlchemy to use the 'roles' column for inheritance mapping
    __mapper_args__ = {
        "polymorphic_on": roles,
        "polymorphic_identity": "user" # Default identity
    }

    
    def AdminUser(self):
        return self.roles == "Admin"
    def DepartmentHeadUser(self):
        return self.roles == "Department Head"  
    def OfficerUser(self):  
        return self.roles == "Officer"
    def RegistryUser(self):
        return self.roles == "Registry"