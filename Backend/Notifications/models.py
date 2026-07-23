from sqlalchemy import Column, Integer, String, Text, Boolean, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Config import Base


class Notification(Base):
    __tablename__ = "notifications"

    notificationId = Column(Integer, primary_key=True, autoincrement=True)

    docId = Column(Integer, ForeignKey("documents.docId"), nullable=False)
    deptId = Column(String(20), ForeignKey("department.deptId"), nullable=False)

    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)

    priority = Column(
        Enum("Normal", "Warning", "Urgent"),
        default="Normal"
    )

    isRead = Column(Boolean, default=False)

    createdAt = Column(TIMESTAMP, server_default=func.now())

    document = relationship("Documents", backref="notifications")
    department = relationship("Department", backref="notifications")