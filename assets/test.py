import mysql.connector
from mysql.connector import OperationalError

connection = mysql.connector.connect(
    host='137.184.125.49',
    user='usertesting',
    password='Va5PKAtv8RCQbcgY',
    database='dataset'
)


def obtenerCursor():
    try:
        cursor = connection.cursor()
        return cursor
    except OperationalError:
        connection.reconnect()
        cursor = connection.cursor()
        return cursor


cursor = obtenerCursor()
# cursor.execute('SELECT command_name FROM comandos')
# tags = cursor.fetchall()

# for tag in tags:
#     cont = 3
#     tag = tag[0]
#     print(f'tag = {tag}')
#     while True:
#         pattern = input('Pattern: ')
#         if pattern == 'salir':
#             break
#         cursor.execute(f"INSERT INTO trainData VALUES('{tag}',{cont},'{pattern}')")
#         cont += 1

tag = 'spotify016'
cont = 5
while True:
    pattern = input('Pattern: ')
    if pattern == 'salir':
        break
    cursor.execute(f"INSERT INTO trainData VALUES('{tag}',{cont},'{pattern}')")
    cont += 1
connection.commit()


