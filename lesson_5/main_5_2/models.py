from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class ToDo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
