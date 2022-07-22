import json
import random
import argparse

system_file = 'system.json'


def get_data(filename):
    """
    Получение данных из системного файла
    """
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data


def system_change(data):
    """
    Запись в системный файл измененных данных
    """
    with open(system_file, 'w') as json_file:
        json.dump(data, json_file)


def rate(data):
    """
    Получение текущего курса UAH к USD
    """
    print(data['exchange_rate'])


def available(data):
    """
    Текуший баланс счета
    """
    print(f"USD {data['USD']}\n"
          f"UAH {data['UAH']}")


def buy_usd(usd_quantity, data):
    """
    Покупка указанной суммы USD
    """
    recount = round(usd_quantity * data['exchange_rate'], 2)
    if (data['UAH'] - recount) > 0:
        data['UAH'] = round((data['UAH'] - recount), 2)
        data['USD'] = round((data['USD'] + usd_quantity), 2)
        system_change(data)
    else:
        print(f"UNAVAILABLE, REQUIRED BALANCE UAH {recount}, AVAILABLE {data['UAH']}")


def sell_usd(usd_quantity, data):
    """
    Продажа указанной суммы USD
    """
    if usd_quantity <= data['USD']:
        recount = usd_quantity * data['exchange_rate']
        data['UAH'] = round((data['UAH'] + recount), 2)
        data['USD'] = round((data['USD'] - usd_quantity), 2)
        system_change(data)
    else:
        print(f"UNAVAILABLE, REQUIRED BALANCE USD {usd_quantity}, AVAILABLE {data['USD']}")


def buy_max_usd(data):
    """
    Покупка USD на все UAH, которые доступны на счете
    """
    if data['UAH'] > 0.01 * data['exchange_rate']:
        amount_of_currency = round(data['UAH'] / data['exchange_rate'], 2)
        data['USD'] = round(data['USD'] + amount_of_currency, 2)
        data['UAH'] = round(data['UAH'] - amount_of_currency * data['exchange_rate'], 2)
        if data['UAH'] < 0:
            data['UAH'] = round((data['UAH'] + 0.01 * data['exchange_rate']), 2)
            data['USD'] = round(data['USD'] - 0.01, 2)
        system_change(data)


def sell_all_usd(data):
    """
    Вродажа всех USD которые доступны на счете
    """
    if data['USD'] > 0:
        amount_of_currency = data['USD'] * data['exchange_rate']
        data['USD'] -= data['USD']
        data['UAH'] = round(data['UAH'] + amount_of_currency, 2)
        system_change(data)
        print(f"YOU SOLD {amount_of_currency} USD")


def next_day(data):
    """
    Рандомная смена курса валют в указанном диапазоне и выдача нового курса
    """
    exchange_rate = data['exchange_rate']
    data['exchange_rate'] = round(random.uniform(exchange_rate - data['delta'], exchange_rate + data['delta']), 2)
    system_change(data)


def restart():
    """
    Перезагрузка системы, вовзращение системного файла к стоковой конфигурации
    """
    data = get_data('config.json')
    system_change(data)


args = argparse.ArgumentParser()
args.add_argument('command')
args.add_argument('amount', type=str, nargs='?', default=0)
args = vars(args.parse_args())
command = args['command']
amount = args['amount']

system_data = get_data(system_file)

if command == 'NEXT':
    next_day(system_data)
elif command == 'RATE':
    rate(system_data)
elif command == 'AVAILABLE':
    available(system_data)
elif command == 'RESTART':
    restart()
elif command == 'BUY':
    if amount == 'ALL':
        buy_max_usd(system_data)
    else:
        buy_usd(float(amount), system_data)
elif command == 'SELL':
    if amount == 'ALL':
        sell_all_usd(system_data)
    else:
        sell_usd(float(amount), system_data)
else:
    print('COMMAND NOT RECOGNIZED')
