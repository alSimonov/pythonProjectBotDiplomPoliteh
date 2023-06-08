import asyncio

from conf import token
import but as kbs
from asyncio import new_event_loop
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import CallbackQuery, InputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, PollAnswer
# from aiogram.types.poll import PollAnswer

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
    await bot.send_message(message.from_user.id, f'Для полного фунционала, следует зарегестрироваться!',
                           reply_markup=kbs.reg_keyboard)
    # await message.answer(f"текст", reply_markup=kbs.menu_keyboard)
    await message.delete()




@dp.callback_query_handler(kbs.cb.filter(action='registr'))
async def vvedenie_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Выберите роль',
                        options=['Студент',
                                 'Дипломный руководитель',
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=False)


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


@dp.callback_query_handler(kbs.cb.filter(action='Введение'))
async def vvedenie_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='000 Есть ли у вас введение?',
                        options=['Да',
                                 'Нет',
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='Аннотация'))
async def annotaion_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='001 Что содержит ваша аннотация?',
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
    poll = await bot.send_poll(chat_id=call.message.chat.id,
                        question='002 Присутсвует ли в вашей работе обзор предметной области?',
                        options=['обзор предметной области?', 'содержит ли он ссылки на авторов?'],
                        is_anonymous=False,
                        allows_multiple_answers=True)
    await asyncio.sleep(20)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=poll.message_id)

@dp.callback_query_handler(kbs.cb.filter(action='003 Обзор аналогов'))
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
                                 'Имеются требования к входным и выходным данным?(данные должны быть корректны,не менее 5-10 записей)',
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
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Включена ли в работу разработка структуры данных?',
                        options=['У вас присутствует схема?',
                                 'Есть ли у вас описание элементов?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


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


# ----------------------------------------------------

@dp.callback_query_handler(kbs.cb.filter(action='обработка событий и ошибок'))
async def eventhandling_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Присутствует обработка событий и ошибок ввода данных?',
                        options=['События обработаны?',
                                 'Указаны спецификации обработчиков?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='программный алгоритм'))
async def softwarealgorithm_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='У вас есть разработка программного алгоритма?',
                        options=['Алгоритм разработан?',
                                 'Содержатся спецификации функций или функциональных элементов?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='интерфейс хранения данных'))
async def datastorageinterface_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Включена в работу организация интерфейса хранения данных?',
                        options=['Интерфейс разработан?',
                                 'Присутствуют спецификации процедур или операций чтения-записи?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='тестирование'))
async def testing_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Присутствует тестирование в вашей работе?',
                        options=['Указаны примеры проверки в нормальных условиях?',
                                 'Показаны примеры проверки в экстремальных условиях?'
                                 'Указаны примеры проверки в исключительных условиях?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='руководство программиста'))
async def programmerguide_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Указано ли у вас руководство программиста?',
                        options=['Указаны характеристики?',
                                 'Написано, какие входные и выходные данные?(данные должны быть корректны,не менее 5-10 записей)',
                                 'Содержится настройка программы?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='руководство оператора'))
async def operatormanual_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Есть ли руководство оператора?',
                        options=['Рукводство функционально?',
                                 'Написано сообщения оператору?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='заключение'))
async def conclusion_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Не забыли про заключение?',
                        options=['Соотвествует ли результат работы поставленным целям?',
                                 'В результате работы были выполнены поставленные задачи?',
                                 'Были ли соблюдены требования при выполнении работы?',
                                 'Результат содержит технологии и платформу?',
                                 'Вы указали описание разделов в результате проделанной работы?',
                                 'Вы уточнили внедрение и/или ожидаемый эффект?'
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='список литературы'))
async def listliterature_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Присутсвует список литературы?',
                        options=['Количество источников соотвествует требованиям?',
                                 'Есть ли соответствие ГОСТу?'
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


@dp.poll_answer_handler()
async def handle_poll_answer(poll: PollAnswer):


    # обработка ответа пользователя
    await bot.send_message(poll.user.id, "Спасибо за ответ!")
    # удаление опроса


    connect = Connection.connect()
    cursor = connect.cursor()
    interests = str(poll['option_ids'])
    user_id = poll['user']['id']

    cursor.execute("""INSERT INTO [Groups](Name) VALUES(?) """, [interests])

    cursor.close()
    connect.commit()
    connect.close()


# --------------------------------------------------------------------------------


@dp.callback_query_handler(kbs.cb.filter(action='program'))
async def po_command(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Программа:', reply_markup=kbs.program_keyboard)
    # await bot.send_message(call.message.chat.id, 'Программа:', reply_markup=kbs.createButAnswers())


@dp.callback_query_handler(kbs.cb.filter(action='programCh1'))
async def po_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Что есть в вашей программе? Часть 1',
                        options=['Запускается ли ваше ПО?',
                                 'Соответствует программа ТЗ?',
                                 'В вашем программном обеспечении есть схема данных?',
                                 'Авторизация присутствует в вашем ПО?',
                                 'Содержит ли ПО следующие осн функции: фильтр, расч. и др?',
                                 'Включена в вашей ПО обработка ошибок?',
                                 ],
                        is_anonymous=False,
                        allows_multiple_answers=True)


@dp.callback_query_handler(kbs.cb.filter(action='programCh2'))
async def po_command(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(chat_id=call.message.chat.id,
                        question='Что есть в вашей программе? Часть 2',
                        options=[
                            'Присутствует русификация в вашем проекте?',
                            'Вы указали справку в вашем ПО?',
                            'Присутствует ли заполнение данными?',
                            'Содержатся отчеты?',
                            'Включено ли журналирование и другие дополнительные функции?',
                            'Ваша программа содержит дружелюбный интерфейс?'
                        ],
                        is_anonymous=False,
                        allows_multiple_answers=True)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
