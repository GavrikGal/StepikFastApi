from fastapi import FastAPI, Depends, status, HTTPException, Response
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
security = HTTPBasic()


class User(BaseModel):
    username: str
    password: str


DB = [User(**{"username": "user1", "password": "pass1"}),
      User(**{"username": "user2", "password": "pass2"})]


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials')
    return user


def get_user_from_db(username: str):
    for user in DB:
        if user.username == username:
            return user
        return None


@app.get('/login')
def get_protected_resource(user: User = Depends(authenticate_user)):
    response = Response(content="{'message': 'You got my secret, welcome'}")
    response.headers['WWW-Authenticate'] = 'Basic'
    return response
