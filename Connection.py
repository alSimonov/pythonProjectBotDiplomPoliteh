import pyodbc

s = 'DESKTOP-IBJCCC1'  # Your server name
d = 'DiplomBotDB'  # Your database name
u = 'admin'  # Your login
p = 'admin'  # Your login password
str_con = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + s + ';DATABASE=' + d + ';UID=' + u + ';PWD=' + p


def connect():
    return pyodbc.connect(str_con)

