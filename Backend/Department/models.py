from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from Config import Base
class Department(Base):
    
    __tablename__ = "department"

    
    deptId = Column(String(20), primary_key=True)
    deptName = Column(String(50), nullable=False)
    documents = relationship('Documents', back_populates='department')  