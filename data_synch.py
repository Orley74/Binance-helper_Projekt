import os
import ctypes
import sys

os.system("net stop w32time")
os.system("w32tm /unregister")
os.system("w32tm /register")
os.system("net start w32time")
os.system("w32tm /resync")
