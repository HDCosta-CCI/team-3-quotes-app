from sqlalchemy import Column, Uuid, ForeignKey, Boolean
from sqlalchemy import Uuid
from uuid import uuid4
from connections.database import Base

class UserQuoteReactions(Base):
    __tablename__ = "user_quote_reactions"
    
    reaction_id = Column(Uuid, primary_key=True, default=uuid4, nullable=False)
    like = Column(Boolean, default=False)
    dislike = Column(Boolean, default=False)
    quote_id = Column(Uuid, ForeignKey("quotes.quote_id"), nullable=False)
    user_id = Column(Uuid, ForeignKey("users.user_id"), nullable=False)
