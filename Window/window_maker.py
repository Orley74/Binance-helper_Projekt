from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QLabel, QPushButton, QListWidget, QListWidgetItem


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicjalizacja interfejsu użytkownika z pliku .ui
        uic.loadUi("interface.ui", self)










