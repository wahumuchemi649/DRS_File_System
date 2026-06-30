from Registry.models import Document
from Config import SessionLocal

def route_document(doc_id: int, dept_id: str):
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.docId == doc_id).first()

        if not document:
            return {"error": "Document not found"}

        document.status = "Routed"
        document.deptId = dept_id
        db.commit()
        db.refresh(document)

        return {
            "message": "Document routed successfully",
            "docId": document.docId,
            "refNo": document.refNo,
            "status": document.status,
            "deptId": document.deptId
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    result = route_document(1, "HR01")
    print(result)