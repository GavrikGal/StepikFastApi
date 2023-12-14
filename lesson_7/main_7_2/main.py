from fastapi import FastAPI, Depends
from typing import Annotated

from .servises import some_logic


app = FastAPI()


db = [{'username': 'user1', 'password': 'pass1'},
      {'username': 'user2', 'password': 'pass2'}]


def get_db():
    return db


@app.get('/users/{username}')
def get_user(username: str, db: Annotated[dict, Depends(get_db)]):
    for user in db:
        if user['username'] == username:
            return {'username': username, 'password': user['password']}
    return {'message': 'user not found'}


@app.get('/logic')
def do_with_some_logic(a: int, b: int):
    result = some_logic(a, b)
    return {'result': result}
