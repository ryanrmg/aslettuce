from tkinter import *

#ellipse class    
class LetterCircle(object):
    #Model
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.r = 65
        self.letter = letter
        self.isCompleted = False
        
        if self.isCompleted:
            self.fillcolor = "light green"
            self.outlinecolor = "white"
        else:
            self.fillcolor = "white"
            self.outlinecolor = "dark turquoise"
            
    def __repr__(self):
        return "x=" + str(self.x) + " y=" + str(self.y) + " r=" + str(self.r) + " let=" + str(self.letter)
        
    #view    
    def draw(self, canvas, data):
        x1 = self.x-self.r
        y1 = self.y-self.r
        x2 = self.x+self.r
        y2 = self.y+self.r
        canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.fillcolor, outline=self.fillcolor)
        canvas.create_oval(self.x-(self.r*0.8),self.y-(self.r*0.8),self.x+(self.r*0.8),self.y+(self.r*0.8),fill=self.fillcolor, outline=self.outlinecolor, width="8")
        canvas.create_text(self.x, self.y, text=self.letter, anchor="center", font="Helvetica 45")
    
    def getSize(self):
        return self.sz

def init(data):
    data.coords = []
    data.count = 0
    data.d = 150
    data.circles = []
    generateGrid(data)
    
def mousePressed(event, data):
    # use event.x and event.y
    for circle in data.circles:
        if circle.x-circle.r<=event.x<=circle.x+circle.r and circle.y-circle.r<=event.y<=circle.y+circle.r:
            print(circle.letter)

def keyPressed(event, data):
    # use event.char and event.keysym
    pass
    

#core animation code
def generateGrid(data):
    r = 75
    margin = 100
    while data.count < 26:
        print(data.count)
        if 0<=data.count<=5:
            cols = 6
            y = data.height/5
            # print(y)
            x = 80+data.width/cols/2 + (((data.width/cols)-30) * (data.count%cols))
            # print(data.width/cols, data.count%cols)
            # print((data.width/cols) * (data.count%cols))
            data.coords.append([x,y])
            #print([x,y, count%cols, data.width/cols])
        elif 6<=data.count<=12:
            cols = 7
            y = 2*data.height/5
            x = data.width/cols/2 + ((data.width/cols) * (data.count%cols))
            data.coords.append([x,y])
            #print([x,y, count%cols, data.width/cols])
        elif 13<=data.count<=18:
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
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for x in data.coords:
        if letterindex < 26:
            data.circles.append(LetterCircle(x[0], x[1], alphabet[letterindex]))
            letterindex+=1



def redrawAll(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill="gainsboro", outline=None)
    for circle in data.circles:
        circle.draw(canvas, data)
        
        
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

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
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
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1280, 720)