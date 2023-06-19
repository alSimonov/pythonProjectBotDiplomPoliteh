from aiogram import Bot, Dispatcher, types, executor
import Connection
import storage
from conf import token
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot)


class Mydialog(StatesGroup):
    otvet = State()

def stat_detailedPz(userId, sql):
    connect = Connection.connect()
    cursor = connect.cursor()

    params = userId
    cursor.execute(sql, (params))


    tuple_temp = cursor.fetchall()[0]

    str_introduction = ('0 %', '100 %')[tuple_temp[0] == True]

    list_stat = []

    list_stat.append(f'{storage.list_pz[0]}:  {str_introduction}\n')
    for i in range(1,17):
        list_stat.append(f'{storage.list_pz[i]}:  {int(tuple_temp[i] * 100)} %\n')


    cursor.close()
    connect.close()

    return ''.join(list_stat)



def stat_comomn(userId, sql, PzOrPo):
    connect = Connection.connect()
    cursor = connect.cursor()

    params = userId
    cursor.execute(sql, (params))

    endNum = (-4, -8)[PzOrPo]

    s = float(cursor.fetchall()[0][0])
    s_int1 = s * 20
    x1 = int(s_int1) * '! '

    s_int2 = 20 - s_int1
    x2 = int(s_int2) * '. '

    outStr = f'Прогресс составляет: {int(s * 100)} %\n\t\t\t\t\t{x1+x2}'

    cursor.close()
    connect.close()

    return outStr



def update_answers(userId, sql, totalQuestions):
    connect = Connection.connect()
    cursor = connect.cursor()

    result = len(storage.Options_answ[userId]) / totalQuestions
    answers = ",".join(set(storage.Options_answ[userId]))
    params = (str(userId), answers, result)
    cursor.execute(sql, (params))

    connect.commit()
    cursor.close()
    connect.close()

    storage.Options_answ[userId] = []

    return answers

def update_answers_program(userId, sqlOut , sql, totalQuestions):
    connect = Connection.connect()
    cursor = connect.cursor()

    str_temp = ""
    cursor.execute(sqlOut, userId)

    str_temp = cursor.fetchall()[0][0]

    lst_temp = str_temp.split(',')

    result = (len(set(storage.Options_answ[userId])) + len(lst_temp)) / totalQuestions

    answers = ",".join(set(storage.Options_answ[userId]))
    params = (str(userId), answers, result)
    cursor.execute(sql, (params))

    connect.commit()
    cursor.close()
    connect.close()

    storage.Options_answ[userId] = []

    return answers

