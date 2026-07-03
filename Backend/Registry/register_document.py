from Documents.models import Documents as Document
from Config import SessionLocal

def register_by_id(doc_id: int):
    db = SessionLocal()
    try:
        # Step 1: Find the document by ID
        document = db.query(Document).filter(Document.docId == doc_id).first()

        # Step 2: Check if it exists
        if not document:
            return {"error": "Document not found"}

        # Step 3: Check if it's in Received status
        if document.status != "Received":
            return {"error": f"Document is already '{document.status}'. Can only register Received documents."}

        # Step 4: Generate a ref number
        count = db.query(Document).count()
        ref_no = f"REF-{count + 1:04d}"

        # Step 5: Update the document
        document.refNo = ref_no
        document.status = "Registered"

        # Step 6: Save changes
        db.commit()
        db.refresh(document)

        return {
            "message": "Document registered successfully",
            "ref_no": document.refNo,
            "docId": document.docId,
            "status": document.status
        }

    except Exception as e:
        return {"error": str(e)}