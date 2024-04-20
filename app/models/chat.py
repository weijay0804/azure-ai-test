from datetime import datetime

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, String, Text, func, DateTime, Integer, ForeignKey

from app.config.database import Base


class ChatSession(Base):
    '''`chat_session` table ORM model'''

    __tablename__ = "chat_session"

    id = Column(String(36), primary_key=True)
    update_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now())
    create_at = Column(DateTime, nullable=False, server_default=func.now())

    # 建立與 chat_message table 的一對多關係
    chat_messages = relationship("ChatMessage", back_populates="chat_session", lazy="dynamic")


class ChatRole(Base):
    '''`chat_role` table ORM model'''

    __tablename__ = "chat_role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(20), nullable=False, unique=True)
    update_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now())
    create_at = Column(DateTime, nullable=False, server_default=func.now())

    # 建立與 chat_message table 的一對多關係
    chat_messages = relationship("ChatMessage", back_populates="chat_role")


class ChatMessage(Base):
    '''`chat_message` table ORM model'''

    __tablename__ = "chat_message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = mapped_column(ForeignKey('chat_session.id'))
    role_id = mapped_column(ForeignKey('chat_role.id'))
    message = Column(Text, nullable=False)
    update_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now())
    create_at = Column(DateTime, nullable=False, server_default=func.now())

    chat_session = relationship("ChatSession", back_populates="chat_messages")
    chat_role = relationship("ChatRole", back_populates="chat_messages")
