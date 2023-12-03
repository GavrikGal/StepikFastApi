from sqlalchemy.orm import Session

from . import models, schemas


def get_todo(db: Session, todo_id: int):
    return db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.ToDoCreate):
    db_todo = models.ToDo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo: schemas.ToDoUpdate):
    db_todo = get_todo(db=db, todo_id=todo.id)
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db.query(models.ToDo).filter(models.ToDo.id == todo_id).delete()
    db.commit()
