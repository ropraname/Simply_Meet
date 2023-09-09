from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated
import db_states
import os
import base64
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Text_Query(BaseModel):
    tg_query_b64: str

templates = Jinja2Templates(directory="templates")

@app.get(f"/", response_class=HTMLResponse)
async def start_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

for path in os.listdir('templates'):
    @app.get(f"/{path}", response_class=HTMLResponse)
    async def page(request: Request):
        return templates.TemplateResponse(path, {"request": request})

@app.post(f"/page_body", response_class=HTMLResponse)
async def page_body(request: Request, tg_duery: Annotated[str, Form()]):
    init_data = json.loads(tg_duery)
    user_id = init_data['user']['id']
    return str(user_id)
    return templates.TemplateResponse(path, {"request": request})