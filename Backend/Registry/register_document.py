from Registry.models import Document
from Config import SessionLocal

def register_document(document:Document):
  db = SessionLocal()
  try:
    count = db.query(Document).count()
    ref_no = f"REF-{count + 1:04d}" #generate ref no e.g REF-0001...

    #NEW DOCUMENT OBJECT
    new_document = Document(
      refNo=ref_no,
      docType=document.docType,
      dateCreated=document.dateCreated,
      IsExternal=document.IsExternal,
      title=document.title,
      filepath=document.filepath,
      deptId=document.deptId,
      status="Registered"
      
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {"message": "Document registered successfully", "ref_no": new_document.refNo}

  except Exception as e:
      return {"error": str(e)}

if __name__ == "__main__":
    test_doc = Document(
        docId=999,
        docType="Report",
        IsExternal=False,
        title="Budget Report",
        filePath="/files/budget.pdf",
        deptId=None
    )

    result = register_document(test_doc)
    print(result)