from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

import Connection
import storage

cb = CallbackData('mark', 'action')


def createButPz():
    keyboard = InlineKeyboardMarkup()
    lst_button = []
    for i in storage.list_pz:
        lst_button.append(InlineKeyboardButton(i, callback_data=f'mark:{i}'))

    for i in lst_button:
        keyboard.add(i)

    return keyboard


# выбор роли
role_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Студент', callback_data='mark:roleStudent'),
    InlineKeyboardButton('Руководитель', callback_data='mark:roleRukov')
)

# подтверждение регистрации
yesorno_registr_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Да', callback_data='mark:ConfirmRegistr'),
    InlineKeyboardButton('Нет', callback_data='mark:registr')
)

# подтверждение удаления аккаунта
delete_account_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Да', callback_data='mark:deleteAccount'),
    InlineKeyboardButton('Нет', callback_data='mark:menu')
)

# Программа
program_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Часть 1', callback_data='mark:programCh1'),
    InlineKeyboardButton('Часть 2', callback_data='mark:programCh2')
)

# это наше меню
menu_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('Регистрация', callback_data='mark:registr'),
    InlineKeyboardButton('Руководитель', callback_data='mark:rukovUpdate')
).add(
    InlineKeyboardButton('ПЗ', callback_data='mark:pz'),
    InlineKeyboardButton('Программа', callback_data='mark:program')
).add(
    InlineKeyboardButton('Статистика ПЗ', callback_data='mark:statPZ'),
    InlineKeyboardButton('Статистика ПО', callback_data='mark:statPO')
)

# меню для руководителей
menu_forRukov_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('Регистрация', callback_data='mark:registr')
).add(InlineKeyboardButton('Студенты', callback_data='mark:getStudents'))




# кнопка
button = KeyboardButton('Меню')
menu_button = ReplyKeyboardMarkup(resize_keyboard=True).add(button)

# кнопка Введение
button_introduction = KeyboardButton('Введение')
introduction_button = ReplyKeyboardMarkup(resize_keyboard=True).add(button)

# Регистрация
reg_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Регистрация', callback_data='mark:registr')
)

# Статистика
stat_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Статистика', callback_data='mark:stat')
)

statPzDetail_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Подробнее', callback_data='mark:statPzDetail')
)



# Вывод руководителей

def createButRukov():
    storage.lst_rukov = []

    keyboard = InlineKeyboardMarkup()

    conn = Connection.connect()
    cursor = conn.cursor()

    str_temp = ""
    cursor.execute(
        "SELECT [Id], [LastName], [FirstName], [Patronymic] FROM [Participant] WHERE IdRole = (SELECT Id FROM [Role] WHERE [Name] = ?)",
        'Руководитель')
    for row in cursor.fetchall():
        str_temp = str(row)[1:-1].replace("'", "").replace(" ", "").split(",")
        n_str_temp = f'{str_temp[1]} {str_temp[2][0]}. {str_temp[3][0]}.'
        storage.lst_rukov.append([str_temp[0], n_str_temp])

    cursor.close()
    conn.close()

    num = 1
    for i in storage.lst_rukov:
        keyboard.add(InlineKeyboardButton(i[1], callback_data=f'mark:pzOpt{num}'))
        num += 1

    keyboard.add(InlineKeyboardButton('Подтвердить', callback_data=f'mark:rukovOptConfirm'))
    return keyboard


rukov_update_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Изменить', callback_data='mark:getRukov'))


# Вывод студентов

def createButStudents(idPerson):
    keyboard = InlineKeyboardMarkup()

    conn = Connection.connect()
    cursor = conn.cursor()

    cursor.execute("exec [dbo].[GetStudentsBySuperviser] ?", str(idPerson))

    storage.lst_students[idPerson] = []
    for row in cursor.fetchall():

        str_temp = str(row)[1:-1].replace("'", "").replace(" ", "").split(",")
        n_str_temp = f'{str_temp[1]} {str_temp[2][0]}. {str_temp[3][0]}.'
        storage.lst_students[idPerson].append([str_temp[0], n_str_temp])

    studentsTemp = storage.lst_students.get(idPerson)

    cursor.close()
    conn.close()

    if len(studentsTemp) == 0:
        return None

    num = 1
    for i in studentsTemp:
        keyboard.add(InlineKeyboardButton(i[1], callback_data=f'mark:pzOpt{num}'))
        num += 1

    keyboard.add(InlineKeyboardButton('Подтвердить', callback_data=f'mark:SelectStudentConfirm'))
    return keyboard




# ПЗ варианты ответов

def createButAnswersPz(question):
    keyboard = InlineKeyboardMarkup()

    num = 1
    for i in storage.dict_pzOptions[question]:
        keyboard.add(InlineKeyboardButton(i, callback_data=f'mark:pzOpt{num}'))
        num += 1

    keyboard.add(InlineKeyboardButton('Подтвердить', callback_data=f'mark:pzOptConfirm{question}'))
    return keyboard


# программа варианты ответов


def createButAnswersProgram(question):
    keyboard = InlineKeyboardMarkup()

    num = (7, 1)[question == 1]
    for i in storage.dict_program_options[question]:
        keyboard.add(InlineKeyboardButton(i, callback_data=f'mark:pzOpt{num}'))
        num += 1

    keyboard.add(InlineKeyboardButton('Подтвердить', callback_data=f'mark:programOptConfirm{question}'))
    return keyboard


# ПЗ Введение варианты ответов

Introduction_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data='mark:pzOptTrue'),
                                                   InlineKeyboardButton('Нет', callback_data='mark:pzOptFalse'))

Introduction_keyboard.add(InlineKeyboardButton('Подтвердить', callback_data='mark:pzOptConfirm1'))

# -------------------------------------------------------------------------
