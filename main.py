
import ctypes
import sys
import threading
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QFont, QTextFormat
from PyQt6.QtWidgets import QLineEdit
import logging
from Binance.binance_api import *
from Window.window_maker import *



def upgrade_balance_on_account ():
    hajs = window.findChild(QLabel,"hajs")
    balance = get_actual_balance()
    hajs.setText(f"Stan konta: {balance}")

def user_info():
    ##TODO
    ##zrobic panel uzytkownika z nazwa konta,ew jakies dane inne
    pass
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


def update_user():
    update_market = threading.Thread(target=fill_current_assets)
    update_market.start()




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
    # print(time)
    try:
        window.search_market.clear()
        symbols = get_tradable_symbols()

        window.postepSearchMarket.setMaximum(len(symbols))
        postep = 0
        found = 0
    except:
        window.search_market.addItem(f"Niepowodzenie 2")


    window.search_market.addItem(
        f"\nDostepne krypto:\nname  |  value  |  wzrost w {time}")
    for i in symbols:
        try:
            result = look_market(i, interval[time], grow)
        except:
            continue
        window.postepSearchMarket.setValue(int(postep))
        postep += 1
        if result is None:
            continue
        item = QListWidgetItem()
        found+=1
        if float(result['grow']) < 5:
            item.setText(f"{i}  |  {result['value']}  |  {result['grow']} ")
            item.setForeground(QColor("white"))
        elif float(result['grow']) < 10:
            item.setText(f"! {i}  |  {result['value']}  |  {result['grow']} !")
            item.setForeground(QColor("yellow"))
        elif float(result['grow']) < 20:
            item.setText(f"!! {i}  |  {result['value']}  |  {result['grow']} !!")
            item.setForeground(QColor("orange"))
        else:
            item.setText(f"!!! {i}  |  {result['value']}  |  {result['grow']} !!!")
            item.setForeground(QColor("red"))
        window.search_market.addItem(item)

    window.search_market.addItem(f"Znalezniono {found} elementow spelniajace podana zaleznosc co stanowi {round(found*100/len(symbols),2)}")



    # window.my_timer.start(10000)

def search_market():
    search_market_th = threading.Thread(target=search_market_button)
    search_market_th.start()

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    window = MyWindow()


    window.UserInfo.clicked.connect(user_info)
    window.Search_market_button.clicked.connect(search_market)
    fill_current_assets()
    print(client.get_symbol_ticker(symbol="BTCUSDT"))

    window.my_timer = QTimer()
    window.my_timer.timeout.connect(update_user)
    window.my_timer.start(10000)
    window.show()
    app.exec()


    client.close_connection()

