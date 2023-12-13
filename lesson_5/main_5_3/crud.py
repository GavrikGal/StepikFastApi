from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_todo(db: AsyncSession, todo_id: int):
    return await db.get_one(models.ToDo, todo_id)


async def create_todo(db: AsyncSession, todo: schemas.ToDoCreate):
    db_todo = models.ToDo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def update_todo(db: AsyncSession, todo: schemas.ToDoUpdate, db_todo: models.ToDo):
    db_todo.completed = todo.completed
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def delete_todo(db: AsyncSession, todo: models.ToDo):
    await db.delete(todo)
    await db.commit()
