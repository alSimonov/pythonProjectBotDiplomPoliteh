from aiogram import Bot, Dispatcher, types, executor
import sqlite3
from conf import token
from aiogram.types import Message, InputFile, message, CallbackQuery

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot)


async def instr_question1_handler(callback_query: CallbackQuery,
                                  callback_data: dict):
    answer = callback_data['answer']
    if answer == 'b':
        await callback_query.answer('Правильно!🎊')
    else:
        await callback_query.answer('Неправильно.🤔')


async def instr_question2_handler(callback_query: CallbackQuery,
                                  callback_data: dict):
    answer = callback_data['answer']
    if answer == 'a':
        await callback_query.answer('Правильно!🎊')
    else:
        await callback_query.answer('Неправильно.🤔')


async def instr_question3_handler(callback_query: CallbackQuery,
                                  callback_data: dict):
    answer = callback_data['answer']
    if answer == 'b':
        await callback_query.answer('Правильно!🎊')
    else:
        await callback_query.answer('Неправильно.🤔')


async def instr_question4_handler(callback_query: CallbackQuery,
                                  callback_data: dict):
    answer = callback_data['answer']
    if answer == 'b':
        await callback_query.answer('Правильно!🎊')
    else:
        await callback_query.answer('Неправильно.🤔')


async def structure_command(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           'Наш колледж стремится к созданию <u>безопасной и уважительной среды</u> для <b>всех</b> ')
