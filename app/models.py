from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text, ForeignKey
from .database import Base

class Post(Base):
   __tablename__ = 'posts'
   id = Column(Integer, primary_key=True, nullable=False)
   title = Column(String, nullable=False)
   content = Column(String, nullable=False)
   published = Column(Boolean, server_default='TRUE')
   created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
   user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
   username = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False)

class User(Base):
   __tablename__ = 'users'
   id = Column(Integer, primary_key=True, nullable=False)
   email = Column(String, unique=True, nullable=False)
   password = Column (String, nullable=False)
   username = Column(String, unique=True, nullable=False)
   created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Like(Base):
   __tablename__ = 'likes'
   user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
   post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
   like_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))