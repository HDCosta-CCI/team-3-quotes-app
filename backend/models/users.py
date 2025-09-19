from database import Base
from sqlalchemy import TIMESTAMP, String, Column, Uuid
from datetime import datetime
import uuid

class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    status = Column(String(15), default="active")
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now(), onupdate=datetime.now())