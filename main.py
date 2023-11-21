import dbase
import json
import requests
from time import sleep

clear = "\n" * 100
val = "address"
text_about = "Перед вами программа, функционал которой позволит вам узнать координаты указанного вами адреса.\n" \
             "Управление программой осуществляется вводом чисел, соответствующих пунктам, указанным в консоли\n" \
             "программы, кроме случая, когда вам потребуется ввести интересующий вас адрес."


class Datas:
    base_url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/'


def search_address(address, query):
    conn = dbase.creat_conn()
    url = dbase.select_user(conn, 1)
    full_url = url + address
    api = dbase.select_user(conn, 2)
    lang = dbase.select_user(conn, 3)
    headers = {
        'Authorization': 'Token ' + api,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "query": query,
        "language": lang
    }
    try:
        result = requests.post(full_url, data=json.dumps(data), headers=headers)
    except requests.exceptions.RequestException as err:
        print(f"Ошибка:{err}")
        return 0

    return result.json()


def list_values(res, dic):
    num = 1
    print("0. Назад.")
    for key in res['suggestions']:
        print(f"{num}. {key['value']}")
        dic[str(num)] = key
        num += 1


def print_results(res):
    while True:
        if len(res['suggestions']) == 0:
            print("По указанному адресу ничего не найдено. Попробуйте изменить свой запрос.")
            coord()
        else:
            num = 1
            dict_res = {}
            print("0. Назад.")
            for key in res['suggestions']:
                print(f"{num}. {key['value']}")
                dict_res[str(num)] = key
                num += 1

            user_choice = input("\nУкажите подходящий адрес или вернитесь назад: ")
            match user_choice:
                case "0":
                    print(clear)
                    coord()
                case _:
                    try:
                        geo_lat = dict_res[user_choice]['data']['geo_lat']
                        geo_lon = dict_res[user_choice]['data']['geo_lon']
                        print(clear)
                        print('Результат:')
                        print(f'Широта: {geo_lat}.')
                        print(f'Долгота: {geo_lon}.')
                        print()
                        break
                    except KeyError:
                        print(clear)
                        print("Введите число.")
                        continue
    coord()


def about():
    print(text_about)
    print("1. Назад")

    user_choice = input('\nВыберите действие: ')
    match user_choice:
        case "1":
            print(clear)
            menu()


def coord():
    print("1.Назад")

    user_choice = input('\nВведите адрес в соответствии с политикой Dadada.ru или вернитесь назад: ')
    match user_choice:
        case "1":
            print(clear)
            menu()
        case _:
            print(clear)
            result = search_address(val, user_choice)
            print_results(result)


def get_url():
    conn = dbase.creat_conn()
    url = dbase.select_user(conn, 1)
    match url:
        case Datas.base_url:
            print(f"Нынешний URL: {url + val} (по умолчанию)")
        case _:
            print(f"Нынешний URL: {url + val}")

    print("1. Вернуть URL по умолчанию")
    print("2. Назад")

    user_choice = input('\nВведите новый URL или выберите действие: ')
    match user_choice:
        case "1":
            print(clear)
            dbase.update_user(conn, 1, Datas.base_url)
            get_url()
        case "2":
            print(clear)
            options()
        case _:
            print(clear)
            dbase.update_user(conn, 1, user_choice)
            get_url()

    conn.close()


def get_api():
    conn = dbase.creat_conn()
    api = dbase.select_user(conn, 2)
    print(f"Нынешний API: {api}")
    print("1. Назад")

    user_choice = input('\nВведите новый API или венитесь назад: ')
    match user_choice:
        case "1":
            print(clear)
            options()
        case _:
            print(clear)
            dbase.update_user(conn, 2, user_choice)
            get_api()

    conn.close()


def get_lang():
    new_lang = None
    conn = dbase.creat_conn()
    lang = dbase.select_user(conn, 3)
    match lang:
        case "ru":
            new_lang = "en"
        case "en":
            new_lang = "ru"

    print(f"Хотите поменять {lang} на {new_lang}?")
    print("1. Да")
    print("2. Нет")

    user_choice = input('\nВыберите действие: ')
    match user_choice:
        case "1":
            print(clear)
            dbase.update_user(conn, 3, new_lang)
            get_lang()
        case "2":
            print(clear)
            options()


def options():
    print("1. Изменить URL")
    print("2. Изменить API-ключ")
    print("3. Изменить язык")
    print("4. Назад")

    user_choice = input('\nВыберите действие: ')
    match user_choice:
        case "1":
            print(clear)
            get_url()
        case "2":
            print(clear)
            get_api()
        case "3":
            print(clear)
            get_lang()
        case "4":
            print(clear)
            menu()


def menu():
    print("1. Описание программы")
    print("2. Найти координаты")
    print("3. Настройки")
    print("4. Выход")

    user_choice = input('\nВыберите действие: ')

    match user_choice:
        case "1":
            print(clear)
            about()
        case "2":
            print(clear)
            coord()
        case "3":
            print(clear)
            options()
        case "4":
            print(clear)
            print("Программа выключается...")
            sleep(3)


def main():
    dbase.creat_table()
    menu()


if __name__ == "__main__":
    main()
