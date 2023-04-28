
import ctypes
import sys


from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLineEdit

from Binance.binance_api import *
from Window.window_maker import *


def synchroniza_time():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "data_synch.py", None, 1)
def upgrade_balance_on_account ():
    hajs = window.findChild(QLabel,"hajs")
    balance = get_actual_balance()
    hajs.setText(f"Stan konta: {balance}")

def user_info():
    ##TODO
    ##zrobic panel uzytkownika z nazwa konta,ew jakies dane inne
    pass
def fill_current_assets():
    current_asstets = window.findChild(QListWidget, "currentAssects")
    actual_assets_data = show_actual_assets()
    window.hajs.setText(f"Obecny stan konta: {get_actual_balance()} zł")
    window.LiczbaPosiadanychAktywow.setText(f"Liczba aktywów: {len(actual_assets_data)}")
    try:
        window.currentAssects.clear()
    except:
        window.currentAssects.addItem(
            f"Niepowodznie")
    window.currentAssects.addItem(
        f"Dostepne krypto:\nname |  amount |  price |  value |  24h_change |  udzial")
    for i in actual_assets_data:
        window.currentAssects.addItem(f"{i['name']} | {i['amount']} | {i['price']}$ | {i['value']}$ | {i['24h_change']}% | {i['udzial']}%")



def search_market_button():
    try:
        search_market = window.findChild(QListWidget, "Search_market")
        gross = int(window.search_market_grow.text())
        time = str(window.search_market_time.text())
    except:
        window.search_market.addItem(f"Niepowodzenie 1")
    try:
        window.search_market.clear()
        result = look_market(time,gross)
        window.search_market.addItem(f"Wyszukiwanie...")
    except:
        window.search_market.addItem(f"Niepowodzenie 2")

    window.search_market.addItem(
        f"Dostepne krypto:\nname  |  value  |  grow in {time} hours")
    for i in result:
        window.search_market.addItem(
            f"{i['symbol']} | {i['value']}$ | {i['gross']}% |")


if __name__ == '__main__':


    #synchronizacja czasu komputera i czasu servera Binance, potrzebne uprawnienia administratora
    #

    app = QtWidgets.QApplication([])
    window = MyWindow()

    window.UserInfo.clicked.connect(user_info)
    window.Search_market_button.clicked.connect(search_market_button)
    fill_current_assets()
    window.my_timer = QTimer()
    window.my_timer.timeout.connect(fill_current_assets)
    window.my_timer.start(10000)
    window.show()
    app.exec()


    client.close_connection()
    #look_market(client,'2',2.5)
