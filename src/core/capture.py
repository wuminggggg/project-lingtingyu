import logging

import mss
from PIL import Image
import pygetwindow


def prt_sc():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = sct.grab(monitor)

    img = Image.frombytes("RGB",sct_img.size,sct_img.bgra,"raw","BGRX")
    print("📸 截图已捕获...")
    return img

def get_window_name():
    window = pygetwindow.getActiveWindow()
    if window is not None:
        return window.title
    else:
        return "桌面或未知窗口"








