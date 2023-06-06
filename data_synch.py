import ctypes

ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd", "/c net stop w32time & "
                                                          "w32tm /unregister & "
                                                          "w32tm /register &"
                                                          " net start w32time & "
                                                          "w32tm /resync", None, 1)

