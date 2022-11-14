from typing import List

from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyHeader


app = FastAPI()
templates = Jinja2Templates(directory='../templates/')



@app.get('/little-pink')
def index_page(request: Request):
    print(f'---------- {request.body()} --------------')
    result = 'Type sentences'
    return templates.TemplateResponse('lp.html', context={'request':request, 'result':result})
