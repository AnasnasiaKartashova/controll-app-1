from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database_connection import get_db
from src.models.lessons.lesson_model import Lesson
from src.models.user_status.status_model import UserStatus

router_user_status = APIRouter(prefix="/user-status", tags=['user-status'])


@router_user_status.get("/last-lesson/{user_id}")
def get_last_lesson(user_id: int, db: Session = Depends(get_db)):
    user_status = db.query(UserStatus).filter(UserStatus.user_id == user_id).order_by(UserStatus.lesson_id.desc()).first()
    if user_status:
        lesson = db.query(Lesson).filter(Lesson.id == user_status.lesson_id).first()
        return f'Вы остановились на теме {lesson.topic_name}. Хотите продолжить обучение?'
    else:
        return {"last_lesson": None}
