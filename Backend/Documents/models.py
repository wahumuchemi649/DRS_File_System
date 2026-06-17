from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Config import Base

class Documents(Base):
    __tablename__ = "documents"  # ← fix: was "document"

    docId = Column(Integer, primary_key=True, autoincrement=True)  # ← DB generates it
    docType     = Column(String(20), nullable=False)
    refNo       = Column(String(20))
    dateCreated = Column(String(20))
    IsExternal  = Column(Boolean)
    title       = Column(String(20))
    filepath    = Column(String(255))
    deptId      = Column(String(20),ForeignKey('department.deptId'))
    department = relationship('Department',  back_populates='documents')
    report     = relationship('Report',      back_populates='document', uselist=False)
    notice     = relationship('Notice',      back_populates='document', uselist=False)
    discussion = relationship('Discussion',  back_populates='document', uselist=False)
    request    = relationship('Request',     back_populates='document', uselist=False)


class Report(Base):
    __tablename__ = 'reports'
    report       = Column(Integer, primary_key=True)
    docId        = Column(Integer, ForeignKey('documents.docId'))  # ← String to match parent
    creatorId    = Column(Integer)
    availability = Column(Integer)

    document = relationship('Documents', back_populates='report')  # ← 'Documents' not 'Document'


class Notice(Base):
    __tablename__ = 'notices'
    noticeId = Column(Integer, primary_key=True)
    docId    = Column(Integer, ForeignKey('documents.docId'))
    sender   = Column(Integer)
    subject  = Column(String(255))

    document = relationship('Documents', back_populates='notice')


class Discussion(Base):
    __tablename__ = 'discussions'
    discussions = Column(Integer, primary_key=True)
    docId       = Column(Integer, ForeignKey('documents.docId'))
    hostId      = Column(Integer)
    agenda      = Column(String(255))
    isDiscussed = Column(Integer)

    document = relationship('Documents', back_populates='discussion')


class Request(Base):
    __tablename__ = 'requests'
    requestId = Column(Integer, primary_key=True)
    docId     = Column(Integer, ForeignKey('documents.docId'))
    sender    = Column(Integer)
    receiver  = Column(Integer)
    status    = Column(String(20))

    document = relationship('Documents', back_populates='request')

    