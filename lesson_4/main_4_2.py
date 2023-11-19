from datetime import datetime, timedelta


from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
import random


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = 'secretkey'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1


class User(BaseModel):
    username: str
    password: str


def authenticate_user(username: str, password: str) -> bool:
    """ Рандомная аутентификация пользователя """
    return random.choice([True, False])


def create_jwt_token(data: dict):
    """ Функция для создания JWT токена """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# роут для аутентификации, в уроке написано, что так делать не надо, это только для примера
@app.post('/login')
async def login(user_in: User):
    if authenticate_user(**user_in.model_dump()):
        return {'access_token': create_jwt_token({'sub': user_in.username}),
                'token_type': 'bearer'}
    return {'error': 'Invalid credentials'}


# защищенный роут (все проверки стоит выносить в отдельный метод, но так надо по заданию)
@app.get('/protected_resource')
async def protected_resource(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Получаем юзера и проверяем, что он декодировался
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Invalid token')

        # Получаем время жизни токена и проверяем, что он декодировался
        expire = payload.get('exp')
        if expire is None:
            raise jwt.DecodeError

        # Проверяем, что токен не устарел
        expire = datetime.fromtimestamp(expire)
        if expire < datetime.utcnow():
            raise jwt.ExpiredSignatureError

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired',
                            headers={'WWW-Authenticate': 'Bearer'})
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail='Invalid token', headers={'WWW-Authenticate': 'Bearer'})
    return {'message': 'got protected resource'}
