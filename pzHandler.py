from conf import token
import but as kbs
from asyncio import new_event_loop
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import CallbackQuery, InputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, PollAnswer
import main
import Connection

bot = main.bot
dp = main.dp

