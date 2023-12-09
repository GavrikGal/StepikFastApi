from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas
from .database import SessionLocal, create_all


app = FastAPI()


# Экземпляр БД, который будет зависимостью для эндпоинтов
# Dependency
async def get_db():
    async with SessionLocal() as db:
        yield db


@app.on_event('startup')
async def create_db():
    await create_all()


@app.post('/todo/', response_model=schemas.ToDo)
async def create_todo(todo: schemas.ToDoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_todo(db=db, todo=todo)


@app.get('/todo/{todo_id}', response_model=schemas.ToDo)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail='ToDo not found')
    return db_todo


@app.put('/todo/', response_model=schemas.ToDo)
async def update_todo(todo: schemas.ToDoUpdate, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.get_todo(db=db, todo_id=todo.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail='ToDo not found')
    return await crud.update_todo(db=db, todo=todo, db_todo=db_todo)


@app.delete('/todo/{todo_id}')
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail='ToDo not found')
    await crud.delete_todo(db=db, todo=db_todo)
    return {'message': f'ToDo with id:{todo_id} has been deleted'}