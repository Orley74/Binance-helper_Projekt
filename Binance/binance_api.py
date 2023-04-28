from binance.client import Client
from Window import window_maker

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
        i['24h_change'] = round(change_price_in_hours('24', name), 2)
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

    candles =  client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=hours, requests_params={'timeout': 120})
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
    print(percent_change)
    #print(f"Procentowa zmiana ceny {symbol} w ciągu ostatnich {hours} godzin: {percent_change:.2f}%")
    return percent_change


def get_actual_balance():
    balance = client.get_asset_balance(asset='PLN')['free']
    #print(balance)
    balance = round(float(balance),2)
    return balance


def look_market(hours: str,value_up : float):
    #dostepne krypto

    symbols = list(map(lambda x: x['baseAsset'],
                              filter(lambda x: x['quoteAsset'] == 'USDT'

                                     ,client.get_exchange_info()['symbols'])))
    # znalezienie par krypto dostepnych z USDT i mapwanie ich do kolumny ich symbolu np MATIC,BTC


    # znaleznienie najwiekszych i wiekszych od podanej value_up
    # symbols = list(
    #                 filter(lambda x: float(change_price_in_hours(hours, get_pair_name(x)))  > value_up , symbols))
    #key dodac jak zacznie dzialac


    for i in symbols:
        a =(float(change_price_in_hours(hours, get_pair_name(i))))
        if a >value_up:
            result = {'symbol': i,
                      'value': "{:.4s}".format(client.get_symbol_ticker(symbol=get_pair_name(i))['price']),
                      'gross': "{:.2f}".format(a)}
        else:
            continue

    if result is None:
        print("Brak danych")
    else:

        for result in result:
            print(result)
    return result
