from Registry.models import Document
from Config import SessionLocal

def get_documents_by_status(status: str):
  db = SessionLocal()
  try:
    documents = db.query(Document).filter((Document.status == status)).all()
    if not documents:
      return{"message":f"No documents with status: {status}"}

    return{"message": f"Documents with status: {status}", "documents": documents}

    

  except Exception as e:
    return {"error": str(e)}

if __name__ == "__main__":
  approvedDocs = get_documents_by_status("Approved")
  print(approvedDocs)
