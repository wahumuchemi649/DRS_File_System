from Documents.models import Documents as Document
from Config import SessionLocal

def get_documents_by_status(status: str):
    db = SessionLocal()
    try:
        documents = db.query(Document).filter(Document.status == status).all()

        if not documents:
            return {"message": f"No documents with status: {status}", "documents": []}

        docs_list = []
        for doc in documents:
            docs_list.append({
                "docId": doc.docId,
                "docType": doc.docType,
                "refNo": doc.refNo,
                "dateCreated": str(doc.dateCreated) if doc.dateCreated else None,
                "IsExternal": doc.IsExternal,
                "title": doc.title,
                "filePath": doc.filepath,
                "deptId": doc.deptId,
                "status": doc.status
            })

        return {"message": f"Documents with status: {status}", "documents": docs_list}

    except Exception as e:
        return {"error": str(e)}