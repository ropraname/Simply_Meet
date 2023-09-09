import telebot
from telebot.types import *

from secret import tg_api_key
bot = telebot.TeleBot(tg_api_key)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # markup.add(KeyboardButton("Бебра", web_app=WebAppInfo("https://hackvds.gronics.ru/tgapp")))
    bot.reply_to(message, "Привет! Это Simple Meet Bot, который поможет тебе найти напарника для любых целей. Переходи в приложение и создавай запрос!")

bot.infinity_polling()