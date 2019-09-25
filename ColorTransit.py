# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 08/03/2017
# Homework: Term Prject
# Title: Transitioning color, the animation program allows you 
# to visualize the color in transition
import math
from tkinter import *

def rgbToHex(cl):
        (r, g, b) = cl
        return '#%02x%02x%02x' % (int(r), int(g), int(b))

def hexToRGB(c):
        if len(c) != 7: 
            print(c)
            return False
        r = int(c[1:3], 16)
        g = int(c[3:5], 16)
        b = int(c[5:7], 16)
        return (r, g, b)
def constantDerp(c, t, o, l):
    # c = current
    # t = target
    # o = original
    # l = length 
    c += (t-o)/l
    if t > o and c >= t:
        c = t
    elif t < o and c <= t:
        c = t
    return c 

class Color(object):
    def __init__(self, original, target, length, bounce = True):
        self.original = hexToRGB(original)
        self.current = self.original
        self.target = hexToRGB(target)
        self.length = length
        self.timer = 0
        self.bounce = bounce # color switch back and forth

    def __str__(self):
        self.transit()
        return rgbToHex(self.current)

    def transit(self):
        if self.current != self.target:
            o = self.original
            c = self.current
            t = self.target
            self.current = (constantDerp(c[0], t[0], o[0], self.length),
                            constantDerp(c[1], t[1], o[1], self.length),
                            constantDerp(c[2], t[2], o[2], self.length))
        elif self.bounce:
            (self.target, self.original) = (self.original, self.target)

    
        

####################################
# customize these functions
####################################

def init(data):
    data.c = Color(rgbToHex((0,255,0)), rgbToHex((0,0,0)), 100)

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill = data.c, width = 0)

####################################
# use the run function as-is
####################################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
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
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 5
    init(data)
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop() 
    print("bye!")

#run(600, 600)
