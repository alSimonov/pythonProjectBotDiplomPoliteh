import pyodbc


s = 'DESKTOP-IBJCCC1' #Your server name
d = 'DiplomBotDatabase' #Your database name
u = 'admin' #Your login
p = 'admin' #Your login password
str_con = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p

def connect():
    return pyodbc.connect(str_con)

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



