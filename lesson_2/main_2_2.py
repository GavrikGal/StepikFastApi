from fastapi import FastAPI

from models_2_2 import User

app = FastAPI()

test_user = {
    'name': 'John Doe',
    'age': 1
}

test_user_obj = User(**test_user)


@app.get('/')
async def read_root():
    return {'message': 'Hello'}


@app.get('/users')
async def users():
    return test_user_obj


@app.post('/user')
async def user(user: User):
    adult = False
    if user.age >= 18:
        adult = True
    response = {
        'name': user.name,
        'age': user.age,
        'is_adult': adult
    }
    return response


@app.get('/{user_id}')
async def search_user_by_id(user_id: int):
    return {'Вы просили найти юзера с id': user_id}

