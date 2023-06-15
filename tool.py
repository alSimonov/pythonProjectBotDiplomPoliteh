from aiogram import Bot, Dispatcher, types, executor
import sqlite3

from aiogram.dispatcher import FSMContext

import Connection
import storage
from conf import token
from aiogram.types import Message, InputFile, message, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot)


class Mydialog(StatesGroup):
    otvet = State()





def update_answers(userId, sql, totalQuestions):
    connect = Connection.connect()
    cursor = connect.cursor()

    result = len(storage.Options_answ) / totalQuestions
    params = (str(userId), ",".join(set(storage.Options_answ)), result)
    cursor.execute(sql, (params))


    connect.commit()
    cursor.close()
    connect.close()

    storage.Options_answ = []

#
# @dp.message_handler(state=Mydialog.otvet)
# async def process_message(message: types.Message, state: FSMContext):
#
#     async with state.proxy() as data:
#         data['text'] = message.text
#         user_message = data['text']
#
#         otvet_klienty = 'bla, bla, bla'
#
#         await bot.send_message(
#             message.from_user.id,
#             otvet_klienty,
#             parse_mode='HTML',
#         )
#
#
#     await state.finish()


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
