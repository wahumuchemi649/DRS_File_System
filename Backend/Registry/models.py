from sqlalchemy import Column, Integer, String, Boolean, Enum, TIMESTAMP
from Config import Base

class Document(Base):
  __tablename__ = "documents"
  docId = Column(Integer, primary_key = True, autoincrement = True)
  docType = Column(String(20))
  refNo = Column(String(20))
  dateCreated = Column(TIMESTAMP)
  IsExternal = Column(Boolean)
  title = Column(String(20))
  filePath = Column(String(255))
  deptId = Column(String(20))
  status = Column(Enum('Received','Registered','Routed', 'Under Review', 'Approved'), default = 'Received')


  #testing purposes
#if __name__ == "__main__":
 # from Config import SessionLocal

  #db = SessionLocal()
  #docs = db.query(Document).all()
  #print(docs)