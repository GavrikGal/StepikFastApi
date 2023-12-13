from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator


app = FastAPI()


async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': 'Custom Unprocessable Entity Error'},
    )


async def custom_request_validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={'message': 'Custom Request Validation Error', 'error': jsonable_encoder(exc.errors())},
    )


app.add_exception_handler(HTTPException,
                          custom_http_exception_handler)
app.add_exception_handler(RequestValidationError,
                          custom_request_validation_exception_handler)


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    @field_validator('price')
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Price must be non-negative')
        return value


@app.post('/items')
async def create_item(item: Item):
    return {'message': 'Item created successfully', 'item': item}