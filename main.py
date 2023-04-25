from binance.client import Client
import pandas as pd
#sql alchemy
# print(client.get_account_status())


def get_pair_name(name):
    if name != 'USDT':
        name = name + 'USDT'
    else:
        name = 'BUSD'+name
    return name


def show_actual_assets(client):
    print(f"Posiadane aktywa")
    account_info = client.get_account()
    # pobranie o posiadanych aktywach nazwa:ilosc
    balance = list(map(lambda x: {"name": x['asset'], "amount": x['free']},
                       filter(lambda x: float(x['free']) > 0.0, account_info['balances'])))
    # dopisanie wartosci jednej akcji, wszystkich razem i zmiana % w 24h
    for i in balance:
        name = get_pair_name(i['name'])
        ticker = client.get_symbol_ticker(symbol=name)['price']
        i['price'] = "{:.4s}".format(ticker)
        i['value'] = round(float(ticker) * float(i['amount']), 2)
        i['24h_change'] = round(change_price_in_hours('24', name, client), 2)
    balance = sorted(balance, key=lambda x: x['value'], reverse=True)
    #wyswietlanie tabel
    for i in balance:
        print(i)

    return balance


def change_price_in_hours(hours: str, symbol: str, client):
    # powyzej 8 znakow to nie dziala XD
    if len(symbol)>9:
        return -101
    # pobranie danych z binance o tym symbolu
    candles =  client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=hours, timestamp=None)

    # przezucenie do pd
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                    'close_time', 'quote_asset_volume', 'number_of_trades',
                                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
                                    'ignore'])

    # pierwsza i ostatnia swieca
    try:
        first_candle = df.iloc[0]
        last_candle = df.iloc[-1]
    except:
        return -101
    price_change = float(last_candle['close']) - float(first_candle['open'])

    # Obliczenie procentowego wzrostu lub spadku ceny
    percent_change = price_change / float(first_candle['open']) * 100

    #print(f"Procentowa zmiana ceny {symbol} w ciągu ostatnich {hours} godzin: {percent_change:.2f}%")
    return percent_change


def get_actual_balance(client):
    balance = ":.2f".format(client.get_asset_balance(asset='PLN'))
    # print(balance['free'])
    return balance['free']


def look_market(client):
    exchange_info = client.get_exchange_info()
    # znalezienie par krypto dostepnych z USDT i mapwanie ich do kolumny ich symbolu np MATIC,BTC
    symbols = list(sorted(map(lambda x: x['baseAsset'],
                              filter(lambda x: x['quoteAsset'] == 'USDT', exchange_info['symbols']))))

    # symbols = list(filter(lambda x : 0.5<float(client.get_symbol_ticker(symbol=get_pair_name(x))['price']) <70,symbols))
    # for x in symbols:
    #     print(client.get_symbol_ticker(symbol=get_pair_name(x)))

    # znaleznienie najwiekszych i wiekszych od 1
    symbols = list(sorted(
                    filter(lambda x: float(change_price_in_hours('24', get_pair_name(x), client)) > 1.0, symbols)))
    #key dodac jak zacznie dzialac
    if symbols is None:
        print("Brak danych")
    else:
        for symbol in symbols:
            print(symbol)

# show_actual_assets(client)
# look_market(client)


if __name__ == '__main__':
    api_key = 'TAJNE'
    api_secret = 'TAJNE'
    client = Client(api_key, api_secret)
    client.close_connection()
