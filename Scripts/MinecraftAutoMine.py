from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

import numpy as np
import argparse
import cv2

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print("die")
def eat(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(4) 
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    print("yummy yummy that was good")
def turnRight():
    x, y = pyautogui.position()
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1350, 0, 0, 0)
    print("turn")
def checkLava():
    x = 1920
    y = 1080
    lava = False
    for i in range(0,int(x/2),10):
        
        if pyautogui.pixelMatchesColor(i,int(y/2-100), (255,174,201),tolerance = 10):
            lava = True
            return lava
        if pyautogui.pixelMatchesColor(int(x/2+i),int(y/2-100), (255,174,201),tolerance = 10):
            lava = True
            return lava
        if pyautogui.pixelMatchesColor(int(x/2-i),int(y/2-100), (255,174,201),tolerance = 10):
            lava = True
            return lava
        if pyautogui.pixelMatchesColor(x-i,int(y/2-100), (255,174,201),tolerance = 10):
            lava = True
            return lava
    for i in range(0,int(y/2),10):
        if pyautogui.pixelMatchesColor(int(x/2),i, (255,174,201),tolerance = 10):
            lava = True
            return lava
        if pyautogui.pixelMatchesColor(int(x/2),int(y/2+i), (255,174,201),tolerance = 10):
            lava = True
            return lava
        if pyautogui.pixelMatchesColor(int(x/2),int(y/2-i), (255,174,201),tolerance = 10):
            lava = True
            return lava
        if pyautogui.pixelMatchesColor(int(x/2),y-i, (255,174,201),tolerance = 10):
            lava = True
            return lava
    return lava
def checkLava1():
    if pyautogui.locateOnScreen('RealLava.png')!= None :
        return True
    return False
sleep(5)
while keyboard.is_pressed('q') == False:
    
##    keyboard.press('w')
##    keyboard.press('alt')
##    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
##
    
    if pyautogui.pixel(1015, 901)[0] < 45:
        if pyautogui.pixel(1015, 901)[0] > 30:
            eat(807, 400)
    if(keyboard.is_pressed('o') == True):
        turnRight()
    if(checkLava()):
        print("lava")
        keyboard.release('w')
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        keyboard.press('s')
        sleep(5)
        keyboard.release('s')
        turnRight()
    else:
        print("no Lava")
    #click(1,1)
#    x, y = pyautogui.position()
#    pixelColor = pyautogui.screenshot().getpixel((x, y))
#    print(pixelColor)
#    print(pyautogui.position())
    sleep(1)
keyboard.release('w')
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
keyboard.release('alt')
print("done")














































