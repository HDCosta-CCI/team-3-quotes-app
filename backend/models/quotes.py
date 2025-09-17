from sqlalchemy import Column, Integer, String, Uuid, ForeignKey
from sqlalchemy import Uuid
from uuid import uuid4
from connections.database import Base

class Quotes(Base):
    __tablename__ = "quotes"
    quotes_id = Column(Uuid, primary_key=True, default=uuid4, nullable=False)
    quote = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    like = Column(Integer, default=0)
    dislike = Column(Integer, default=0)
    tags = Column(String(255), nullable=True)
    user_id = Column(Uuid, ForeignKey("users.user_id"), nullable=False)
