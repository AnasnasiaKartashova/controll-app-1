import random
from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query
from pymysql import IntegrityError
from sqlalchemy.orm import Session

from src.database_connection import get_db
from src.models.test_level.level_model import Level
from src.models.test_level.level_schema import LevelSchema

router_level_test = APIRouter(prefix="/level-test", tags=['level-test'])


@router_level_test.get("/questions/")
def get_questions(page: int = Query(1, ge=1), page_size: int = Query(5, ge=1), db: Session = Depends(get_db)):
    questions = db.query(Level).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Questions not found")
    start = (page - 1) * page_size
    end = start + page_size
    questions = questions[start:end]
    response = []
    for question in questions:
        response.append({
            "question": question.question,
            "media_file_id": question.media_file_id,
            "answers": list(question.answer.values())
        })
        random.shuffle(response[-1]["answers"])
        response[-1]["answers"] = {key: response[-1]["answers"].pop() for key in sorted(question.answer.keys())}

    return {"questions": response}


@router_level_test.post("/question/result")
def check_answers(answers: List[int], db: Session = Depends(get_db)):
    questions = db.query(Level).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Questions not found")
    num_correct = 0
    for i, question in enumerate(questions):
        correct_answer = list(question.answer.keys())[0]
        if answers[i] == int(correct_answer[-1]):
            num_correct += 1
            if 5 < num_correct <= 25:
                result = f"Вы набрали {num_correct} из {len(questions)} баллов, ваш уровень А1"
            elif 25 < num_correct <= 45:
                result = f"Вы набрали {num_correct} из {len(questions)} баллов, ваш уровень А2"
            elif 45 < num_correct <= 65:
                result = f"Вы набрали {num_correct} из {len(questions)} баллов, ваш уровень B1"
            elif 65 < num_correct <= 85:
                result = f"Вы набрали {num_correct} из {len(questions)} баллов, ваш уровень B2"
            elif 85 < num_correct <= 105:
                result = f"Вы набрали {num_correct} из {len(questions)} баллов, ваш уровень C1"
            elif 105 < num_correct <= 113:
                result = f"Вы набрали {num_correct} из {len(questions)} баллов, ваш уровень C2"
            else:
                result = f"Вы набрали {num_correct} из {len(questions)} баллов, ваш уровень A0"
    return {"result": result}


@router_level_test.post("/add-question/")
def post_question(qwestion_add: LevelSchema, db: Session = Depends(get_db)):
    new_qwestion = Level(section_name=qwestion_add.section_name,
                    question=qwestion_add.question,
                    answer=qwestion_add.answer)

    try:
        db.add(new_qwestion)
        db.commit()
        db.refresh(new_qwestion)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Question already exists")

    return {"message": "Created question"}


@router_level_test.patch("/update-question/{question_id}")
def update_question(id: int, qwestion: LevelSchema, db: Session = Depends(get_db)):
    up_question = db.query(Level).filter(Level.id == id).first()
    if not up_question:
        raise HTTPException(status_code=404, detail="Question not found")
    up_question.section_name = qwestion.section_name
    up_question.question = qwestion.question
    up_question.answer = qwestion.answer
    db.commit()
    return {"message": "Question updated"}


@router_level_test.delete("/delete-question/{question_id}")
def delete_question(id: int, db: Session = Depends(get_db)):
    del_question = db.query(Level).filter(Level.id == id).first()
    if not del_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(del_question)
    db.commit()
    return {"message": "Question deleted"}
