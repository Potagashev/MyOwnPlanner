from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from datetime import datetime

from models import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    status = Column(String, default='inbox')  # inbox, planned, done
    created_at = Column(DateTime, default=datetime.now)
    priority = Column(String, nullable=True)
    category = Column(String, nullable=True)
    estimated_minutes = Column(Integer, nullable=True)
    ai_analyzed = Column(DateTime, nullable=True)
