from conf import token
import but as kbs
from asyncio import new_event_loop
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import CallbackQuery, InputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types.poll import PollAnswer

from tool import instr_question1_handler, instr_question2_handler, instr_question3_handler, instr_question4_handler, \
    structure_command
import Connection

loop = new_event_loop()

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot=bot, loop=loop)


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(text=message.text)


# @dp.message_handler(commands=["start"])
# async def start_command(message: types.Message):
#     await bot.send_message(message.from_user.id, "Привет", reply_markup=kbs.menu_button)
#     await message.answer(f"текст", reply_markup=kbs.menu_keyboard)


@dp.message_handler(text='Меню')
async def process_menu_message(message: types.Message):
    if message.text.lower() == 'меню':
        await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_keyboard)


@dp.callback_query_handler(lambda x: x.data == 'history_but')
async def instr_command(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Ответьте на вопросы теста:')

    # Отправляем первый вопрос
    await bot.send_message(callback_query.from_user.id, 'Какое событие привело к <b>началу</b> Первой мировой войны?⚔',
                           reply_markup=kbs.question1_buttons)


@dp.callback_query_handler(kbs.question1_cb.filter())
async def question1_handler(callback_query: CallbackQuery, callback_data: dict):
    answer = callback_data['answer']
    while answer != 'b':
        await callback_query.answer('Неправильно🤔.')
    await callback_query.answer('Правильно👍!')
    # Отправляем второй вопрос
    await callback_query.message.answer('В каком году произошла Революция во <b>Франции</b>?',
                                        reply_markup=kbs.question2_buttons)


@dp.callback_query_handler(kbs.question2_cb.filter())
async def question2_handler(callback_query: CallbackQuery, callback_data:
dict):
    answer = callback_data['answer']
    while answer != 'a':
        await callback_query.answer('Неправильно🤔.')
    await callback_query.answer('Правильно👍!')
    # Отправляем третий вопрос
    await callback_query.message.answer('Кто был <b>первым</b> президентом Российской Федерации?',
                                        reply_markup=kbs.question3_buttons)


@dp.callback_query_handler(kbs.question3_cb.filter())
async def question3_handler(callback_query: CallbackQuery, callback_data: dict):
    answer = callback_data['answer']
    while answer != 'b':
        await callback_query.answer('Неправильно🤔.')
    await callback_query.answer('Правильно👍!')
    # Отправляем четвертый вопрос
    await callback_query.message.answer('В каком году произошла Октябрьская революция в России?',
                                        reply_markup=kbs.question4_buttons)


@dp.callback_query_handler(kbs.question4_cb.filter())
async def question4_handler(callback_query: CallbackQuery, callback_data: dict):
    answer = callback_data['answer']
    while answer != 'b':
        await callback_query.answer('Неправильно🤔.')
    await callback_query.answer('Правильно👍!')
    # Завершаем тест
    await callback_query.message.answer('Тест окончен🎉🎊. Спасибо за участие!👍')
    await bot.send_sticker(chat_id=callback_query.from_user.id,
                           sticker=r"CAACAgIAAxkBAAEI3U1kVQZGtdksjFg9CH636ma1ogc_XQACEBoAAocnIEjsWiTwN9NJuy8E")


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

kb = ReplyKeyboardMarkup(resize_keyboard=True)  # , one_time_keyboard=True

b1 = KeyboardButton('/help')
b2 = KeyboardButton('/description')
b3 = KeyboardButton('/photo')
kb.add(b1).insert(b2).insert(b3)

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>старт бота</em>
<b>/description</b> - <em>описание бота</em>

<b>/menu</b> - <em>меню бота</em>
<b>/groups</b> - <em>описание бота</em>

<b>/photo</b> - <em>отправка нашего фото</em>
"""


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML")  # , reply_markup=ReplyKeyboardRemove()
    await message.delete()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # await bot.send_message(chat_id=message.from_user.id,
    #                        text="Добро пожаловать в наш бот",
    #                        parse_mode="HTML",
    #                        reply_markup=kb)
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.full_name}', reply_markup=kbs.menu_button)
    # await message.answer(f"текст", reply_markup=kbs.menu_keyboard)
    await message.delete()


@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Наш бот умеет отправлять фотографии",
                           parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands=['photo'])
async def photo_command(message: types.Message):
    await bot.send_photo(message.from_user.id,
                         photo='https://oir.mobi/uploads/posts/2022-09/1662322342_1-oir-mobi-p-uporotaya-sova-vkontakte-1.jpg')
    await message.delete()


@dp.message_handler(commands=['groups'])
async def group_command(message: types.Message):
    connect = Connection.connect()
    cursor = connect.cursor()

    listss = []
    cursor.execute("SELECT Name FROM Groups")
    for row in cursor.fetchall():
        listss.append(str(row)[2:-3])

    cursor.close()
    connect.close()

    await bot.send_message(message.from_user.id, 'Группы', reply_markup=kbs.createButGroups(listss))
    await message.delete()


@dp.callback_query_handler(kbs.cb.filter(action='Аннотация'))
async def annotaion_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Что содержит ваша аннотация?',
                        options=['цель',
                                 'задачи',
                                 'требования',
                                 'технологии и платформа',
                                 'описание разделов'],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='Обзор предметной области'))
async def reviewsubarea_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Присутсвует ли в вашей работе обзор предметной области?',
                        options=['обзор предметной области?', 'содержит ли он ссылки на авторов?'],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='Обзор аналогов'))
async def reviewanalog_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Содержится в вашем проекте обзор аналогов?',
                        options=['Включает ли он необходимое количество аналогов?',
                                 'Присутствуют ли у вас недостатки аналогов?'],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='Моделирование'))
async def modelir_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Ваша работа содержит моделирование?',
                        options=['У вас присутствует схема?',
                                 'Есть ли у вас описание элементов?'],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='техническое задание'))
async def techzad_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Указано ли у вас техническое задание?',
                        options=['Содержатся требования к составу выполняемых функций?',
                                 'Имеются требования к входным и выходным данным?',
                                 'Содержатся требования к пользовательскому интерфейсу?',
                                 'Включаеются ли требования к информационной и программной совместимости?',
                                 'Прописаны этапы разработки?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='архитектура программы'))
async def arhitectprogr_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Присутствует у вас разработка архитектуры программы?',
                        options=['У вас присутствует схема?',
                                 'Есть ли у вас описание элементов?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='структуры данных'))
async def structuredata_command(call: CallbackQuery):
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Включена ли в работу разработка структуры данных?',
                        options=['У вас присутствует схема?',
                                 'Есть ли у вас описание элементов?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)
    await call.answer(cache_time=10)


@dp.callback_query_handler(kbs.cb.filter(action='пользовательский интерфейс'))
async def polinterf_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Присутствует у вас разработка архитектуры программы?',
                        options=['У вас присутствует схема?',
                                 'Есть ли у вас описание элементов?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='pz'))
async def pz_command(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Пояснительная записка:', reply_markup=kbs.createButPz())


@dp.message_handler(text='Меню')
async def process_menu_message(message: types.Message):
    if message.text.lower() == 'меню':
        await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_keyboard)


# @dp.callback_query_handler(kbs.cb.filter(action='pz'))
# async def pz_command(call: CallbackQuery):
#     await call.answer(cache_time=10)
#     await bot.send_poll(chat_id=call.message.chat.id,
#                         question='Что содержит ваша аннотация?',
#                         options=['цель',
#                                  'задачи',
#                                  'требования',
#                                  'технологии и платформа',
#                                  'описание разделов'],
#                         is_anonymous=False,
#                         allows_multiple_answers=True)


@dp.poll_answer_handler()
async def handle_poll_answer(poll: PollAnswer):
    connect = Connection.connect()
    cursor = connect.cursor()
    interests = str(poll['option_ids'])
    user_id = poll['user']['id']

    cursor.execute("""INSERT INTO [Groups](Name) VALUES(?) """, [interests])

    cursor.close()
    connect.commit()
    connect.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
