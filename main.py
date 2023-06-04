from conf import token
import but as kbs
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import CallbackQuery, InputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from tool import instr_question1_handler, instr_question2_handler, instr_question3_handler, instr_question4_handler, \
    structure_command

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot)

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

kb = ReplyKeyboardMarkup(resize_keyboard=True) #, one_time_keyboard=True

b1 = KeyboardButton('/help')
b2 = KeyboardButton('/description')
b3 = KeyboardButton('/photo')
kb.add(b1).insert(b2).insert(b3)


HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>старт бота</em>
<b>/description</b> - <em>описание бота</em>
<b>/photo</b> - <em>отправка нашего фото</em>
"""


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML") #, reply_markup=ReplyKeyboardRemove()
    await message.delete()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Добро пожаловать в наш бот",
                           parse_mode="HTML",
                           reply_markup=kb)
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


