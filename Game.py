# oopyDotsDemo.py
# starts with betterDotsDemo and adds:
#   * a dotCounter that counts all the instances of Dot or its subclasses
#   * a MovingDot subclass of Dot that scrolls horizontally
#   * a FlashingMovingDot subclass of MovingDot that flashes and moves

import random
from tkinter import *

class Bubble(object):
    def __init__(self, cx, cy, r, type, speed):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.type = type
        self.speed = speed
        self.colour = "white"
        self.ringColour = "dark turquoise"
        self.isCheck = False
        self.isOriginalSize = True


    def draw(self, canvas):
        #varaibles to draw outer circle
        outerLeft = self.cx - self.r
        outerRight = self.cx + self.r
        outerUp = self.cy - self.r
        outerDown = self.cy + self.r

        innerLeft = self.cx - int(self.r*0.85)
        innerRight = self.cx + int(self.r*0.85)
        innerUp = self.cy - int(self.r*0.85)
        innerDown = self.cy + int(self.r*0.85)


        canvas.create_oval(outerLeft, outerUp, outerRight, outerDown, fill = self.colour, outline="")
        canvas.create_oval(innerLeft, innerUp, innerRight, innerDown, fill = self.colour,
                            outline = self.ringColour, width = 10)
        canvas.create_text(self.cx, self.cy, text=self.type, font = "Helvetica " + str(self.r))

    def moveBubbleDown(self):
        self.cy += self.speed

    def changeBubbleColour(self):
        self.colour = "dark turquoise"
        self.ringColour = "white"

    def changeBubbleColourCorrect(self):
        self.colour = "spring green"

    def changeBubbleColourIncorrect(self):
        self.colour = "salmon"

    def changeBubbleSize(self):
        self.r = int(self.r*(1.3))
        self.isOriginalSize = False

    def getYPos(self):
        return self.cy

    def makeCheckTrue(self):
        self.isCheck = True

    def checkTrue(self):
        return self.isCheck

    def checkOriginalSize(self):
        return self.isOriginalSize

    def checkType(self):
        return self.type




# Core animation code

def init(data):
    data.timer = 0
    data.score = 0
    data.bubblesMoving = True
    data.bubbleList = [ ]
    data.currentKey = ""


def addBubble(data):
    alphaList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    type = alphaList[random.randint(0, 25)]
    startCx = int((data.width*(7/10) +(data.width*(7/10)+data.width//4))//2)
    startCy = 0
    startR = data.width//16

    newBubble = Bubble(startCx, startCy, startR, type, 10)
    data.bubbleList.append(newBubble)

def drawBackgroundRect(canvas, data):
    left = int(data.width*(7/10))
    top = 0
    size = data.width//4

    canvas.create_rectangle(left, top, left+size, data.height, fill="gainsboro", outline ="")

def checkBubblesStop(data):
    if data.bubbleList[0].getYPos() == 600:
        data.bubblesMoving = False
        return True
    else:
        data.bubblesMoving = True
        return False

def checkLeap(data, val):
    return data.currentKey

def mousePressed(event, data):
    pass


def keyPressed(event, data):
    data.currentKey = event.keysym

def timerFired(data):
    if data.timer == 0:
        addBubble(data)
    data.timer += 0.1
    data.timer = float('{0:.2f}'.format(data.timer))
    if data.timer % 3 == 0:
        if data.bubblesMoving == True:
            addBubble(data)

    if data.bubblesMoving == True:
        for bubble in data.bubbleList:
            bubble.moveBubbleDown()
    else:
        data.bubbleList[0].makeCheckTrue()
        data.bubbleList[0].changeBubbleColour()
        if data.bubbleList[0].checkOriginalSize() == True:
            data.bubbleList[0].changeBubbleSize()


def checkCurrentBubble(data, val):
    print(checkLeap(data, val), data.bubbleList[0].checkType())
    if checkLeap(data, val) == data.bubbleList[0].checkType():
        data.bubbleList[0].changeBubbleColourCorrect()
        data.score += 1
    else:
        data.bubbleList[0].changeBubbleColourIncorrect()



def redrawAll(canvas, data):
    checkBubblesStop(data)
    drawBackgroundRect(canvas,data)
    if data.bubblesMoving == False:
        checkCurrentBubble(data, "x")
    for bubble in data.bubbleList:
        bubble.draw(canvas)
    print(checkLeap(data, "x"))
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1280, 720)