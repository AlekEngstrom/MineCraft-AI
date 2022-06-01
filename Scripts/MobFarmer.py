import MCcontroller as MC
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
time.sleep(5)
while keyboard.is_pressed('q') == False:
    if(MC.isHurt()):
        MC.leave()
    MC.click()
    MC.eat()
    time.sleep(0.61)