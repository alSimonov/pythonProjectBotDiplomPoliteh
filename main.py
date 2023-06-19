from aiogram.dispatcher import FSMContext
import random
import tool
import storage
from conf import token
import but as kbs
from asyncio import new_event_loop
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import CallbackQuery, InputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, PollAnswer
from aiogram.contrib.fsm_storage.memory import MemoryStorage


import Connection

loop = new_event_loop()

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot=bot, loop=loop, storage=MemoryStorage())

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

    conn = Connection.connect()
    cursor = conn.cursor()

    sql = "exec [dbo].[DropRecord] ? "
    params = message.from_user.id
    cursor.execute(sql, (params))

    cursor.commit()
    cursor.close()
    conn.close()

    await bot.send_message(message.from_user.id, 'Аккакунт удален')
    await bot.send_message(message.from_user.id, f'Для полного фунционала, следует зарегистрироваться!',
                           reply_markup=kbs.reg_keyboard)


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

    keyboard = (kbs.menu_keyboard, kbs.menu_forRukov_keyboard)[storage.registr['role'] == 2]

    await bot.send_message(message.from_user.id, 'Регистрация завершена', reply_markup=keyboard)


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


# ------------------------------------------------------------------------------

@dp.callback_query_handler(kbs.cb.filter(action='rukovUpdate'))
async def updateRukov_command(message: types.Message):

    currentRuk = ''

    conn = Connection.connect()
    cursor = conn.cursor()

    str_temp = ""
    cursor.execute("exec [dbo].[GetCurrentSuperviser] ?", message.from_user.id)
    for row in cursor.fetchall():
        str_temp = str(row)[1:-1].replace("'", "").replace(" ", "").split(",")
        n_str_temp = f'{str_temp[0]} {str_temp[1][0]}. {str_temp[2][0]}.'
        currentRuk = n_str_temp

    cursor.close()
    conn.close()



    currentRukStr = (currentRuk, 'не указан')[currentRuk == '']
    await bot.send_message(message.from_user.id, f'Ваш текущий дипломный руководитель: \n{currentRukStr}',
                           reply_markup=kbs.rukov_update_keyboard)


@dp.callback_query_handler(kbs.cb.filter(action='getRukov'))
async def getRukov_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Выберите своего дипломного руководителя.',
                           reply_markup=kbs.createButRukov())


@dp.callback_query_handler(kbs.cb.filter(action='rukovOptConfirm'))
async def confirmRukov_command(message: types.Message):
    temp = int(storage.Options_answ[message.from_user.id][-1]) - 1
    idSuperviser = int(storage.lst_rukov[temp][0])


    connect = Connection.connect()
    cursor = connect.cursor()

    sql = "exec [dbo].[UpdateStudendtSuperviser] ?, ?"
    params = (message.from_user.id, idSuperviser)
    cursor.execute(sql, (params))

    connect.commit()
    cursor.close()
    connect.close()

    await bot.send_message(message.from_user.id, f'Вашим дипломным руководителем выбран:\n{storage.lst_rukov[temp][1]}')


# ------------------------------------------------------------------------------


# ПЗ Вывод вопросов

# ------------------------------------------------------------------------------

@dp.callback_query_handler(kbs.cb.filter(action='Введение'))
async def vvedenie_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = None
    await bot.send_message(message.from_user.id, f'Есть ли у вас введение?',
                           reply_markup=kbs.Introduction_keyboard)
    # await bot.delete_message(message.from_user.id, message.message_id)


@dp.callback_query_handler(kbs.cb.filter(action='Аннотация'))
async def annotaion_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Что содержит ваша аннотация?',
                           reply_markup=kbs.createButAnswersPz(2))


@dp.callback_query_handler(kbs.cb.filter(action='Обзор предметной области'))
async def reviewsubarea_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Присутсвует ли в вашей работе обзор предметной области?',
                           reply_markup=kbs.createButAnswersPz(3))


@dp.callback_query_handler(kbs.cb.filter(action='Обзор аналогов'))
async def reviewanalog_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Содержится в вашем проекте обзор аналогов?',
                           reply_markup=kbs.createButAnswersPz(4))


@dp.callback_query_handler(kbs.cb.filter(action='Моделирование'))
async def modelir_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Ваша работа содержит моделирование?',
                           reply_markup=kbs.createButAnswersPz(5))


@dp.callback_query_handler(kbs.cb.filter(action='Техническое задание'))
async def techzad_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Указано ли у вас техническое задание?',
                           reply_markup=kbs.createButAnswersPz(6))


@dp.callback_query_handler(kbs.cb.filter(action='Архитектура программы'))
async def arhitectprogr_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Присутствует у вас разработка архитектуры программы?',
                           reply_markup=kbs.createButAnswersPz(7))


@dp.callback_query_handler(kbs.cb.filter(action='Структуры данных'))
async def structuredata_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Включена ли в работу разработка структуры данных?',
                           reply_markup=kbs.createButAnswersPz(8))


@dp.callback_query_handler(kbs.cb.filter(action='Пользоват. интерфейс'))
async def polinterf_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Присутствует ли у вас пользовательский интерфейс?',
                           reply_markup=kbs.createButAnswersPz(9))


@dp.callback_query_handler(kbs.cb.filter(action='Обработка событий и ошибок'))
async def eventhandling_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Присутствует обработка событий и ошибок ввода данных?',
                           reply_markup=kbs.createButAnswersPz(10))


@dp.callback_query_handler(kbs.cb.filter(action='Программный алгоритм'))
async def softwarealgorithm_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'У вас есть разработка программного алгоритма?',
                           reply_markup=kbs.createButAnswersPz(11))


@dp.callback_query_handler(kbs.cb.filter(action='Интерфейс хранения данных'))
async def datastorageinterface_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Включена в работу организация интерфейса хранения данных?',
                           reply_markup=kbs.createButAnswersPz(12))


@dp.callback_query_handler(kbs.cb.filter(action='Тестирование'))
async def testing_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Присутствует тестирование в вашей работе?',
                           reply_markup=kbs.createButAnswersPz(13))


@dp.callback_query_handler(kbs.cb.filter(action='Руководство программиста'))
async def programmerguide_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Указано ли у вас руководство программиста?',
                           reply_markup=kbs.createButAnswersPz(14))


@dp.callback_query_handler(kbs.cb.filter(action='Руководство оператора'))
async def operatormanual_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Есть ли руководство оператора?',
                           reply_markup=kbs.createButAnswersPz(15))


@dp.callback_query_handler(kbs.cb.filter(action='Заключение'))
async def conclusion_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Не забыли про заключение?',
                           reply_markup=kbs.createButAnswersPz(16))


@dp.callback_query_handler(kbs.cb.filter(action='Список литературы'))
async def listliterature_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Присутсвует список литературы?',
                           reply_markup=kbs.createButAnswersPz(17))

# ------------------------------------------------------------------------------


# ПЗ Подтверждение отмеченных ответов

# ------------------------------------------------------------------------------

@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm1'))
async def listliterature_command(message: types.Message):
    connect = Connection.connect()
    cursor = connect.cursor()

    sql = "exec [dbo].[UpdateIntroduction] ?, ?"

    TrueFalse = storage.Options_answ_TrueFalse.get(message.from_user.id)

    resultTrueFalse = (TrueFalse, False)[TrueFalse == None]

    params = (message.from_user.id, resultTrueFalse)
    cursor.execute(sql, (params))

    connect.commit()
    cursor.close()
    connect.close()

    # asyncio.create_task(tool.delete_message(storage.messageid_temp))
    await bot.send_message(message.from_user.id, f'{random.choice(storage.list_support)}')




@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm2'))
async def pzOptConfirm2_command(message: types.Message):
    sql = "exec [dbo].[UpdateAnnotation] ?, ?, ?"
    totalQuestions = 5
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)

    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm3'))
async def pzOptConfirm3_command(message: types.Message):
    sql = "exec [dbo].[UpdateSubjectAreaOverview] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm4'))
async def pzOptConfirm4_command(message: types.Message):
    sql = "exec [dbo].[UpdateOverviewOfAnalags] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm5'))
async def pzOptConfirm5_command(message: types.Message):
    sql = "exec [dbo].[UpdateModeling] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm6'))
async def pzOptConfirm6_command(message: types.Message):
    sql = "exec [dbo].[UpdateTechnicalSpecification] ?, ?, ?"
    totalQuestions = 5
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm7'))
async def pzOptConfirm7_command(message: types.Message):
    sql = "exec [dbo].[UpdateDevelopmentProgramArchitecture] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm8'))
async def pzOptConfirm8_command(message: types.Message):
    sql = "exec [dbo].[UpdateDataStructureDevelopment] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm9'))
async def pzOptConfirm9_command(message: types.Message):
    sql = "exec [dbo].[UpdateUserInterface] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm10'))
async def pzOptConfirm10_command(message: types.Message):
    sql = "exec [dbo].[UpdateHandlingEventsDataEntryErrors] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm11'))
async def pzOptConfirm11_command(message: types.Message):
    sql = "exec [dbo].[UpdateDevelopmentSoftwareAlgorithm] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm12'))
async def pzOptConfirm12_command(message: types.Message):
    sql = "exec [dbo].[UpdateOrganizationDataStorageInterface] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm13'))
async def pzOptConfirm13_command(message: types.Message):
    sql = "exec [dbo].[UpdateTesting]  ?, ?, ?"
    totalQuestions = 3
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm14'))
async def pzOptConfirm14_command(message: types.Message):
    sql = "exec [dbo].[UpdateProgrammerGuide] ?, ?, ?"
    totalQuestions = 3
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm15'))
async def pzOptConfirm15_command(message: types.Message):
    sql = "exec [dbo].[UpdateOperatorManual] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm16'))
async def pzOptConfirm16_command(message: types.Message):
    sql = "exec [dbo].[UpdateConclusion] ?, ?, ?"
    totalQuestions = 6
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='pzOptConfirm17'))
async def pzOptConfirm17_command(message: types.Message):
    sql = "exec [dbo].[UpdateListLiterature] ?, ?, ?"
    totalQuestions = 2
    answers = tool.update_answers(message.from_user.id, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


# ------------------------------------------------------------------------------


# ----------------------------------------------------------

# Добавление выбранных ответов

@dp.callback_query_handler(kbs.cb.filter(action='pzOptTrue'))
async def pzopt1_command(message: types.Message):
    storage.Options_answ_TrueFalse[message.from_user.id] = True



@dp.callback_query_handler(kbs.cb.filter(action='pzOptFalse'))
async def pzopt1_command(message: types.Message):
    storage.Options_answ_TrueFalse[message.from_user.id] = False



# ----------------------------------------------------------

# добавление отмеченных ответов в список в storage

# ----------------------------------------------------------

@dp.callback_query_handler(kbs.cb.filter(action='pzOpt1'))
async def pzopt1_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('1')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt2'))
async def pzopt2_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('2')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt3'))
async def pzopt3_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('3')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt4'))
async def pzopt4_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('4')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt5'))
async def pzopt5_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('5')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt6'))
async def pzopt6_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('6')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt7'))
async def pzopt7_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('7')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt8'))
async def pzopt8_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('8')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt9'))
async def pzopt9_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('9')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt10'))
async def pzopt10_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('10')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt11'))
async def pzopt11_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('11')


@dp.callback_query_handler(kbs.cb.filter(action='pzOpt12'))
async def pzopt12_command(message: types.Message):
    storage.Options_answ[message.from_user.id].append('12')

# ----------------------------------------------------------


@dp.callback_query_handler(kbs.cb.filter(action='pz'))
async def pz_command(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Пояснительная записка:', reply_markup=kbs.createButPz())


@dp.message_handler(text='Меню')
async def process_menu_message(message: types.Message):
    if message.text.lower() == 'меню':

        connect = Connection.connect()
        cursor = connect.cursor()

        sql = "exec [dbo].GetParticipantRole ?"
        params = (message.from_user.id)
        cursor.execute(sql, (params))

        idRole = str(cursor.fetchall())[2:-3]

        cursor.close()
        connect.close()

        if idRole == '1':
            await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_keyboard)

        elif idRole == '2':
            await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_forRukov_keyboard)


@dp.callback_query_handler(kbs.cb.filter(action='menu'))
async def process_mmenu_message(message: types.Message):
    connect = Connection.connect()
    cursor = connect.cursor()

    sql = "exec [dbo].GetParticipantRole ?"
    params = (message.from_user.id)
    cursor.execute(sql, (params))

    idRole = str(cursor.fetchall())[2:-3]

    cursor.close()
    connect.close()

    if idRole == 1:
        await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_keyboard)

    elif idRole == 2:
        await bot.send_message(message.chat.id, 'Меню:', reply_markup=kbs.menu_forRukov_keyboard)



# --------------------------------------------------------------------------------


# Статистика
# --------------------------------------------------------------------------------


@dp.callback_query_handler(kbs.cb.filter(action='statPZ'))
async def process_menu_message(message: types.Message):
    sql = "exec [dbo].[StatProcExNote] ?"
    outStr = tool.stat_comomn(message.from_user.id, sql, True)
    await bot.send_message(message.from_user.id, f'Статистика ПЗ:\n{outStr}', reply_markup=kbs.statPzDetail_keyboard)


@dp.callback_query_handler(kbs.cb.filter(action='statPO'))
async def process_menu_message(message: types.Message):
    sql = "exec [dbo].[StatProcSoft] ?"
    outStr = tool.stat_comomn(message.from_user.id, sql, False)
    await bot.send_message(message.from_user.id, f'Статистика ПО: \n{outStr}')


@dp.callback_query_handler(kbs.cb.filter(action='statPzDetail'))
async def process_menu_message(message: types.Message):
    sql = "exec [dbo].[GetStatDetailPZ] ?"
    outStr = tool.stat_detailedPz(message.from_user.id, sql)
    await bot.send_message(message.from_user.id, f'Статистика ПЗ (подробная): \n{outStr}')



# --------------------------------------------------------------------------------



# Все по программе
# --------------------------------------------------------------------------------
@dp.callback_query_handler(kbs.cb.filter(action='program'))
async def po_command(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Программа:', reply_markup=kbs.program_keyboard)
    # await bot.send_message(call.message.chat.id, 'Программа:', reply_markup=kbs.createButAnswers())


@dp.callback_query_handler(kbs.cb.filter(action='programCh1'))
async def po_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Что есть в вашей программе? Часть 1',
                           reply_markup=kbs.createButAnswersProgram(1))


@dp.callback_query_handler(kbs.cb.filter(action='programCh2'))
async def po_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []
    await bot.send_message(message.from_user.id, f'Что есть в вашей программе? Часть 2',
                           reply_markup=kbs.createButAnswersProgram(2))


@dp.callback_query_handler(kbs.cb.filter(action='programOptConfirm1'))
async def OptConfirmProgram1_command(message: types.Message):
    sqlOut = "SELECT [Answers2] FROM [StatitisticSoftware] WHERE Id = (SELECT Id FROM Participant WHERE PersonID = ?)"
    sql = "exec [dbo].[UpdateSoftware1] ?, ?, ?"
    totalQuestions = 12
    answers = tool.update_answers_program(message.from_user.id, sqlOut, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


@dp.callback_query_handler(kbs.cb.filter(action='programOptConfirm2'))
async def OptConfirmProgram2_command(message: types.Message):
    sqlOut = "SELECT [Answers1] FROM [StatitisticSoftware] WHERE Id = (SELECT Id FROM Participant WHERE PersonID = ?)"
    sql = "exec [dbo].[UpdateSoftware2] ?, ?, ?"
    totalQuestions = 12
    answers = tool.update_answers_program(message.from_user.id, sqlOut, sql, totalQuestions)
    await bot.send_message(message.from_user.id, f'Выбраны следующие пункты: \n{answers}'
                                                 f'\n{random.choice(storage.list_support)}')


# --------------------------------------------------------------------------------

# Для режим руководителей


@dp.callback_query_handler(kbs.cb.filter(action='getStudents'))
async def getStudents_command(message: types.Message):
    storage.Options_answ[message.from_user.id] = []

    keyboard = kbs.createButStudents(message.from_user.id)
    str_n = ('', '\nХм... а их нет.')[keyboard == None]
    await bot.send_message(message.from_user.id, f'Выберите студента.{str_n}',
                           reply_markup=keyboard)
    await bot.send_message(message.from_user.id, '🙀')


@dp.callback_query_handler(kbs.cb.filter(action='SelectStudentConfirm'))
async def selectStudent_command(message: types.Message):
    temp = int(storage.Options_answ[message.from_user.id][-1]) - 1
    selectedStudentId = int(storage.lst_students.get(message.from_user.id)[temp][0])

    connect = Connection.connect()
    cursor = connect.cursor()

    cursor.execute('SELECT PersonID FROM Participant WHERE Id = ?', selectedStudentId)
    selectedStudentPersonID = str(cursor.fetchall()[0])[2:-3]

    cursor.close()
    connect.close()

    sql = "exec [dbo].[StatProcSoft] ?"
    outStrPO = tool.stat_comomn(selectedStudentPersonID, sql, False)

    sql = "exec [dbo].[StatProcExNote] ?"
    outStrPZ = tool.stat_comomn(selectedStudentPersonID, sql, True)

    sql = "exec [dbo].[GetStatDetailPZ] ?"
    outStrPZDetail = tool.stat_detailedPz(selectedStudentPersonID, sql)

    await bot.send_message(message.from_user.id, f'Выбран:\n{storage.lst_students.get(message.from_user.id)[temp][1]}')
    await bot.send_message(message.from_user.id, f'Статистика ПО: \n{outStrPO}\nСтатистика ПЗ:\n{outStrPZ}')
    await bot.send_message(message.from_user.id, f'Статистика ПЗ (подробная): \n{outStrPZDetail}')





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
