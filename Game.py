# oopyDotsDemo.py
# starts with betterDotsDemo and adds:
#   * a dotCounter that counts all the instances of Dot or its subclasses
#   * a MovingDot subclass of Dot that scrolls horizontally
#   * a FlashingMovingDot subclass of MovingDot that flashes and moves

import random
from Tkinter import *
import Tkinter as tk
import subprocess
import urllib2
import Leap
import json
from translate import Translator
from GenerateTrainingSet import GenerateTrainingSet
from PIL import Image, ImageTk
import cv2



class Bubble(object):
    def __init__(self, cx, cy, r, letter, speed):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.letter = letter
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
        canvas.create_text(self.cx, self.cy, text=self.letter, font = "Helvetica " + str(self.r))

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

    def __repr__(self):
        return "y=" + str(self.cy)
    def getYPos(self):
        return self.cy

    def makeCheckTrue(self):
        self.isCheck = True

    def checkTrue(self):
        return self.isCheck

    def checkOriginalSize(self):
        return self.isOriginalSize

    def checkType(self):
        return self.letter


# Core animation code

def init(data):
    data.timer1 = 0
    data.bubbleTimer = 0
    data.score = 0
    data.bubbleScore = 10
    data.bubblesMoving = True
    data.bubbleList = [ ]
    data.currentKey = ""
    data.textTimer = 0
    data.showText = False
    data.textType = ""


def addBubble(data):
    alphaList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letter = alphaList[random.randint(0, 25)]
    startCx = int((896 + 896 +data.width//4)//2)
    startCy = 0
    startR = data.width//16

    newBubble = Bubble(startCx, startCy, startR, letter, 10)
    data.bubbleList.append(newBubble)

def drawBackgroundRect(canvas, data):
    left = 896
    top = 0
    size = data.width//4

    canvas.create_rectangle(left, top, left+size, data.height, fill="gainsboro", outline ="")

def showScore(canvas, data):
    canvas.create_text(data.width//18, int(data.height*0.8), text="Score:  " + str(data.score),
                        font = "Helvetica " + str(data.width//20), anchor=NW)

    if data.bubblesMoving:
        txt = "Ready?"
        colour = "spring green"
    else:
        txt = "Timer:   " + str(int(data.bubbleScore))
        colour = "salmon"
    canvas.create_text(data.width//18, int(data.height*0.72), text=txt,
                        font = "Helvetica " + str(data.width//30), anchor=NW,
                        fill=colour)

def checkBubblesStop(data):
    if data.bubbleList[0].getYPos() == 600:
        data.bubblesMoving = False
        return True
    else:
        data.bubblesMoving = True
        return False


def checkLeap():
    # Create a translation object
    translator = Translator()
    gestureListener = GenerateTrainingSet()
    controller = Leap.Controller()
    classificationResult = translator.classify(gestureListener.captureGesture(controller))
    return classificationResult


def mousePressed(event, data):
    pass


def keyPressed(event, data):
    pass

def timerFired(data):
    #print(data.showText, data.textTimer, data.textTimer)
    if data.timer1 == 0:
        addBubble(data)
    data.timer1 += 0.1
    data.timer1 = float('{0:.2f}'.format(data.timer1))
    if data.timer1 % 3 == 0:
        if data.bubblesMoving == True:
            addBubble(data)

    if data.bubblesMoving == True:
        for bubble in data.bubbleList:
            bubble.moveBubbleDown()
    else:
        data.bubbleTimer += 0.1
        data.bubbleScore -= 0.1
        data.bubbleList[0].makeCheckTrue()
        data.bubbleList[0].changeBubbleColour()
        if data.bubbleList[0].checkOriginalSize() == True:
            data.bubbleList[0].changeBubbleSize()

    if data.showText == True and data.textTimer < 0.9:
        data.textTimer += 0.1
    elif data.textTimer >= 0.9:
        data.textTimer = 0
        data.showText = False


def checkCurrentBubble(data, canvas):
    print checkLeap(), data.bubbleList[0].checkType()
    print data.bubbleTimer
    if checkLeap() == data.bubbleList[0].checkType():
        data.bubbleList[0].changeBubbleColourCorrect()
        data.score += 1
        data.bubblesMoving = True
        data.bubbleList.pop(0)
        data.bubbleTimer = 0
        data.bubbleScore = 10
        data.textType = "Good"
        data.showText = True
    elif int(data.bubbleTimer) == 10:
        data.bubbleList[0].changeBubbleColourIncorrect()
        data.bubblesMoving = True
        data.bubbleList.pop(0)
        data.bubbleTimer = 0
        data.bubbleScore = 10
        data.textType = "Bad"
        data.showText = True


def redrawAll(canvas, data):
    showScore(canvas, data)
    checkBubblesStop(data)
    drawBackgroundRect(canvas,data)
    if data.bubblesMoving == False:
        checkCurrentBubble(data,canvas)
    for bubble in data.bubbleList:
        bubble.draw(canvas)
    #print(checkLeap())
    if data.showText == True:
        if data.textType == "Good":
            canvas.create_text(data.width//3, data.height//3, text="AMAZING",
                                font = "Helvetica " + str(data.width//10))
        else:
            canvas.create_text(data.width//3, data.height//3, text="TOO SLOW!",
                                font = "Helvetica " + str(data.width//10))
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width/2)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height/2)
    def show_frame():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)

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
    lmain = tk.Label(root)
    lmain.pack()
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    #show_frame()
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(1280, 720)