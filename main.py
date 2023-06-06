import asyncio
import threading
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QFont, QTextFormat
from PyQt6.QtWidgets import QLineEdit, QWidget,QVBoxLayout
from Binance.binance_api import *
from Window.window_maker import *
import matplotlib.pyplot as plt
import tensorflow as tf
from ML import *

import pandas as pd


gui_change_sem = threading.Lock()
gui_change_crypto = threading.Lock()
gui_change_asstets_sort = threading.Lock()

def win_style():
    target = window.window_Style.text()

    if target == "Tryb ciemny":
        change_win = threading.Thread(target=dark_win)
        change_win.start()
        window.window_Style.setText("Tryb jasny")
    elif target == "Tryb jasny":
        change_win = threading.Thread(target=light_win)
        change_win.start()
        window.window_Style.setText("Tryb ciemny")

def dark_win():
    gui_change_sem.acquire()
    window.centralWidget().setStyleSheet("""
    #centralwidget {
        background-color: #28272d; 
    }
    QListWidget{
        border-radius: 12px;
        background-color: #504e59;
        overflow: auto;
        color: #817c8d;
    }
    QLabel{
        color: #817c8d;
    } 
    #window_Style{
        background-color: #eeedf5;
        color: #7a7a75;
    }
    #widget{
        border: 1px solid #504e59;
    }
    QRadioButton{
        color: #817c8d;
    }
     """
    )
#backend.qt_compat , qtagg
    gui_change_sem.release()
def light_win():
    gui_change_sem.acquire()
    window.centralWidget().setStyleSheet("""
    #centralwidget {
        background-color: #eeedf5; 
    }
    QListWidget{
        border-radius: 12px;
        background-color: #c0f1f9;
        overflow: auto;
        color: #7a7a75;
    }
    QLabel{
        color: #7a7a75;
    } 
    #window_Style{
        background-color: #28272d;
        color: #817c8d;
    }
    #widget{
        border: 1px solid #c0f1f9;
    }
    QRadioButton{
        color: #7a7a75;
    }
     """
    )
    gui_change_sem.release()

def upgrade_balance_on_account ():
    hajs = window.findChild(QLabel,"hajs")
    balance = get_actual_balance()
    hajs.setText(f"Stan konta: {balance}")


def fill_current_assets():

    actual_assets_data = show_actual_assets()

    najlepszaKrypto = max(actual_assets_data, key= lambda x: x['24h_change'])
    dziennyZysk= round(sum([i['value']*i['24h_change']/100 for i in actual_assets_data]),2)

    if dziennyZysk > 0:
        window.dziennyZysk.setStyleSheet("color: green")
    else:
        window.dziennyZysk.setStyleSheet("color: red")

    window.hajs.setText(f"Obecny stan konta: {get_actual_balance()} zł")
    window.LiczbaPosiadanychAktywow.setText(f"Liczba aktywów: {len(actual_assets_data)}")
    window.dziennyZysk.setText(f"Dzienny zysk: {dziennyZysk}")
    window.najwiekszyWzrost.setText(f"Najwiekszy wzrost: {najlepszaKrypto['name']} {najlepszaKrypto['24h_change']}%")
    try:
        window.currentAssects.clear()
    except:
        window.currentAssects.addItem(
            f"Niepowodznie")
    window.currentAssects.addItem(
        f"Dostepne krypto:\nname |  amount |  price |  value |  24h_change |  udzial")
    for i in actual_assets_data:
        window.currentAssects.addItem(f"{i['name']} | {i['amount']} | {i['price']}$ | {i['value']}$ | {i['24h_change']}% | {i['udzial']}%")

def crypto_more_info(item):
    gui_change_crypto.acquire()
    text = item.text()
    text = text.split("|")
    gui_change_crypto.release()
    symbol = get_pair_name(text[0].replace(" ",""))
    limit_range = 144 #12h w 5 minutach

    candles = client.get_klines(symbol=symbol, interval=client.KLINE_INTERVAL_5MINUTE, limit=limit_range)
    time = [i+1 for i in range(limit_range)]
    close_time = [float(candles[i][4]) for i in range(limit_range)]

    plt.xlabel('czas')
    plt.ylabel('cena')
    plt.title(f"{text[0]}wykres ceny")

    plt.plot(time,close_time)

    plt.show()

def fill_crypt(crypto_list):

    try:
        window.crypto_list.clear()
    except:
        window.crypto_list.addItem(
            f"Niepowodznie")
    window.crypto_list.addItem(
        f"Dostepne krypto:\nname |  price  |  24h change")
    for i in crypto_list:
        window.crypto_list.addItem(
            f"{i['symbol'][:-4]} | {'{:.6s}'.format(i['bidPrice'])}$ | {i['priceChangePercent']}")


def add_crypt():
    gui_change_crypto.acquire()
    crypto_list = list(filter(lambda x: 'usdt' in x['symbol'].lower() and float(x['bidPrice']) > 0, client.get_ticker()))

    if window.all_crypto_per.isChecked():
        crypto_list = list(sorted(crypto_list, key=lambda x: float(x['priceChangePercent']), reverse=True))
        fill_crypt(crypto_list)
    elif window.all_crypto_value.isChecked():
        crypto_list = list(sorted(crypto_list, key=lambda x: float(x['bidPrice']), reverse=True))
        fill_crypt(crypto_list)
    else:
        fill_crypt(crypto_list)
    gui_change_crypto.release()

def update_user():
    update_market = threading.Thread(target=fill_current_assets)
    update_market.start()
def update_crypto():
    update_crypt = threading.Thread(target=add_crypt)
    update_crypt.start()
def add_item_to_search(symbol,result):
    item = QListWidgetItem()
    if float(result['grow']) < 5:
        item.setText(f"{symbol}  |  {result['value']}  |  {result['grow']} {result['trade numbers']}")
        item.setForeground(QColor("white"))
    elif float(result['grow']) < 10:
        item.setText(f"! {symbol}  |  {result['value']}  |  {result['grow']} {result['trade numbers']} !")
        item.setForeground(QColor("yellow"))
        # item.textAlignment("center")
    elif float(result['grow']) < 20:
        item.setText(f"!! {symbol}  |  {result['value']}  |  {result['grow']} {result['trade numbers']} !!")
        item.setForeground(QColor("orange"))
    else:
        item.setText(f"!!! {symbol}  |  {result['value']}  |  {result['grow']} | {result['trade numbers']} !!!")
        item.setForeground(QColor("red"))
    window.search_market.addItem(item)

def search_market_button():
    interval = {
        "3 minuty": Client.KLINE_INTERVAL_3MINUTE,
        "5 minut": Client.KLINE_INTERVAL_5MINUTE,
        "15 minut": Client.KLINE_INTERVAL_15MINUTE,
        "30 minut": Client.KLINE_INTERVAL_30MINUTE,
        "1 godzina": Client.KLINE_INTERVAL_1HOUR,
        "2 godziny": Client.KLINE_INTERVAL_2HOUR,
        "4 godziny": Client.KLINE_INTERVAL_4HOUR,
        "6 godzin": Client.KLINE_INTERVAL_6HOUR,
        "8 godzin": Client.KLINE_INTERVAL_8HOUR,
        "12 godzin": Client.KLINE_INTERVAL_12HOUR,
        "1 dzien": Client.KLINE_INTERVAL_1DAY,
        "3 dni": Client.KLINE_INTERVAL_3DAY,
        "1 tydzien": Client.KLINE_INTERVAL_1WEEK,
        "1 miesiac": Client.KLINE_INTERVAL_1MONTH
    }
    grow = window.search_market_grow.text()
    if grow == "":
        grow = -101
    else:
        grow=float(grow)

    time = str(window.choose_time.currentText())

    current_interval = interval[time]
    window.search_market.clear()

    window.search_market.addItem(
        f"\nDostepne krypto:\nname  |  value  |  wzrost w {time}")
    #


def search_market():
    search_market_th = threading.Thread(target=search_market_button)
    search_market_th.start()

def search_type_changed():
    window.search_market_grow.setPlaceholderText(window.search_type.currentText())


if __name__ == '__main__':

    #Train_set(model)
    # check_ml(model)

    #predict_future(model)
    # print(client.get_all_tickers())
    app = QtWidgets.QApplication([])
    window = MyWindow()

    window.search_type.currentIndexChanged.connect(search_type_changed)
    window.Search_market_button.clicked.connect(search_market)
    window.window_Style.clicked.connect(win_style)
    window.currentAssects.itemDoubleClicked.connect(crypto_more_info)
    window.crypto_list.itemDoubleClicked.connect(crypto_more_info)
    window.all_crypto_per.toggled.connect(update_crypto)
    window.all_crypto_value.toggled.connect(update_crypto)

    dark_win()
    fill_current_assets()
    update_crypto()

    window.my_timer = QTimer()
    window.my_timer.timeout.connect(update_user)
    window.my_timer.start(10000)

    window.show()
    app.exec()


    client.close_connection()

