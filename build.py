from copy import deepcopy
from dataclasses import make_dataclass
from distutils.archive_util import make_archive
from re import T
from telnetlib import X3PAD
from tkinter import E
from pyautogui import *
import pyautogui
import time
import random
import win32api, win32con
import keyboard
import pynput
import cv2
import math

import numpy as np
import argparse
import pytesseract
import pydirectinput
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print("die")
def eat(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(4) #This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    print("yummy yummy that was good")
def cleanImg(img):
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

def getDirection():
    keyboard.press('f3')
    keyboard.release('f3')
    time.sleep(.1)
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
def getCoords():
    keyboard.press('f3')
    keyboard.release('f3')
    time.sleep(.1)
    Coords = pyautogui.screenshot(region=(0,375,800,50))
    keyboard.press('f3')
    keyboard.release('f3')
    Coords = cleanImg(Coords)
    coords = pytesseract.image_to_string(Coords)
    copy = deepcopy(coords)
    print(coords)
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

def calibrate(I, J):
    calibrated = False
    mouse = pynput.mouse.Controller()

    failC = 0
    while(not calibrated):
        i,j = getDirection()
        
        if i == -1:
            print("failed to calibrate")
            failC += 1
            if(failC > 3):
                mouse.move(100, 100)
                failC = 0
        else:
            if(I == 180):
                if(I < 0):
                    I = 360 - abs(I)
                if(i < 0):
                    i = 360 - abs(i)

            moveAmount = 100
            if(abs(I-i) > 10):
                moveAmount = 1000
            if(abs(I-i) > 20):
                moveAmount = 3000
            if(abs(I-i) > 90):
                moveAmount = 5000

            if(abs(i) <= 360) & (abs(j) <= 180):
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
        

    time.sleep(1)
def centerOnBlock():
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
    print(xyz)
def buildPlatform(x,y,platform):
    centerOnBlock()
    time.sleep(1)
    r = 180
    calibrate(r,80)
    time.sleep(1)
    for row in range(x):
        keyboard.press('alt')
        if r == 180:
            for col in range(y-1):
                keyboard.press('s')
                time.sleep(1)
                keyboard.release('s')
                keyboard.press(platform[row][col+1])
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)

                keyboard.release(platform[row][col+1])
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        else:
            for col in reversed(range(y-1)):
                keyboard.press('s')
                time.sleep(1)
                keyboard.release('s')

                keyboard.press(platform[row][col])
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)

                keyboard.release(platform[row][col])
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        time.sleep(1)
        keyboard.release('alt')
        centerOnBlock()
        if(row != x-1):
            if(r == 180):
                
                r = r - 90
                calibrate(r,80)
                keyboard.press('alt')
                keyboard.press('s')
                time.sleep(1)
                keyboard.release('s')
                keyboard.press(platform[row+1][y-1])
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)

                keyboard.release(platform[row+1][y-1])
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
                r = r - 90
                time.sleep(1)
                keyboard.release('alt')
                centerOnBlock()
                calibrate(r,80)

            elif(r == 0):
                r = r + 90
                calibrate(r,80)
                keyboard.press('alt')
                keyboard.press('s')
                time.sleep(1)
                keyboard.release('s')
                keyboard.press(platform[row+1][0])
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
                keyboard.release(platform[row+1][0])
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
                r = r + 90
                time.sleep(1)
                keyboard.release('alt')
                centerOnBlock()
                calibrate(r,80)
    calibrate(-90,0)
    keyboard.press('alt')
    keyboard.press('s')
    time.sleep(x)
    keyboard.release('s')
    keyboard.press('a')
    time.sleep(y)
    keyboard.release('a')

    keyboard.press('w')
    time.sleep(0.5)
    keyboard.release('w')
    keyboard.press('d')
    time.sleep(0.5)
    keyboard.release('d')
    keyboard.release('alt')

    centerOnBlock()
def makeCircle(width, height, a, b, r):
    p = [[]]
    p = [['1' for x in range(width)] for y in range(height)]
    EPSILON = 2.2
    # draw the circle
    for y in range(height):
        for x in range(width):
            # see if we're close to (x-a)**2 + (y-b)**2 == r**2
            if abs((x-a)**2 + (y-b)**2 - r**2) < EPSILON**2:
                p[y][x] = '2'

    for line in p:
        print (' '.join(line))
    return p
def makeSphere(size, radius):
    ''' size : size of original 3D numpy matrix A.
    radius : radius of circle inside A which will be filled with ones. 
    '''


    ''' A : numpy.ndarray of shape size*size*size. '''
    A = [[ ['1' for col in range(size)] for col in range(size)] for row in range(size)]

    ''' AA : copy of A (you don't want the original copy of A to be overwritten.) '''
    AA = deepcopy(A) 

    ''' (x0, y0, z0) : coordinates of center of circle inside A. '''
    x0, y0, z0 = int(np.floor(len(A[0])/2)), int(np.floor(len(A[1])/2)), int(np.floor(len(A[2])/2))


    for x in range(x0-radius, x0+radius+1):
        for y in range(y0-radius, y0+radius+1):
            for z in range(z0-radius, z0+radius+1):
                ''' deb: measures how far a coordinate in A is far from the center. 
                        deb>=0: inside the sphere.
                        deb<0: outside the sphere.'''   
                deb = radius - ((x0-x)**2 + (y0-y)**2 + (z0-z)**2)**0.5
                if (deb)>=0: AA[x][y][z] = "2"
    return AA
def makeTorus(size, radius, r2):

    A = [[ ['.' for col in range(size)] for col in range(size)] for row in range(size)]

    AA = deepcopy(A) 

    x0, y0, z0 = int(np.floor(len(A[0])/2)), int(np.floor(len(A[1])/2)), int(np.floor(len(A[2])/2))


    for x in range(x0-radius, x0+radius+1):
        for y in range(y0-radius, y0+radius+1):
            for z in range(z0-radius, z0+radius+1):
 
                deb = (r2 - math.sqrt(((x)**2 + (y)**2)))**2 + (z)**2 - radius**2
                if ((deb) <= 0): AA[x][y][z] = "#"
    return AA  

#time.sleep(3)
np.set_printoptions(threshold=sys.maxsize)

R3 = makeSphere(11, 5)

for i in R3:
    for j in i:
        print(j)
    print("+++++++++++++++")

#centerOnBlock()
#buildPlatform(11,11,platform = p)
time.sleep(5)

for i in R3:

    buildPlatform(15,15, i)
    calibrate(90,80)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    keyboard.press('space')
    time.sleep(0.5)
    keyboard.release('space')
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

'''
keyboard.press('alt')
keyboard.press('s')
win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
time.sleep(10) #This pauses the script for 0.1 seconds
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
keyboard.release('s')
keyboard.release('alt')
'''
