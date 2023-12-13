from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions.exception import CustomExceptionA, CustomExceptionB
from .exceptions.schemas import ErrorResponse

app = FastAPI()


@app.get('/items/{item_id}')
async def get_item(item_id: int):
    if item_id != 777:
        raise CustomExceptionA(status_code=404, detail='Item not found')
    return {'item_id': item_id}


@app.get('/server_error')
async def server_error():
    raise CustomExceptionB(status_code=501, detail='Some server error')


@app.exception_handler(CustomExceptionA)
async def custom_exception_handler_a(request: Request, exc: ErrorResponse):
    print(f'log exception: url=[{request.url}] -> exc=[{exc.status_code=}, {exc.detail=}]')
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': 'client error',
                 'error_detail': exc.detail}
    )


@app.exception_handler(CustomExceptionB)
async def custom_exception_handler_b(request: Request, exc: ErrorResponse):
    print(f'log exception: url=[{request.url}] -> exc=[{exc.status_code=}, {exc.detail=}]')
    return JSONResponse(
        status_code=500,
        content={'error': 'server error',
                 'error_detail': exc.detail}
    )
