import binance
from binance import *
from Window import window_maker
# from binance.lib.utils import config_logging


import pandas as pd
#sql alchemy
# print(client.get_account_status())
api_key = 'MCStQtlkXyJh9Yfys4L6plpbspQPbHHcxCEVs5aZjRClgqgXyaRftL7kgfZ0uE4P'
api_secret = 'g4IQD0GC4y2tJV6HnNGk8T7loh3iWWYuXkbl1r3Aq4RML1nt1kIXbJyk6uHabfDA'
client = Client(api_key, api_secret)

def get_pair_name(name):
    if name != 'USDT':
        name = name + 'USDT'
    else:
        name = 'BUSD'+name
    return name


def show_actual_assets():
    # print(f"Posiadane aktywa")
    account_info = client.get_account()
    # pobranie o posiadanych aktywach nazwa:ilosc
    balance = list(map(lambda x: {"name": x['asset'], "amount": x['free']},
                       filter(lambda x: float(x['free']) > 0.0, account_info['balances'])))


    # dopisanie wartosci jednej akcji, wszystkich razem i zmiana % w 24h
    for i in balance:
        name = get_pair_name(i['name'])
        ticker = client.get_symbol_ticker(symbol=name)['price']
        i['amount'] = '{:.6s}'.format(i['amount'])
        i['price'] = "{:.4s}".format(ticker)
        i['value'] = round(float(ticker) * float(i['amount']), 2)
        i['24h_change'] = round(change_price_in_hours(Client.KLINE_INTERVAL_1DAY, name), 2)
    balance = sorted(balance, key=lambda x: x['value'], reverse=True)

    suma=0
    # print(f"Procentowy udzial kazdego aktywa w portfelu:")
    for i in balance:
        suma += i['value']

    for i in balance:
        i['udzial'] = round(i['value'] / suma * 100, 2)
        # print(f"nazwa aktywa: [{i['name']}], udział: [{i['udzial']}]")


    return balance


def change_price_in_hours(hours: str, symbol: str):
    # powyzej 8 znakow to nie dziala XD

    if len(symbol)>9:
        return -101
    # pobranie danych z binance o tym symbolu

    candles =  client.get_klines(symbol=symbol, interval=hours, limit=1)
    try:
        #cena otwarcia pierwszej swiecy
        first_candle = float(candles[0][1])
        #zamkniecia 2
        last_candle = float(candles[-1][4])
    except:
        return -101
    price_change = last_candle - first_candle

    # Obliczenie procentowego wzrostu lub spadku ceny
    percent_change = price_change / first_candle * 100
    #print(f"Procentowa zmiana ceny {symbol} w ciągu ostatnich {hours} godzin: {percent_change:.2f}%")
    return percent_change


def get_actual_balance():
    balance = client.get_asset_balance(asset='PLN')['free']
    #print(balance)
    balance = round(float(balance),2)
    return balance

def get_tradable_symbols():
    all =  list(sorted(map(lambda x: x['baseAsset'],
                              filter(lambda x: x['quoteAsset'] == 'BTC'
                                     ,client.get_exchange_info()['symbols']))))

    return all

def look_market(symbol,hours: str,value_up : float):

    pair_name = get_pair_name(symbol)
    change_price =(float(change_price_in_hours(hours, pair_name)))

    if change_price > value_up:
        return {'symbol': symbol,
                      'value': "{:.4s}".format(client.get_symbol_ticker(symbol=pair_name)['price']),
                      'grow': "{:.2f}".format(change_price)}


