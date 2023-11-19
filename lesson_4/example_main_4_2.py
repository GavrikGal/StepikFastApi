from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# Пример информации из БД
USERS_DATA = [
    {"username": "admin", "password": "adminpass"}
]


class User(BaseModel):
    username: str
    password: str


def create_jwt_token(data: dict):
    """ Функция для создания JWT токена """
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    """ Функция получения User'a по токену """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        ...
    except jwt.InvalidTokenError:
        ...


def get_user(username: str):
    """ Получение пользовательских данных на основе имени пользователя """
    for user in USERS_DATA:
        if user.get('username') == username:
            return user
    return None


# роут для аутентификации; так делать не нужно, это для примера
@app.post('/login')
async def login(user_in: User):
    for user in USERS_DATA:
        if user.get('username') == user_in.username and user.get('password') == user_in.password:
            return {'access_token': create_jwt_token({'sub': user_in.username}),
                    'token_type': 'bearer'}
        return {'error': 'Invalid credentials'}


# защищенный роут для получения информации о пользователе
@app.get('/about_me')
async def about_me(current_user: str = Depends(get_user_from_token)):
    user = get_user(current_user)
    if user:
        return user
    return {'error': 'User not found'}
