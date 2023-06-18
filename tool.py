from aiogram import Bot, Dispatcher, types, executor

from aiogram.dispatcher import FSMContext

import Connection
import storage
from conf import token
from aiogram.types import Message, InputFile, message, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup

import asyncio
from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

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


def update_answers_program(userId, sqlOut , sql, totalQuestions):
    connect = Connection.connect()
    cursor = connect.cursor()

    str_temp = ""
    cursor.execute(sqlOut, userId)
    for row in cursor.fetchall():
        str_temp = str(row)[2: -3]

    lst_temp = str_temp.split(',')

    result = (len(storage.Options_answ) + len(lst_temp)) / totalQuestions
    params = (str(userId), ",".join(storage.Options_answ), result)
    cursor.execute(sql, (params))

    connect.commit()
    cursor.close()
    connect.close()

    storage.Options_answ = []


# async def delete_message(message: types.Message):
#     # await asyncio.sleep(sleep_time)
#     with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
#         await message.delete()


#
# async def instr_question1_handler(callback_query: CallbackQuery,
#                                   callback_data: dict):
#     answer = callback_data['answer']
#     if answer == 'b':
#         await callback_query.answer('Правильно!🎊')
#     else:
#         await callback_query.answer('Неправильно.🤔')
#
