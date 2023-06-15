from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import storage

list_pz = [
    'Введение',
    'Аннотация',
    'Обзор предметной области',
    'Обзор аналогов',
    'Моделирование',
    'техническое задание',
    'архитектура программы',
    'структуры данных',
    'пользовательский интерфейс',
    'обработка событий и ошибок',
    'программный алгоритм',
    'интерфейс хранения данных',
    'тестирование',
    'руководство программиста',
    'руководство оператора',
    'заключение',
    'список литературы'

]

cb = CallbackData('mark', 'action')


def createButPz():
    group_keyboard = InlineKeyboardMarkup()
    lst_button = []
    for i in list_pz:
        lst_button.append(InlineKeyboardButton(i, callback_data=f'mark:{i}'))

    for i in lst_button:
        group_keyboard.add(i)

    return group_keyboard


def createButGroups(lst):
    group_keyboard = InlineKeyboardMarkup()
    lst_button = []
    for i in (lst):
        lst_button.append(InlineKeyboardButton(i, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

    for i in lst_button:
        group_keyboard.add(i)

    return group_keyboard


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
    InlineKeyboardButton('Секрет', url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    InlineKeyboardButton('Наши фото', url="https://www.youtube.com/watch?v=pVHKp6ffURY")
).add(
    InlineKeyboardButton('ПЗ', callback_data='mark:pz'),
    InlineKeyboardButton('Программа', callback_data='mark:program')
)

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


# ПЗ варианты ответов

def createButAnswersPz(question):
    pzOptions_keyboard = InlineKeyboardMarkup()

    num = 0
    for i in storage.dict_pzOptions[question]:
        pzOptions_keyboard.add(InlineKeyboardButton(i, callback_data=f'mark:pzOpt{num}'))
        num += 1

    pzOptions_keyboard.add(InlineKeyboardButton('Подтвердить', callback_data=f'mark:pzOptConfirm{question}'))
    return pzOptions_keyboard


# -------------------------------------------------------------------------

study_keyboard = InlineKeyboardMarkup()
history_button = InlineKeyboardButton('История', 'history_but')

study_keyboard.add(history_button)

question1_cb = CallbackData('question1', 'answer')
question2_cb = CallbackData('question2', 'answer')
question3_cb = CallbackData('question3', 'answer')
question4_cb = CallbackData('question4', 'answer')

# Создаем кнопки с вариантами ответов для каждого вопроса для инструментов
question1_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton('Начало строительства Берлинской стены',
                         callback_data=question1_cb.new(
                             answer='a')),
    InlineKeyboardButton('Убийство Франца Фердинанда в Сараево',
                         callback_data=question1_cb.new(
                             answer='b')),
    InlineKeyboardButton(
        'Подписание Тройственного союза между Германией, Австро-Венгрией и Италией',
        callback_data=question1_cb.new(answer='c')))
question2_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton('1789', callback_data=question2_cb.new(answer='a')),
    InlineKeyboardButton('1889', callback_data=question2_cb.new(answer='b')),
    InlineKeyboardButton('1989', callback_data=question2_cb.new(answer='c'))
)
question3_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton('Михаил Горбачев',
                         callback_data=question3_cb.new(answer='a')),
    InlineKeyboardButton('Борис Ельцин',
                         callback_data=question3_cb.new(answer='b')),
    InlineKeyboardButton('Владимир Путин',
                         callback_data=question3_cb.new(answer='c'))
)
question4_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton('1817', callback_data=question4_cb.new(answer='a')),
    InlineKeyboardButton('1917', callback_data=question4_cb.new(answer='b')),
    InlineKeyboardButton('1927', callback_data=question4_cb.new(answer='c'))
)
