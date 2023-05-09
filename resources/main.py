from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

from Binance.binance_api import show_actual_assets
from binance.client import Client
import Window.window_maker

if __name__ == '__main__':
    api_key = 'COdC7l6z6wiUc6imvCaVNHbxdQWzZCc5peVZoWG2kckAzDjcio8Zu4QRP9dAuELr'
    api_secret = 'olVwMoCPZP3hSHxVFRqtxf9jDBxpehp8FBUEfLJ1mYkYnCJQr6DxvRrPT5Alqn69'
    # client = Client(api_key, api_secret)
    client = Client(api_key, api_secret)
    okienko = QApplication([])
    window = uic.loadUi('window_designer.ui')
    window.show()
    okienko.exec()
    #client.get_all_orders(symbol='BNBBTC', requests_params={'timeout': 5})
    show_actual_assets(client)
    client.close_connection()

