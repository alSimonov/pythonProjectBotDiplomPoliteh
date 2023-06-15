import asyncio

from aiogram.dispatcher import FSMContext

import tool
import storage
from conf import token
import but as kbs
from asyncio import new_event_loop
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import CallbackQuery, InputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, PollAnswer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.types.poll import PollAnswer

from tool import instr_question1_handler, instr_question2_handler, instr_question3_handler, instr_question4_handler, \
    structure_command
import Connection

loop = new_event_loop()

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot=bot, loop=loop, storage=MemoryStorage())


# @dp.message_handler(commands=["start"])
# async def start_command(message: types.Message):
#     await bot.send_message(message.from_user.id, "Привет", reply_markup=kbs.menu_button)
#     await message.answer(f"текст", reply_markup=kbs.menu_keyboard)


@dp.message_handler(text='Меню')
async def process_menu_message(message: types.Message):
    if message.text.lower() == 'меню':
        await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_keyboard)


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
    await bot.send_message(message.from_user.id, f'Для полного фунционала, следует зарегистрироваться!',
                           reply_markup=kbs.reg_keyboard)
    # await message.answer(f"текст", reply_markup=kbs.menu_keyboard)
    await message.delete()


@dp.callback_query_handler(kbs.cb.filter(action='registr'))
async def choosing_role_command(message: types.Message):
    conn = Connection.connect()
    cursor = conn.cursor()

    listss = []
    cursor.execute("SELECT Id, LastName FROM Participant WHERE PersonID = ?", message.from_user.id)
    coincidence = len(cursor.fetchall())

    cursor.close()
    conn.close()

    if coincidence != 0:
        await bot.send_message(message.from_user.id, f'Этот пользователь уже зарегистрирован.')
        await bot.send_message(message.from_user.id, f'Вы желаете удалить аккаунт?',
                               reply_markup=kbs.delete_account_keyboard)
        return

    await bot.send_message(message.from_user.id, f'Выберите свою роль.', reply_markup=kbs.role_keyboard)
    # await message.delete()


@dp.callback_query_handler(kbs.cb.filter(action='deleteAccount'))
async def choosing_role_command(message: types.Message):
    if (storage.chh >= 3):
        await bot.send_message(message.from_user.id, 'Хватит это делать! Забаню')
        return
    storage.chh += 1

    await bot.send_message(message.from_user.id, 'В разработке')

    # TODO доделать удаление аккаунта (надо удалить записи по вопросам)

    #
    # conn = Connection.connect()
    # cursor = conn.cursor()
    #
    # cursor.execute("DELETE Participant WHERE PersonID = ?", message.from_user.id)
    #
    # cursor.commit()
    # cursor.close()
    # conn.close()
    #
    # await bot.send_message(message.from_user.id, 'Аккакунт удален')
    # await bot.send_message(message.from_user.id, f'Для полного фунционала, следует зарегистрироваться!',
    #                        reply_markup=kbs.reg_keyboard)


@dp.message_handler(state=tool.Mydialog.otvet)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text'].split()

        if len(user_message) != 3:
            await bot.send_message(message.from_user.id, 'Было распознано не 3 слова. Введите ФИО еще раз.')
            return

        storage.registr['patronymic'] = user_message.pop()
        storage.registr['firstname'] = user_message.pop()
        storage.registr['lastname'] = user_message.pop()

        otvet_klienty = f"Ваше ФИО: {storage.registr['lastname']}, {storage.registr['firstname']}, {storage.registr['patronymic']} \n" \
                        f"Ваша роль {('Руководитель', 'Студент')[storage.registr['role'] == 1]} \n" \
                        f"Все верно?"

        await bot.send_message(
            message.from_user.id,
            otvet_klienty,
            parse_mode='HTML',
            reply_markup=kbs.yesorno_registr_keyboard
        )
        # await message.delete()

    await state.finish()


@dp.callback_query_handler(kbs.cb.filter(action='ConfirmRegistr'))
async def confirm_registr_command(message: types.Message):
    conn = Connection.connect()
    cursor = conn.cursor()

    sql = "exec [dbo].[CreateParticipant] ?, ?, ?, ?, ?"
    params = (
        storage.registr['lastname'], storage.registr['firstname'], storage.registr['patronymic'], message.from_user.id,
        storage.registr['role']
    )
    cursor.execute(sql, (params))

    conn.commit()
    cursor.close()
    conn.close()

    await bot.send_message(message.from_user.id, 'Регистрация завершена', reply_markup=kbs.menu_keyboard)


@dp.callback_query_handler(kbs.cb.filter(action='roleStudent'))
async def select_role_student_command(message: types.Message):
    storage.registr['role'] = 1
    await bot.send_message(message.from_user.id, 'Выбран студент')
    await tool.Mydialog.otvet.set()
    await bot.send_message(message.from_user.id, f'Введите свое ФИО. (В одну строку через пробел.)')


@dp.callback_query_handler(kbs.cb.filter(action='roleRukov'))
async def select_role_rukov_command(message: types.Message):
    storage.registr['role'] = 2
    await bot.send_message(message.from_user.id, 'Выбран руководитель')
    await tool.Mydialog.otvet.set()
    await bot.send_message(message.from_user.id, f'Введите свое ФИО. (В одну строку через пробел.)')


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

    # TODO удалить метод по группам

    listss = []
    cursor.execute("SELECT Name FROM Groups")
    for row in cursor.fetchall():
        listss.append(str(row)[2:-3])

    cursor.close()
    connect.close()

    await bot.send_message(message.from_user.id, 'Группы', reply_markup=kbs.createButGroups(listss))
    await message.delete()


@dp.callback_query_handler(kbs.cb.filter(action='Введение'))
async def vvedenie_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Есть ли у вас введение?',
                           reply_markup=kbs.createButAnswersPz(1))


@dp.callback_query_handler(kbs.cb.filter(action='Аннотация'))
async def annotaion_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Что содержит ваша аннотация?',
                           reply_markup=kbs.createButAnswersPz(2))


@dp.callback_query_handler(kbs.cb.filter(action='Обзор предметной области'))
async def reviewsubarea_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Присутсвует ли в вашей работе обзор предметной области?',
                           reply_markup=kbs.createButAnswersPz(3))


@dp.callback_query_handler(kbs.cb.filter(action='Обзор аналогов'))
async def reviewanalog_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Содержится в вашем проекте обзор аналогов?',
                           reply_markup=kbs.createButAnswersPz(4))


@dp.callback_query_handler(kbs.cb.filter(action='Моделирование'))
async def modelir_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Ваша работа содержит моделирование?',
                           reply_markup=kbs.createButAnswersPz(5))


@dp.callback_query_handler(kbs.cb.filter(action='техническое задание'))
async def techzad_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Указано ли у вас техническое задание?',
                           reply_markup=kbs.createButAnswersPz(6))


@dp.callback_query_handler(kbs.cb.filter(action='архитектура программы'))
async def arhitectprogr_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Присутствует у вас разработка архитектуры программы?',
                           reply_markup=kbs.createButAnswersPz(7))


@dp.callback_query_handler(kbs.cb.filter(action='структуры данных'))
async def structuredata_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Включена ли в работу разработка структуры данных?',
                           reply_markup=kbs.createButAnswersPz(8))


@dp.callback_query_handler(kbs.cb.filter(action='пользовательский интерфейс'))
async def polinterf_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Присутствует у вас разработка архитектуры программы?',
                           reply_markup=kbs.createButAnswersPz(9))


# ----------------------------------------------------

@dp.callback_query_handler(kbs.cb.filter(action='обработка событий и ошибок'))
async def eventhandling_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Присутствует обработка событий и ошибок ввода данных?',
                           reply_markup=kbs.createButAnswersPz(10))


@dp.callback_query_handler(kbs.cb.filter(action='программный алгоритм'))
async def softwarealgorithm_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'У вас есть разработка программного алгоритма?',
                           reply_markup=kbs.createButAnswersPz(11))


@dp.callback_query_handler(kbs.cb.filter(action='интерфейс хранения данных'))
async def datastorageinterface_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Включена в работу организация интерфейса хранения данных?',
                           reply_markup=kbs.createButAnswersPz(12))


@dp.callback_query_handler(kbs.cb.filter(action='тестирование'))
async def testing_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Присутствует тестирование в вашей работе?',
                           reply_markup=kbs.createButAnswersPz(13))


@dp.callback_query_handler(kbs.cb.filter(action='руководство программиста'))
async def programmerguide_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Указано ли у вас руководство программиста?',
                           reply_markup=kbs.createButAnswersPz(14))


@dp.callback_query_handler(kbs.cb.filter(action='руководство оператора'))
async def operatormanual_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Есть ли руководство оператора?',
                           reply_markup=kbs.createButAnswersPz(15))


@dp.callback_query_handler(kbs.cb.filter(action='заключение'))
async def conclusion_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Не забыли про заключение?',
                           reply_markup=kbs.createButAnswersPz(16))


@dp.callback_query_handler(kbs.cb.filter(action='список литературы'))
async def listliterature_command(message: types.Message):
    storage.Options_answ = []
    await bot.send_message(message.from_user.id, f'Присутсвует список литературы?',
                           reply_markup=kbs.createButAnswersPz(17))


# --------------------------------------------------------------

# кнопки подтверждения

@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm1'))
async def listliterature_command(message: types.Message):
    connect = Connection.connect()
    cursor = connect.cursor()

    sql = "exec [dbo].[UpdateIntroduction] ?, ?"
    params = (message.from_user.id, True)
    cursor.execute(sql, (params))

    connect.commit()
    cursor.close()
    connect.close()


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm2'))
async def pzOptConfirm2_command(message: types.Message):
    sql = "exec [dbo].[UpdateAnnotation] ?, ?, ?"
    totalQuestions = 5
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm3'))
async def pzOptConfirm3_command(message: types.Message):
    sql = "exec [dbo].[UpdateSubjectAreaOverview] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm4'))
async def pzOptConfirm4_command(message: types.Message):
    sql = "exec [dbo].[UpdateOverviewOfAnalags] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm5'))
async def pzOptConfirm5_command(message: types.Message):
    sql = "exec [dbo].[UpdateModeling] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm6'))
async def pzOptConfirm6_command(message: types.Message):
    sql = "exec [dbo].[UpdateTechnicalSpecification] ?, ?, ?"
    totalQuestions = 5
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm7'))
async def pzOptConfirm7_command(message: types.Message):
    sql = "exec [dbo].[UpdateDevelopmentProgramArchitecture] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm8'))
async def pzOptConfirm8_command(message: types.Message):
    sql = "exec [dbo].[UpdateDataStructureDevelopment] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm9'))
async def pzOptConfirm9_command(message: types.Message):
    sql = "exec [dbo].[UpdateUserInterface] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm10'))
async def pzOptConfirm10_command(message: types.Message):
    sql = "exec [dbo].[UpdateHandlingEventsDataEntryErrors] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm11'))
async def pzOptConfirm11_command(message: types.Message):
    sql = "exec [dbo].[UpdateDevelopmentSoftwareAlgorithm] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm12'))
async def pzOptConfirm12_command(message: types.Message):
    sql = "exec [dbo].[UpdateOrganizationDataStorageInterface] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm13'))
async def pzOptConfirm13_command(message: types.Message):
    sql = "exec [dbo].[UpdateTesting]  ?, ?, ?"
    totalQuestions = 3
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm14'))
async def pzOptConfirm14_command(message: types.Message):
    sql = "exec [dbo].[UpdateProgrammerGuide] ?, ?, ?"
    totalQuestions = 3
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm15'))
async def pzOptConfirm15_command(message: types.Message):
    sql = "exec [dbo].[UpdateOperatorManual] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm16'))
async def pzOptConfirm16_command(message: types.Message):
    sql = "exec [dbo].[UpdateConclusion] ?, ?, ?"
    totalQuestions = 6
    tool.update_answers(message.from_user.id, sql, totalQuestions)


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm17'))
async def pzOptConfirm17_command(message: types.Message):
    sql = "exec [dbo].[UpdateListLiterature] ?, ?, ?"
    totalQuestions = 2
    tool.update_answers(message.from_user.id, sql, totalQuestions)


# ----------------------------------------------------------

# Добавление выбранных ответов

@dp.callback_query_handler(kbs.cb.filter(action='pzOpt1'))
async def pzopt1_command(message: types.Message):
    storage.Options_answ.append('1')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt2'))
async def pzopt2_command(message: types.Message):
    storage.Options_answ.append('2')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt3'))
async def pzopt3_command(message: types.Message):
    storage.Options_answ.append('3')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt4'))
async def pzopt4_command(message: types.Message):
    storage.Options_answ.append('4')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt5'))
async def pzopt5_command(message: types.Message):
    storage.Options_answ.append('5')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt6'))
async def pzopt6_command(message: types.Message):
    storage.Options_answ.append('6')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt7'))
async def pzopt7_command(message: types.Message):
    storage.Options_answ.append('7')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt8'))
async def pzopt8_command(message: types.Message):
    storage.Options_answ.append('8')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt9'))
async def pzopt9_command(message: types.Message):
    storage.Options_answ.append('9')


@dp.callback_query_handler(kbs.cb.filter(action='pz'))
async def pz_command(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Пояснительная записка:', reply_markup=kbs.createButPz())


@dp.message_handler(text='Меню')
async def process_menu_message(message: types.Message):
    if message.text.lower() == 'меню':
        await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_keyboard)


@dp.callback_query_handler(kbs.cb.filter(action='menu'))
async def process_menu_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_keyboard)


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
