from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)

    uploads = relationship("Upload", back_populates="user")


class Upload(Base):
    __tablename__ = 'uploads'

    id = Column(Integer, primary_key=True)
    uid = Column(String, default=str(uuid.uuid4()))  # Use String type
    filename = Column(String)
    upload_time = Column(DateTime)
    finish_time = Column(DateTime, nullable=True)  # Make it nullable for now
    status = Column(String, default='uploaded')  # Set default status as 'uploaded'
    user_id = Column(Integer, ForeignKey('users.id'))
    pptx_explanation = Column(String)  # New column for storing pptx explanation

    user = relationship("User", back_populates="uploads")


engine = create_engine('sqlite:///sqlalchemy_db.db')

Session = sessionmaker(bind=engine)

session = Session()

Base.metadata.create_all(engine)
