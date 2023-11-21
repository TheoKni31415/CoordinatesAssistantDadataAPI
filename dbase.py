import os.path
import sqlite3
from sqlite3 import Error

creat_user = '''
CREATE TABLE IF NOT EXISTS User (
base_url TEXT,
api TEXT,
language TEXT DEFAULT 'ru' CHECK (language IN ('ru', 'en'))
)
'''

text_execute = "INSERT INTO User (base_url, api, language) VALUES ('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/', 'Отсутствует', 'ru')"


def creat_conn():
    conn = None
    try:
        conn = sqlite3.connect('user.db')
    except Error as e:
        print(f'Произошла ошибка: {e}')
    return conn


def creat_table():
    if not os.path.isfile('user.db'):
        connection = creat_conn()
        cursor = connection.cursor()
        cursor.execute(creat_user)
        cursor.execute(text_execute)
        connection.commit()
        connection.close()


def select_user(conn, setting):
    match setting:
        case 1:
            column = 'base_url'
        case 2:
            column = 'api'
        case 3:
            column = 'language'

    select = f"SELECT {column} FROM User"
    cursor = conn.cursor()

    try:
        cursor.execute(select)
        res = cursor.fetchone()[0]

        return res
    except Error as e:
        print(f'Произошла ошибка: {e}')


def update_user(conn, setting, value):
    match setting:
        case 1:
            column = 'base_url'
        case 2:
            column = 'api'
        case 3:
            column = 'language'

    update = f"UPDATE User SET {column} =?"
    cursor = conn.cursor()
    try:
        cursor.execute(update, (value,))
        conn.commit()
        conn.close()
    except Error as e:
        print(f'Произошла ошибка: {e}')
