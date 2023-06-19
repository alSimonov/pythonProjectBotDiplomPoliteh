import pyodbc

import storage

s = 'DESKTOP-134JFDN'  # Your server name
d = 'DiplomBotDB'  # Your database name
u = 'admin'  # Your login
p = 'admin'  # Your login password
str_con = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + s + ';DATABASE=' + d + ';UID=' + u + ';PWD=' + p


def connect():
    return pyodbc.connect(str_con)


# conn = connect()
# cursor = conn.cursor()


# cursor.execute("exec [dbo].[GetStudentsBySuperviser] ?", '1481918994')
# for row in cursor.fetchall():
#     print(row)
#
# conn = connect()
# cursor = conn.cursor()
# cursor.execute("exec [dbo].[StatProcExNote] ?", '1544090248')
# for row in cursor.fetchall():
#     s=str(row)[10:-8]
#     s_float=float(s)*100
#     print(f'Ваш прогресс составляет: {str(s_float)[:-2]} %')
#     s_int1 = float(s)*20
#     x1=int(s_int1)*'!'
#
#     s_int2 = 20-s_int1
#     x2=int(s_int2)*'.'
#
#     print(x1+x2)
#
# cursor.close()
# conn.close()

# str_temp = ""
# cursor.execute("SELECT [Id], [LastName], [FirstName], [Patronymic] FROM [Participant] WHERE IdRole = (SELECT Id FROM [Role] WHERE [Name] = ?)",
#                'Руководитель')
# for row in cursor.fetchall():
#     str_temp = str(row)[1:-1].replace("'", "").replace(" ", "").split(",")
#     n_str_temp = f'{str_temp[1]} {str_temp[2][0]}. {str_temp[3][0]}.'
#     storage.lst_rukov.append([str_temp[0], n_str_temp])




# cursor.execute("DELETE Participant WHERE PersonID = ?", '1481918994')
#
# cursor.execute("
# SELECT Id, LastName FROM Participant WHERE PersonID = ?", '1481918994')
# print(len(cursor.fetchall()))
#
#
# cursor.close()
# conn.close()




# conn = connect()
# cursor = conn.cursor()
#
# sql = "exec [dbo].[CreateParticipant] ?, ?, ?, ?, ?"
# params = ('Фролов', 'Виктор', 'Александрович', '100100', 1)
# cursor.execute(sql, (params))
#
# listss = []
# cursor.execute("SELECT * FROM Participant")
# for row in cursor.fetchall():
#     print(str(row))
#     # listss.append(str(row))
#
# print("success")
# conn.commit()
#
# cursor.close()
# conn.close()

# cursor.execute("exec sp_dosomething(123, 'abc')")


# cursor.execute("SELECT Name FROM Groups")
# for row in cursor.fetchall():
#     result = str(row)[2:-3]
#     print(result)


# cursor.execute("INSERT INTO Groups (Name) VALUES (?)", 'somename')
# conn.commit()


# cursor.execute("UPDATE Groups SET Name = ? WHERE id = ?", 'somename', someid)
# conn.commit()

# cursor.execute("DELETE FROM Groups WHERE id = ?", 5)
# conn.commit()
