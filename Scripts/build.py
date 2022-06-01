from collections import deque
from copy import deepcopy
import pyautogui, sys
import time
import keyboard
import math
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import MCcontroller as MC

calibrate = MC.calibrate
centerOnBlock = MC.centerOnBlock
fillSpot = '1' #the spot in hotbar that will be used to fill in blocks
def downClick(button = 'right'):
    pyautogui.mouseDown(button)
def upClick(button = 'right'):
    pyautogui.mouseUp(button)

def buildPlatform(x,y,platform): #builds a platform with a 2D array corresposding to the hotbar keys
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
                downClick()

                keyboard.release(platform[row][col+1])
                upClick()
        else:
            for col in reversed(range(y-1)):
                keyboard.press('s')
                time.sleep(1)
                keyboard.release('s')

                keyboard.press(platform[row][col])
                downClick()
                keyboard.release(platform[row][col])
                upClick()
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
                downClick()

                keyboard.release(platform[row+1][y-1])
                upClick()
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
                downClick()
                keyboard.release(platform[row+1][0])
                upClick()
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
def buildShape(path, platform, BreakTemp = False): #builds the shape of the 2D array with as little fill blocks as possible
    x = 0
    y = 0
    prev = None
    for i in range(len(path)):
        if(path[i].y == y) & (path[i].x == x):
            continue
        if(path[i].x > x):
            calibrate(90,80)
        if(path[i].x < x):
            calibrate(-90,80)
        if(path[i].y > y):
            calibrate(180,80)
        if(path[i].y < y):
            calibrate(0,80)
        
        keyboard.press('alt')
        #time.sleep(.1)
        keyboard.press('s')
        time.sleep(.7)
        keyboard.release('s')
        keyboard.press(platform[path[i].x][path[i].y])
        downClick()

        time.sleep(.05)

        keyboard.release(platform[path[i].x][path[i].y])
        upClick()
        
        downClick("middle")
        upClick("middle")

        #Breaks the temporary blocks
        if (prev == fillSpot) & BreakTemp:
            calibrate(J = 70)
            keyboard.press('3')
            time.sleep(.1)
            downClick("left")
            time.sleep(.1)
            upClick("left")
            keyboard.press('3')
            
        prev = platform[path[i].x][path[i].y]
        keyboard.release('alt')     
        x = path[i].x
        y = path[i].y       
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def __repr__(self):
        return str((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def get(self):
        return self.x, self.y
def getPath(node, path=[]):
    if node:
        getPath(node.parent, path)
        path.append(node)
def findPath(grid, x=0, y=0,nextX = None, nextY = None, visited = None): #finds the path to place all the blocks
    
    row = [-1, 0, 0, 1]
    col = [0, -1, 1, 0]
    path = []
    q = deque()
    src = Node(x,y)
    q.append(src)
    
    visited = set()
    key = (src.x, src.y)
    visited.add(key)
    N = len(grid)
    while q:
        current = q.popleft()
        i = current.x
        j = current.y
        
        
        if(grid[i][j] != fillSpot):
            grid[i][j] = fillSpot

            path = []
            p = []

            #time.sleep(4)
            getPath(current, path)
            #print(path)
            '''
            if len(path) > 4: do the split
            p1 = findPath(grid = deepcopy(grid),x = i, y = j, nextX=-1,nextY=0, visited=deepcopy(visited))
            p2 = findPath(grid = deepcopy(grid),x = i, y = j, nextX=0, nextY=-1, visited=deepcopy(visited))
            p3 = findPath(grid = deepcopy(grid),x = i, y = j, nextX=1, nextY=0, visited=deepcopy(visited))
            p4 = findPath(grid = deepcopy(grid),x = i, y = j, nextX=0, nextY=1, visited=deepcopy(visited))
            size = [len(p1), len(p2), len(p3), len(p4)]
            for ff in range(len(size)):
                if size[ff] == 0:
                    size[ff] = 10000
            if (len(p1) == 0) & (len(p2) == 0) & (len(p3) == 0) & (len(p4) == 0):
                
                return path
            m = min(size)

            if len(p1) == m & len(p1) != 0:
                #print(1)
                path += p1
            elif len(p2) == m & len(p2) != 0:
                #print(2)
                path += p2
            elif len(p3) == m & len(p3) != 0:
                #print(3)
                path += p3
            elif len(p4) == m & len(p4) != 0:
                #print(4)
                path += p4
            else:
                print("++++++++++++")
            '''
            path += findPath(grid = deepcopy(grid),x = i, y = j)
            #print(path)
            return path
        
        if(nextX == None):
            for k in range(len(row)):
                x = i + row[k]
                y = j + col[k] 
                if(x < N) & (y < N) & (x >= 0) & (y >= 0):
                    next = Node(x, y, current)
                    key = (next.x, next.y)
                    if key not in visited:
                        q.append(next)
                        visited.add(key)
        else:
            x = i + nextX
            y = j + nextY
            nextX = None
            if(x < N) & (y < N) & (x >= 0) & (y >= 0):
                next = Node(x, y, current)
                key = (next.x, next.y)
                if key not in visited:
                    q.append(next)
                    visited.add(key)
    return []
            
def makeCircle(width, height, a, b, r): #makes a circle in a 2D array
    p = [[]]
    p = [[fillSpot for x in range(width)] for y in range(height)]
    EPSILON = 4
    for y in range(height):
        for x in range(width):
            if abs((x-a)**2 + (y-b)**2 - r**2) < EPSILON**2:
                p[y][x] = '#'

    for line in p:
        print (' '.join(line))
    return p
def makeSphere(size, radius): #makes a sphere in a 3D array
    A = [[ [fillSpot for col in range(size)] for col in range(size)] for row in range(size)]
    AA = deepcopy(A) 
    x0, y0, z0 = int(np.floor(len(A[0])/2)), int(np.floor(len(A[1])/2)), int(np.floor(len(A[2])/2))


    for x in range(x0-radius, x0+radius+1):
        for y in range(y0-radius, y0+radius+1):
            for z in range(z0-radius, z0+radius+1):
                ''' deb: measures how far a coordinate in A is far from the center. 
                        deb>=0: inside the sphere.
                        deb<0: outside the sphere.'''   
                deb = radius - ((x0-x)**2 + (y0-y)**2 + (z0-z)**2)**0.5
                if (deb>=0) & (deb < 1): 
                    AA[x][y][z] = "2"
    return AA
def makeTorus(size, radius, r2): #TODO make a tourus in a 3D array

    A = [[ ['.' for col in range(size)] for col in range(size)] for row in range(size)]

    AA = deepcopy(A) 

    x0, y0, z0 = int(np.floor(len(A[0])/2)), int(np.floor(len(A[1])/2)), int(np.floor(len(A[2])/2))


    for x in range(x0-radius, x0+radius+1):
        for y in range(y0-radius, y0+radius+1):
            for z in range(z0-radius, z0+radius+1): 
                deb = (r2 - math.sqrt(((x0-x)**2 + (y0-y)**2)))**2 + (z0-z)**2 - radius**2
                if (deb>=0) & (deb < 4): 
                    AA[x][y][z] = "2"
    return AA  


#Driver code
to = time.time() #to time how long the builds take

R3 = makeSphere(10,4) #makes the shape that we want to build
path = []
blocks = 0
time.sleep(15) #time to get game ready

for layer in R3: #Loop through each layer of 3D array and build it

    x = 0
    y = 0
    try:
        if(path != []):
            x = path[-1].x
            y = path[-1].y
    except:
        print("sorry")
        
    #Jumps to next level to start building
    calibrate(90,90)
    keyboard.press(layer[x][y])
    downClick()
    keyboard.press('space')
    time.sleep(0.5)
    keyboard.release('space')
    upClick()
    keyboard.release(layer[x][y])
    
    #finds the path and builds it
    c1 = deepcopy(layer)
    #parallel processing could be done here with path
    path = findPath(c1,x,y+1)
    #print("The path is : ", path)
    #print("+++++++++++++++++++++++++++++++++++++++++++++")
    centerOnBlock()
    buildShape(path, layer, BreakTemp=True)
    blocks += len(path)

#print useful information
timeTaken = time.time() - to
print()
print("JOB COMPLETED")
print("This took: ", timeTaken , " seconds.")
print("There were ", blocks, " blocks placed.")
print("This ran at ", timeTaken/blocks, " blocks per second.")

'''
path = findPath(deepcopy([["1","1","1","1","1","2","2"],
                          ["1","1","1","1","1","2","2"],
                          ["1","1","1","1","1","2","2"],
                          ["1","1","1","2","1","2","2"],
                          ["1","1","1","1","1","2","2"],
                          ["1","1","1","1","1","2","2"],
                          ["2","2","2","2","2","2","2"]]))

for i in R3[8]:
    #for line in i:
    print (' '.join(i))
path = findPath(deepcopy(R3[8]))

centerOnBlock()
buildShape(path, deepcopy(R3[8]))
'''