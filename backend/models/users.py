from connections.database import Base
from sqlalchemy import String, Column, Uuid
import uuid

class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(255), unique=True)
    password = Column(String(255))