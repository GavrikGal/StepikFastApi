from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

""" В уроке синхронное подключение к mySQL """

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Экземпляр БД, который будет зависимостью для эндпоинтов
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/todo/', response_model=schemas.ToDo)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


@app.get('/todo/{todo_id}', response_model=schemas.ToDo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail='ToDo not found')
    return db_todo


@app.put('/todo/', response_model=schemas.ToDo)
def update_todo(todo: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db=db, todo_id=todo.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail='ToDo not found')
    return crud.update_todo(db=db, todo=todo)


@app.delete('/todo/{todo_id}')
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail='ToDo not found')
    crud.delete_todo(db=db, todo_id=todo_id)
    return {'message': f'ToDo with id:{todo_id} has been deleted'}
