from src.database_connection import Base
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from datetime import datetime


class UserStatus(Base):
    __tablename__ = 'user_status'

    user_id = Column(Integer, ForeignKey("user.id"), unique=True, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lesson.id"), unique=True)
    last_lesson = Column(String(255))


    # test_topic_id = Column(Integer, ForeignKey("test_topic.id"), unique=True)
    # numbers_of_test_topic = Column(String(255))
    # days = Column(String(255))