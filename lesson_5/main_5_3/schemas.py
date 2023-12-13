from typing import Union
from pydantic import BaseModel


# Базовая модель для наследования
class ToDoBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ToDoCreate(ToDoBase):
    ...


class ToDoUpdate(BaseModel):
    id: int
    completed: bool


class ToDo(ToDoBase):
    id: int
    completed: bool

    # Для связи с ORM
    class Config:
        from_attributes = True
