from fastapi import FastAPI, Cookie, Form, Response
from pydantic import BaseModel
from typing import Annotated
import random

app = FastAPI()

fake_db = [{'username': 'gal', 'password': '123'},
           {'username': 'another', 'password': '1234'}]

sessions = {}


class User(BaseModel):
    username: str
    password: str


def is_user_in_db(user: User):
    in_db = False
    for db_user in fake_db:
        if db_user['username'] == user.username and db_user['password'] == user.password:
            in_db = True
            break
    return in_db


@app.post('/login')
async def login(username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                response: Response):
    user = User(username=username, password=password)
    if is_user_in_db(user):
        sessions_id = str(random.randint(10000, 100000))
        sessions[sessions_id] = user
        response.set_cookie(key='session_token', value=sessions_id,
                            secure=True)
        return {'session_token': sessions_id}
    return {'message': 'user not found'}


@app.get('/user')
async def user(session_token=Cookie()):
    if session_token:
        user = sessions.get(session_token)
        return user
    return {"message": "Unauthorized"}