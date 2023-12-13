from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': exc.detail}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'error': 'Interval server error'}
    )


@app.get('/items/{item_id}')
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomException(detail='Item not found', status_code=404)
    return {'item_id': item_id}


@app.get('/divide_by_zero')
async def divide_by_zero():
    """ Функция симулирует непредусмотренное исключение """
    result = 1 / 0
    return {'message': 'Могло быть норм'}
