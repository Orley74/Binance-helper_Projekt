
from binance import *
import pandas as pd


api_key = 'MCStQtlkXyJh9Yfys4L6plpbspQPbHHcxCEVs5aZjRClgqgXyaRftL7kgfZ0uE4P'
api_secret = 'g4IQD0GC4y2tJV6HnNGk8T7loh3iWWYuXkbl1r3Aq4RML1nt1kIXbJyk6uHabfDA'
client = Client(api_key, api_secret)
data_range = 250
def get_pair_name(name):
    if name != 'USDT':
        return name + 'USDT'
    else:
        return 'BUSD'+name

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
        i['24h_change'] = round(change_price_in_hours(Client.KLINE_INTERVAL_1DAY, name)['percent_change'], 2)
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

    candles = client.get_klines(symbol=symbol, interval=hours, limit=2)
    try:
        #cena otwarcia
        first_candle = float(candles[-1][1])
        #zamkniecia
        last_candle = float(candles[-1][4])
    except:
        return -101
    price_change = last_candle - first_candle
    volume1 = candles[-1][-4]
    volume2 = candles[0][-4]
    # print(volume1,volume2)
    trades = volume1/volume2 * 100
    # Obliczenie procentowego wzrostu lub spadku ceny
    percent_change = price_change / first_candle * 100
    all = {'percent_change': percent_change,
           'trades': trades}
    #print(f"Procentowa zmiana ceny {symbol} w ciągu ostatnich {hours} godzin: {percent_change:.2f}%")
    return all

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

def look_market_by_Grow(symbol,hours: str,value_up : float):
    pair_name = get_pair_name(symbol)
    if float(client.get_symbol_ticker(symbol=pair_name)['price']) < 0.001:
        return None

    change_price =change_price_in_hours(hours, pair_name)
    # print(change_price)
    if change_price['percent_change'] > value_up:
        return {'symbol': symbol,
                      'value': "{:.4s}".format(client.get_symbol_ticker(symbol=pair_name)['price']),
                      'grow': round(change_price['percent_change'],2),
                      'trade numbers': round(change_price['trades'],2)
                }

def look_market_by_Vol(symbol,hours: str,value_up : float):
    try:
        pair_name = get_pair_name(symbol)
        change_price =change_price_in_hours(hours, pair_name)
    except:
        return None
    # print(change_price)
    if change_price['trades'] > value_up:
        return {'symbol': symbol,
                      'value': "{:.4s}".format(client.get_symbol_ticker(symbol=pair_name)['price']),
                      'grow': round(change_price['percent_change'],2),
                      'trade numbers': round(change_price['trades'],2)
                }

def market(symbol,hours : str):
    try:
        print(client.futures_coin_ticker(symbol = symbol, windowSize = hours))
    except:
        print(Exception)

def get_symbol_data(symbol):
    try:
        df = pd.read_csv("symbol_exchange_data")
    except(FileNotFoundError):
        crypto_list = list(map(lambda x: x['symbol'],
                        filter(lambda x: symbol in x['symbol'][0:3] and float(x['bidPrice']) > 0.5 and float(
                            x['volume']) > 50, client.get_ticker())))
        df = pd.DataFrame({"Name": symbol, "Asset": crypto_list})
        # df.to_csv("symbol_exchange_data", index=False)

    if symbol not in df['Name'].values:
        crypto_list = list(map(lambda x: x['symbol'],
                        filter(lambda x: symbol in x['symbol'][0:3] and float(x['bidPrice']) > 0.5 and float(
                            x['volume']) > 50, client.get_ticker())))
        new_row = pd.DataFrame({"Name": symbol, "Asset": crypto_list})
        df = pd.concat([df,new_row])
    df.to_csv("symbol_exchange_data",index=False)

def get_data(symbol):
    get_symbol_data(symbol)
    all_crypto = pd.read_csv('symbol_exchange_data')
    crypto_list= all_crypto.loc[all_crypto['Name']==symbol, 'Asset'].values

    df = pd.DataFrame()
    clines = [map(lambda x: [x[1],x[2],x[3],x[4],x[5]],client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=data_range)) for symbol in crypto_list]
    #open, high, low, close
    for i in range(len(crypto_list)):
        temp = pd.DataFrame(clines[i], columns= ["open","high","low","close","volume"] )
        temp["name"]= crypto_list[i]
        df = pd.concat([df,temp])
    df.to_csv(f"clines_data_{symbol}", index=False)

def VWAP(symbol):
    get_data(symbol)
    all_crypto = pd.read_csv('symbol_exchange_data')
    crypto_list = all_crypto.loc[all_crypto['Name'] == symbol, 'Asset'].values
    try:
        data = pd.read_csv(f"clines_data_{symbol}")
    except:
        return 0
    secondary = [get_pair_name(sym[3:]) for sym in crypto_list]
    usdt_price_factor = []
    if len(secondary)>1:
        for symb in secondary:
            try:
                avg_price = client.get_avg_price(symbol=symb)
                usdt_price_factor.append(float(avg_price['price']))
            except:
                usdt_price_factor.append(0)

    data['avg'] = ((data['open']+ data['high'] + data['low'] + data['close'])/4)*data["volume"]
    l=0
    if len(secondary)>1:
        for i in crypto_list:
            data.loc[data['name']==i, 'avg'] *= usdt_price_factor[l]
            l+=1
    try:
        data = data.loc[(data != 0).all(axis=1)]
        crypto_numbers = data['name'].nunique()
        s=l/crypto_numbers
    except:
        crypto_numbers=len(crypto_list)
        if crypto_numbers == 0:
            return 0

    #print(data)
    VWAP_table = []
    for i in range(data_range):
        #srednia z 24h
        k=0
         #dane z vol i avg
        vol_table = data.iloc[i::data_range,4]
        stat_table = data.iloc[i::data_range,6]

        x = (sum(stat_table)/crypto_numbers)/(sum(vol_table)/crypto_numbers)
        if len(VWAP_table)>1:
            avg_VWAP=sum(VWAP_table[-12:])/len(VWAP_table[-12:])
            VWAP_table.append((x+avg_VWAP)/2)
        else:
            VWAP_table.append(x)
    #print(VWAP_table)

    data.to_csv(f"clines_data_{symbol}", index=False)

    return VWAP_table



