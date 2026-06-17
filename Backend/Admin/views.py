from Admin.models import Admin
from Auth.models import User
from Auth.Sign_up import signup
from Config import SessionLocal
from Department.models import Department
from sqlalchemy import outerjoin
from Documents.models import Documents,Notice, Request,Discussion,Report
from flask import jsonify, request
from Department.models import Department
import uuid
from datetime import datetime

def manage_users():
  db=SessionLocal()

  print("Managing users ...")
  All_users = db.query(User).all()
  db.close()
  users_list = []
  for user in All_users:
        users_list.append({
            "UserId": user.UserId,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "roles": user.roles,
            "deptId": user.deptId
        })
  return users_list
def update_user():
    db = SessionLocal()
    print("Updating user ...")
    data = request.get_json()
    try:
        user=db.query(User).filter(User.email==data.get('email')).first()
        if not user:
            return jsonify({'error':'User not found'}), 404
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if data.get('firstName'): user.firstName = data['firstName']
        if data.get('lastName'):  user.lastName  = data['lastName']
        if data.get('roles'):     user.roles     = data['roles']

        db.commit()
        return jsonify({'message': 'User updated successfully'}), 200 
    except:
        return jsonify({"Message":"The new data matches what we already have!"})            
    db.close()

def delete_user():
  db=SessionLocal()
  print("Deleting user ...")
  data =request.get_json()
 
  try:
        user = db.query(User).filter(User.email == data.get('email')).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        db.delete(user)
        db.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
  except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
  finally:
         db.close()

def create_user(user:User):
  print("Creating user ...")
  signup()

def manage_departments():
    print("Managing departments ...")
    db = SessionLocal()
    
    new_dept = Department()
    new_dept.deptId = input("Enter department ID: ")
    new_dept.deptName = input("Enter department name: ")
    if new_dept.deptId == db.query(Department).filter(Department.deptId == new_dept.deptId).first():
        print("Department ID already exists.")
        db.close()
        return {"error": "Department ID already exists."}
    
    db.add(new_dept)
    db.commit()
    db.close()

def get_documents():
    db = SessionLocal()
    try:
        docs = db.query(Documents)\
                 .outerjoin(Report,     Report.docId     == Documents.docId)\
                 .outerjoin(Notice,     Notice.docId     == Documents.docId)\
                 .outerjoin(Discussion, Discussion.docId == Documents.docId)\
                 .outerjoin(Request,    Request.docId    == Documents.docId)\
                 .all()

        if not docs:
            return jsonify([]), 200  # ← just return empty list, not an error
        
        result = []

        for doc in docs:
            entry = {
                'docId':       doc.docId,
                'docType':     doc.docType,
                'refNo':       doc.refNo,
                'dateCreated': str(doc.dateCreated),
                'title':       doc.title,
                'department':  doc.department.deptName if doc.department else 'N/A',  # ← via relationship
                'status':      None
            }

            if doc.docType == 'report' and doc.report:
                entry['status'] = 'Public' if doc.report.availability else 'Private'
            elif doc.docType == 'notice' and doc.notice:
                entry['status'] = 'N/A'
            elif doc.docType == 'discussion' and doc.discussion:
                entry['status'] = 'Discussed' if doc.discussion.isDiscussed else 'Pending'
            elif doc.docType == 'request' and doc.request:
                entry['status'] = doc.request.status
            result.append(entry)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


def get_stats():
    print("Getting Statistics ...")
    db = SessionLocal()
    totalUsers = db.query(User).count()
    totalDepartments = db.query(Department).count()
    totalDocs = db.query(Documents).count()

    return jsonify({
            'totalDocs': totalDocs,
            'totalUsers': totalUsers,
            'totalDepartments': totalDepartments
        }), 200
    db.close()


def add_document():
    db = SessionLocal()
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        # create the core document
        new_doc = Documents(
           
            docType     = data.get('docType'),
            refNo       = data.get('refNo'),
            dateCreated = str(datetime.now()),
            IsExternal  = int(data.get('isExternal', 0)),
            title       = data.get('title'),
            filepath    = data.get('filePath'),
            deptId      = data.get('deptId')
        )
        db.add(new_doc)
        db.flush()  # ← get docId before committing

        doc_type = data.get('docType')

        if doc_type == 'report':
            child = Report(
                docId        = new_doc.docId,
                creatorId    = data.get('creatorId'),
                availability = int(data.get('availability', 1))
            )
        elif doc_type == 'notice':
            child = Notice(
                docId   = new_doc.docId,
                sender  = data.get('sender'),
                subject = data.get('subject')
            )
        elif doc_type == 'discussion':
            child = Discussion(
                docId       = new_doc.docId,
                hostId      = data.get('hostId'),
                agenda      = data.get('agenda'),
                isDiscussed = int(data.get('isDiscussed', 0))
            )
        elif doc_type == 'request':
            child = Request(
                docId    = new_doc.docId,
                sender   = data.get('sender'),
                receiver = data.get('receiver'),
                status   = data.get('status', 'pending')
            )
        else:
            return jsonify({'error': 'Invalid document type'}), 400

        db.add(child)
        db.commit()
        return jsonify({'message': 'Document added successfully', 'docId': new_doc.docId}), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def search_documents():
    db = SessionLocal()
    data = request.get_json(silent=True)
    doc_type = data.get('docType') if data else None

    if not doc_type:
        return jsonify({'error': 'Document type is required'}), 400

    try:
        docs = db.query(Documents)\
         .outerjoin(Report,     Report.docId     == Documents.docId)\
         .outerjoin(Notice,     Notice.docId     == Documents.docId)\
         .outerjoin(Discussion, Discussion.docId == Documents.docId)\
         .outerjoin(Request,    Request.docId    == Documents.docId)\
         .order_by(Documents.dateCreated.desc())\
         .all()
        if not docs:
            return jsonify([]), 200

        result = []
        for doc in docs:
            entry = {
                'docId':       doc.docId,
                'docType':     doc.docType,
                'refNo':       doc.refNo,
                'dateCreated': str(doc.dateCreated),
                'title':       doc.title,
                'department':  doc.department.deptName if doc.department else 'N/A',
                'status':      None
            }

            if doc.docType == 'report' and doc.report:
                entry['status'] = 'Public' if doc.report.availability else 'Private'
            elif doc.docType == 'notice' and doc.notice:
                entry['status'] = doc.notice.subject
            elif doc.docType == 'discussion' and doc.discussion:
                entry['status'] = 'Discussed' if doc.discussion.isDiscussed else 'Pending'
            elif doc.docType == 'request' and doc.request:
                entry['status'] = doc.request.status

            result.append(entry)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def change_document_status():
    db = SessionLocal()
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    doc_id  = data.get('docId')
    new_status = data.get('status')

    try:
        doc = db.query(Documents).filter(Documents.docId == doc_id).first()
        if not doc:
            return jsonify({'error': 'Document not found'}), 404

        if doc.docType == 'request':
            if not doc.request:
                return jsonify({'error': 'Request record not found'}), 404
            doc.request.status = new_status

        elif doc.docType == 'report':
            if not doc.report:
                return jsonify({'error': 'Report record not found'}), 404
            doc.report.availability = 1 if new_status == 'Public' else 0

        elif doc.docType == 'discussion':
            if not doc.discussion:
                return jsonify({'error': 'Discussion record not found'}), 404
            doc.discussion.isDiscussed = 1 if new_status == 'Discussed' else 0

        else:
            return jsonify({'error': f'Document type {doc.docType} has no status field'}), 400

        db.commit()
        return jsonify({'message': 'Status updated successfully'}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
def view_document():
    db = SessionLocal()
    data = request.get_json(silent=True)
    doc_id = data.get('docId') if data else None

    if not doc_id:
        return jsonify({'error': 'docId is required'}), 400

    try:
        doc = db.query(Documents).filter(Documents.docId == doc_id).first()
        if not doc:
            return jsonify({'error': 'Document not found'}), 404

        entry = {
            'docId':       doc.docId,
            'docType':     doc.docType,
            'refNo':       doc.refNo,
            'dateCreated': str(doc.dateCreated),
            'title':       doc.title,
            'filePath':    doc.filepath,
            'isExternal':  doc.IsExternal,
            'department':  doc.department.deptName if doc.department else 'N/A',
        }

        if doc.docType == 'report' and doc.report:
            entry['details'] = {
                'creatorId':    doc.report.creatorId,
                'availability': 'Public' if doc.report.availability else 'Private'
            }
        elif doc.docType == 'notice' and doc.notice:
            entry['details'] = {
                'sender':  doc.notice.sender,
                'subject': doc.notice.subject
            }
        elif doc.docType == 'discussion' and doc.discussion:
            entry['details'] = {
                'hostId':      doc.discussion.hostId,
                'agenda':      doc.discussion.agenda,
                'isDiscussed': 'Discussed' if doc.discussion.isDiscussed else 'Pending'
            }
        elif doc.docType == 'request' and doc.request:
            entry['details'] = {
                'sender':   doc.request.sender,
                'receiver': doc.request.receiver,
                'status':   doc.request.status
            }
        else:
            entry['details'] = {}

        return jsonify(entry), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()        
def delete_document():
    db=SessionLocal()

    print("Deleting the document")

    data = request.get_json(silent=True)
    doc_id = data.get('docId') if data else None
    

    try:
        document= db.query(Documents).filter(Documents.docId==doc_id).first()
        db.delete(document)
        db.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
        db.close()
    except Exception as e:
        return jsonify({'error':str(e)}) ,500       
    
