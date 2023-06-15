import pyodbc

s = 'DESKTOP-IBJCCC1'  # Your server name
d = 'DiplomBotDB'  # Your database name
u = 'admin'  # Your login
p = 'admin'  # Your login password
str_con = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + s + ';DATABASE=' + d + ';UID=' + u + ';PWD=' + p


def connect():
    return pyodbc.connect(str_con)


# conn = connect()
# cursor = conn.cursor()
#
#
# cursor.execute("DELETE Participant WHERE PersonID = ?", '1481918994')
#
# cursor.execute("SELECT Id, LastName FROM Participant WHERE PersonID = ?", '1481918994')
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
