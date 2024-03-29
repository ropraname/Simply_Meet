from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated
import os
import base64
import json
from db_funcs import *

import telebot
from telebot.types import *

from secret import tg_api_key
bot = telebot.TeleBot(tg_api_key, parse_mode="MarkdownV2")

import starlette

dconf = json.loads(open("conf.json").read())

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Text_Query(BaseModel):
    tg_query_b64: str

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def start_page(request: Request, chat_id: int = 0, search_id: int = 0, intention: str = ""):
    if chat_id != 0:
        add_new_user(chat_id)
    index_page_intention(chat_id, search_id, intention)
    return templates.TemplateResponse("index.html", {"request": request})

def index_page_intention(chat_id, search_id, intention):
    match intention:
        case "accept_pair":
            finish_pairing(search_id, chat_id)
            set_page(chat_id, "end")
        case "decline_pair":
            decline_pairing(search_id, chat_id)
            set_page(chat_id, "end")

@app.post("/page_body", response_class=HTMLResponse)
async def page_body(request: Request):
    json_inp = await request.json()
    user_id = int(json_inp['tg_duery']['user']['id'])
    add_new_user(user_id)
    try:
        pair_id = get_intention(user_id)["current_pair_id"]
    except:
        pair_id = None
    return templates.TemplateResponse(get_page(user_id) + ".html", {"request": request, "dconf": dconf, "user_pair_id": pair_id, "events": get_events(), "pairs": get_finding_pairs(), "json": json, "set": set, "len": len})

@app.post("/start_interest_submit")
async def start_interest_submit(request: Request):
    json_inp = await request.json()
    user_id = int(json_inp['tg_duery']['user']['id'])
    interests = list(set(dconf['main_interests']).intersection(json_inp))
    put_interests(user_id, interests)
    set_page(user_id, "menu")
    return ""

@app.post("/create_new_events")
async def create_new_events(request: Request):
    json_inp = await request.json()
    user_id = int(json_inp['tg_duery']['user']['id'])
    print(json_inp)
    time_json = json.dumps([json_inp['time_start'].split("T"), json_inp['time_end'].split("T")], ensure_ascii=False)
    create_event(user_id, json_inp['general_topic'], json_inp['topic'], int(json_inp['people_amount']), time_json, json_inp['place'])
    set_page(user_id, "end")
    return ""

@app.post("/menu_select_{page}")
async def menu_select(request: Request, page):
    json_inp = await request.json()
    user_id = int(json_inp['tg_duery']['user']['id'])
    set_page(user_id, page)
    return ""

@app.post("/find_pair_start")
async def start_interest_submit(request: Request):
    json_inp = await request.json()
    user_id = int(json_inp['tg_duery']['user']['id'])
    pair_id = start_pairing(user_id, list(set(dconf['main_interests']).intersection(json_inp)))
    set_intention(user_id, {"current_pair_id": pair_id})
    set_page(user_id, "find_pair_way_select")
    return ""

@app.post("/find_pair_specify")
async def find_pair_specify(request: Request):
    json_inp = await request.json()
    user_id = int(json_inp['tg_duery']['user']['id'])
    pair_id = get_intention(user_id)["current_pair_id"]
    time_json = [json_inp['event_start'].split("T"), json_inp['event_end'].split("T")]
    time_json = json.dumps(time_json, ensure_ascii=False)
    place = json_inp['place']
    description = json_inp['description']
    supple_pairing(pair_id, time_json, place, description)
    set_page(user_id, "end")
    return ""

@app.post("/find_pair_list")
async def find_pair_list(request: Request):
    return ""

@app.post("/find_pair_connect")
async def find_pair_connect(request: Request):
    json_inp = await request.json()
    user_id = int(json_inp['tg_duery']['user']['id'])
    pair_id = json_inp["pair_id"]
    other_user_id = notify_about_pairing(pair_id, user_id)
    send_invite_to_user(other_user_id, user_id, pair_id)
    set_page(user_id, "end")
    return ""

def send_invite_to_user(to_id, from_id, pair_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard = True
    markup.add(InlineKeyboardButton("Принять", web_app=WebAppInfo(f"https://hackvds.gronics.ru/tgapp?chat_id={to_id}&search_id={pair_id}&intention=accept_pair")), InlineKeyboardButton("Отклонить", web_app=WebAppInfo(f"https://hackvds.gronics.ru/tgapp?chat_id={to_id}&search_id={pair_id}&intention=decline_pair")))
    bot.send_message(to_id, f"[Пользователь](tg://user?id={from_id}) хочет составить вам компанию", reply_markup=markup)

@app.get("/accept_pair")
async def accept_pair(request: Request):
    json_inp = await request.json()
    user_id = int(json_inp['tg_duery']['user']['id'])
    pair_id = json_inp["pair_id"]
    other_user_id = notify_about_pairing(pair_id, user_id)
    send_invite_to_user(other_user_id, user_id)
    set_page(user_id, "end")
    return ""