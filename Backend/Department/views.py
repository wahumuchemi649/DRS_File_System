from Auth.models import User
from Config import SessionLocal
from Department.models import Department
from Documents.models import Documents

def departments():
     db = SessionLocal()
     departments = db.query(Department).all()
     departments_list = []
     for dept in departments:
          dept_info = {
               "deptId": dept.deptId,
               "deptName": dept.deptName
          }
          departments_list.append(dept_info)
     db.close()
     return departments_list


def dept_members(UserId):
     print("Users in the department:")
     db=SessionLocal()
     depthead = db.query(User).filter(User.UserId == UserId).first()
     members_list = []
     if depthead:
          members = db.query(
               User.UserId,
               User.firstName,
               User.lastName,
               User.email,
               Department.deptName,
          ).join(
               Department,
               User.deptId == Department.deptId
          ).filter(User.deptId == depthead.deptId).all()
          for member in members:
               member_info = {
                    "UserId": member.UserId,
                    "firstName": member.firstName,
                    "lastName": member.lastName,
                    "email": member.email,
                    "deptName": member.deptName
               }
               members_list.append(member_info)
    
     db.close()
     return members_list

def dept_documents(UserId):
     db = SessionLocal()
     depthead = db.query(User).filter(User.UserId == UserId).first()
     if depthead:
          documents= db.query(
               Documents.docId,
               Documents.title,
               Documents.docType,
               Documents.status,
               Documents.dateCreated,
          ).join(
               Department,
               Documents.deptId == Department.deptId
          ).filter(Documents.deptId == depthead.deptId).all()
          documents_list = []
          for doc in documents:
               doc_info = {
                    "docId": doc.docId,
                    "title": doc.title,
                    "docType": doc.docType,
                    "status": doc.status,
                    "dateCreated": doc.dateCreated
               }
               documents_list.append(doc_info)
     db.close()
     return documents_list