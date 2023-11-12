from typing import Annotated
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
import re


app = FastAPI()


@app.get('/items/')
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {'X-Token values': x_token}


def check_headers(headers: Request.headers):
    if 'User-Agent' not in headers:
        raise HTTPException(status_code=400, detail="Header User-Agent not found")
    if 'Accept-Language' not in headers:
        raise HTTPException(status_code=400, detail="Header Accept-Language not found")

    pattern = r"(?i:(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?,)+(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?"

    if not re.fullmatch(pattern, headers['Accept-Language']):
        raise HTTPException(status_code=400, detail="Header Accept-Language has not correct format")


@app.get('/headers')
async def get_headers(request: Request):
    check_headers(request.headers)
    content = {'user-agent': request.headers['user-agent'],
               'accept-language': request.headers['accept-language']}
    response = JSONResponse(content=content)
    return response
