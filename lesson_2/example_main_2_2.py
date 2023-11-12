from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# пример роута (маршрута)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get('/custom')
def read_custom_message():
    return {'message': "This is a custom message!"}


class User(BaseModel):
    username: str
    message: str


@app.post('/')
async def root(user: User):
    print(f'Мы получили от юзера {user.username} такое сообщение: {user.message}')
    return user
