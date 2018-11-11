from Tkinter import *
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

#ellipse class    
class LetterCircle(object):
    #Model
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.r = 65
        self.letter = letter
        self.isLearned = False
        self.fillcolor = "white"
        self.outlinecolor = "dark turquoise"
        
    def changeColor(self):
        self.fillcolor = "light green"
        self.outlinecolor = "white"
            
    def __repr__(self):
        return "x=" + str(self.x) + " y=" + str(self.y) + " r=" + str(self.r) + " let=" + str(self.letter) + " learned=" + str(self.isLearned)
        
    #view    
    def draw(self, canvas, data):
        x1 = self.x-self.r
        y1 = self.y-self.r
        x2 = self.x+self.r
        y2 = self.y+self.r
        if self.isLearned:
            self.changeColor()
        canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.fillcolor, outline=self.fillcolor)
        canvas.create_oval(self.x-(self.r*0.8),self.y-(self.r*0.8),self.x+(self.r*0.8),self.y+(self.r*0.8),fill=self.fillcolor, outline=self.outlinecolor, width="8")
        canvas.create_text(self.x, self.y, text=self.letter, anchor="center", font="Courier 45")
    

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

def init(data):
    data.coords = []
    data.count = 0
    data.d = 150
    data.circles = []
    generateGrid(data)
    data.selectedcircle = None
    data.startstate = True
    data.gridstate = False
    data.learningstate = False
    data.playstate = False
    data.displaynotice = False
    data.canplay = False
    buttonwidth = 300
    buttonheight = 50
    #left,top,right,bot
    data.learnbutton = [data.width/2-buttonwidth-40, data.height/2-buttonheight+80, data.width/2-40, data.height/2+buttonheight+80]
    data.playbutton = [data.width/2+40, data.height/2-buttonheight+80, data.width/2+buttonwidth+40, data.height/2+buttonheight+80]
    data.timer = 0
    data.ellipse1 = [20,20,20]
    data.ellipse2 = [100,100,100]
    data.ellipse3 = [200,200,200]
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
    print(data.bubbleList[0].getYPos)
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

    
def timerFired(data):
    if data.selectedcircle != None and checkLeap() == data.selectedcircle.letter:
        data.selectedcircle.isLearned = True
        data.learningstate = False
        data.gridstate = True
    randomx1 = random.randint(50, data.width-50)
    randomy1 = random.randint(50, data.height-50)
    randomr1 = random.randint(15,100)
    data.ellipse1 = [randomx1,randomy1,randomr1]
    
    randomx2 = random.randint(50, data.width-50)
    randomy2 = random.randint(50, data.height-50)
    randomr2 = random.randint(15,100)
    data.ellipse2 = [randomx2,randomy2,randomr2]
    
    randomx3 = random.randint(50, data.width-50)
    randomy3 = random.randint(50, data.height-50)
    randomr3 = random.randint(15,100)
    data.ellipse3 = [randomx3,randomy3,randomr3]

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
    
def mousePressed(event, data):
    # use event.x and event.y
    if data.startstate:
        lb = data.learnbutton
        pb = data.playbutton
        if lb[0]<=event.x<=lb[2] and lb[1]<=event.y<=lb[3]:
            data.gridstate=True
            data.startstate =False
        elif pb[0]<=event.x<=pb[2] and pb[1]<=event.y<=pb[3]:
            if data.canplay:
                data.playstate = True
                data.startstate = False
            else:
                data.displaynotice = True
    elif data.gridstate:
        for circle in data.circles:
            if circle.x-circle.r<=event.x<=circle.x+circle.r and circle.y-circle.r<=event.y<=circle.y+circle.r:
                data.selectedcircle = circle
                data.learningstate = True
                data.gridstate = False
        if data.canplay:
            if 20<=event.x<=158 and 20<=event.y<=60:
                data.gridstate = False
                data.startstate = True
    elif data.learningstate:
        if 0<=event.x<=data.width and 0<=event.y<=data.height:
            data.gridstate = True
            data.learningstate = False
            data.selectedcircle.isLearned = True
    
def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "l":
        data.canplay = True

#core animation code
def generateGrid(data):
    r = 75
    margin = 100
    while data.count < 26:
        if 0<=data.count<6:
            cols = 6
            y = data.height/5
            # print(y)
            x = 80+data.width/cols/2 + (((data.width/cols)-30) * (data.count%cols))
            # print(data.width/cols, data.count%cols)
            # print((data.width/cols) * (data.count%cols))
            data.coords.append([x,y])
            #print([x,y, count%cols, data.width/cols])
        elif 6<=data.count<13:
            cols = 7
            y = 2*data.height/5
            x = data.width/cols/2 + ((data.width/cols) * (data.count%cols))
            data.coords.append([x,y])
            #print([x,y, count%cols, data.width/cols])
        elif 13<=data.count<19:
            cols = 6
            y = 3*data.height/5
            x = 80+data.width/cols/2 + (((data.width/cols)-30) * (data.count%cols))
            data.coords.append([x,y])
            #print([x,y, count%cols, data.width/cols])
        else:
            cols = 7
            y = 4*data.height/5
            x = data.width/cols/2 + ((data.width/cols) * (data.count%cols))
            data.coords.append([x,y])
            #print([x,y, count%cols, data.width/cols])
        if data.count == 25:
            break
        else:
            data.count+=1
    letterindex = 0
    alphabet = "ABCDEFMGHIJKLOPQRSNYZTUVWX"
    for x in data.coords:
        if letterindex < 26:
            data.circles.append(LetterCircle(x[0], x[1], alphabet[letterindex]))
            letterindex+=1

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill="gainsboro", outline=None)
    if data.startstate:
        lb = data.learnbutton
        pb = data.playbutton
        c1 = data.ellipse1
        c2 = data.ellipse2
        c3= data.ellipse3
        canvas.create_oval(c1[0]-c1[2],c1[1]-c1[2],c1[0]+c1[2],c1[1]+c1[2], fill = "dark turquoise", outline ="white", width = "5")
        canvas.create_oval(c2[0]-c2[2],c2[1]-c2[2],c2[0]+c2[2],c2[1]+c2[2], fill = "dark turquoise", outline ="white", width = "5")
        canvas.create_oval(c3[0]-c3[2],c3[1]-c3[2],c3[0]+c3[2],c3[1]+c3[2], fill = "dark turquoise", outline ="white", width = "5")
        #canvas.create_line(data.width/2,0, data.width/2, data.height)
        canvas.create_rectangle(data.width/2-400, data.height/2-220, data.width/2+400, data.height/2+200, fill = "white", outline="dark turquoise")
        canvas.create_text(data.width/2+5, data.height/4+100, text="ASL Hero", font="Impact 140", fill="dark turquoise")
        canvas.create_rectangle(lb[0],lb[1],lb[2],lb[3], fill="white", outline = "white")
        canvas.create_rectangle(lb[0]+10,lb[1]+10,lb[2]-10,lb[3]-10, fill="white", outline="dark turquoise", width="8")
        canvas.create_text((lb[0]+lb[2])/2, (lb[1]+lb[3])/2, text="Learn", font="Courier 50")
        canvas.create_rectangle(pb[0],pb[1],pb[2],pb[3], fill="white", outline="white")
        canvas.create_rectangle(pb[0]+10,pb[1]+10,pb[2]-10,pb[3]-10, fill="white", outline="dark turquoise", width="8")
        canvas.create_text((pb[0]+pb[2])/2, (pb[1]+pb[3])/2, text="Play", font="Courier 50")
        if data.displaynotice:
            canvas.create_text(data.width/2, data.height*0.9, text="You must learn all the letters before playing!", font="Courier 24")
    elif data.gridstate:
        count = 0
        for circle in data.circles:
            circle.draw(canvas, data)
            if not circle.isLearned:
                count += 1
        if count == 0:
            data.canplay = True
        if data.canplay:
            canvas.create_rectangle(20,20,158,60, fill = "white", outline="light green", width = "5")
            canvas.create_text(90,40, text="Return", fill="light green", font="Courier 25 bold")
    elif data.learningstate:
        canvas.create_oval(data.width/4-220, data.height/2-200, data.width/4+180, data.height/2+200, fill="white", outline="white")
        canvas.create_oval(data.width/4-180, data.height/2-160, data.width/4+140, data.height/2+160, fill="white", outline="dark turquoise", width="20")
        canvas.create_text(data.width/4-20, data.height/2, text=data.selectedcircle.letter, font="Courier 150")
    elif data.playstate:
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
        

def run(width=300, height=300):
    # cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width/2)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height/2)
    # def show_frame():
    #     _, frame = cap.read()
    #     frame = cv2.flip(frame, 1)
    #     image = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    #     cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    #     img = Image.fromarray(cv2image)
    #     imgtk = ImageTk.PhotoImage(image=img)
    #     lmain.imgtk = imgtk
    #     lmain.configure(image=imgtk)
    #     lmain.after(10, show_frame)

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
    data.timerDelay = 10 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
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
    root.mainloop()
    #show_frame()  # blocks until window is closed
    print("bye!")

run(1280, 720)