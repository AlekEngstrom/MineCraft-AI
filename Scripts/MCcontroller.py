from asyncio.windows_events import NULL
from copy import deepcopy
from pyautogui import *
import pyautogui
import time
import win32api, win32con
import keyboard
import pynput
import win32gui
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def click(x=NULL,y=NULL): #clicks on x,y
    if(x != NULL):
        win32api.SetCursorPos((x,y))
    time.sleep(0.1) 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
def eat(): #eat food in offhand
    if pyautogui.pixel(1015, 901)[0] < 45:
        if pyautogui.pixel(1015, 901)[0] > 30:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
            time.sleep(4) 
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
            
def isHurt(hearts = 5): #checks your hearts to see if they are above the specified amount
    if pyautogui.pixel(744, 902)[0] > 200:
        return False
    print(pyautogui.pixel(744, 902)[0])
    return True

def leave():
    time.sleep(0.1) 
    keyboard.press('esc')
    time.sleep(0.1) 
    click(948, 731)
    exit()
    
def cleanImg(img): #Changes RGB values that are not within the threasholds to black
    X, Y = img.size
    for x in range(X):
        for y in range(Y):
            [r,g,b]=img.getpixel((x, y))
            value = (r,g,b)
            threshold = 223
            threshold2 = 226
            if (r < threshold) | (g < threshold) | (b < threshold):
                value = (0,0,0)
            if (r > threshold2) | (g > threshold2) | (b > threshold2):
                value = (0,0,0)
        img.putpixel((x, y), value)
    return img      
def getDirection(): #Returns the direction the minecraft player is facing
    
    while(True): #wait until we are on minecraft screen and the game is not paused
        if(win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Minecraft 1.18.1 - Singleplayer"):
            if pyautogui.locateOnScreen('paused.png') == None : #TODO take pic of pause screen
                break
    
    keyboard.press('f3')
    keyboard.release('f3')
    time.sleep(.1)
    ''' This Doesnt Work propperly yet
    x,y,width,height = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
    p1 = 490/1040
    p2 = 900/1920
    p3 = 45/1040
    Direction = pyautogui.screenshot(region=(x,p1*(height+y), p2*(width+x), p3*(height+y)))
    '''
    Direction = pyautogui.screenshot(region=(0,490,900,45))
    keyboard.press('f3')
    keyboard.release('f3')
    Direction = cleanImg(Direction)

    direction = pytesseract.image_to_string(Direction)
    print(direction)
    open = 0
    slash = 0
    close = 0
    for i in range(len(direction)):
        if direction[i] == '(':
            open = i
        if direction[i] == '/':
            slash = i 
        if direction[i] == ')':
            close = i   
    try:
        i = float(direction[open+1:slash])
        j = float(direction[slash+2:close])
        return i,j
    except:
        print("failed to read")
        return -1, -1
def getCoords(): #Returns the Coordinates of the minecraft player
    while(True): #wait until we are on minecraft screen and the game is not paused
        if(win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Minecraft 1.18.1 - Singleplayer"):
            if pyautogui.locateOnScreen('paused.png') == None : #TODO take pic of pause screen
                break
    keyboard.press('f3')
    keyboard.release('f3')
    time.sleep(.1)
    Coords = pyautogui.screenshot(region=(0,375,800,50))
    keyboard.press('f3')
    keyboard.release('f3')
    Coords = cleanImg(Coords)
    coords = pytesseract.image_to_string(Coords)
    copy = deepcopy(coords)
    xyz = []
    try:
        for _ in range(3):
            start = 0
            end = -1
            for i in range(len(copy)):
                if copy[i] == ':':
                    start = i
                if copy[i] == '/':
                    end = i 
                    break
            
            temp = float(copy[start+1:end])
            copy = copy[end+1:-1]
            xyz.append(temp) 
        return xyz
    except:
        print("failed to read")
        return [-1]
def calibrate(I = None, J = None): #makes the minecraft player look at direction i,j
    calibrated = False
    mouse = pynput.mouse.Controller()

    failC = 0
    while(not calibrated):
        i,j = getDirection()
        if(J == None):
            J = j
        if(I == None):
            I = i
        if i == -1:
            print("failed to calibrate")
            print(i)
            failC += 1
            if(failC > 300):
                mouse.move(100, 100)
                failC = 0
                return
        else:
            if(I == 180):
                if(I < 0):
                    I = 360 - abs(I)
                if(i < 0):
                    i = 360 - abs(i)
            moveAmount = 50
            if(abs(I-i) > 10): #quick movements
                mouse.move(100, 0)
                i2, j2 = getDirection()
                speed = abs(abs(i)-abs(i2))
                print(speed)
                
                speed = 3
                for _ in range(int(abs(I-i)/speed)):
                    time.sleep(0.01)
                    if i < I-1:
                        mouse.move(100, 0)
                    elif i > I+1:
                        mouse.move(-100, 0)
                continue
            if(abs(J-j) > 10): #for quick movements
                mouse.move(100, 0)
                i2, j2 = getDirection()
                speed = abs(abs(j)-abs(j2))
                speed = 3
                for _ in range(int(abs(J-j)/speed)):
                    time.sleep(0.01)
                    if j < J-2:
                        mouse.move(0, 100)
                    elif j > J+2:
                        mouse.move(0, -100)
                continue
                
            if(abs(i) <= 360) & (abs(j) <= 180): #for percice movements
                if i < I-1:
                    mouse.move(moveAmount, 0)
                elif i > I+1:
                    mouse.move(-moveAmount, 0)
                else:
                    if j < J-2:
                        mouse.move(0, 100)
                    elif j > J+2:
                        mouse.move(0, -100)
                    else:
                        calibrated = True

    time.sleep(.1)
def centerOnBlock(): #centers the minecraft player on the block its standing on
    calibratedx = False        
    calibratedz = False
    calibrate(180,80)
    keyboard.press('alt')
    while(not calibratedx) & (not calibratedz):
        
        xyz = getCoords()
        if(xyz != [-1]):
            calibratedx = False        
            calibratedz = False
            time.sleep(1)
            if(xyz[0]%1 < .49):
                keyboard.press('d')
                time.sleep(.05)
                keyboard.release('d')
            elif(xyz[0]%1 > .51):
                keyboard.press('a')
                time.sleep(.05)
                keyboard.release('a')
            else:
                calibratedx = True

            if(xyz[2]%1 < .49):
                keyboard.press('s')
                time.sleep(.05)
                keyboard.release('s')
            elif(xyz[2]%1 > .51):
                keyboard.press('w')
                time.sleep(.05)
                keyboard.release('w')
            else:
                calibratedz = True
        else:
            print("faild block")
    keyboard.release('alt')
