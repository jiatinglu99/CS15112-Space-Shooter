# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 07/30/2017
# Homework: Term Project -- Alien Strike
# This game is similar to Raiden III, and iOS game -- Gemini
####################################
# Citation
####################################
'''
1. I used the animation barebone program from the course website
2. I used my own Pixel Graphics Creator that I made in java
   two years ago
3. I worked on a similar project in java two years ago, the core 
   mechanism should be similar(I do not have old project code)
4. I searched up how to use tkinter built-in PhotoImage class
5. My mentor Matt suggested me the idea of boss with turrets
6. Professor Davis advised me to add more complexity to the game
7. I searched for opacity and image rotation for tkinter 
   but I failed to find anything
'''
####################################
# Imports #  I am not using additional module
####################################
import math
import random
from tkinter import *
from Background import *
from UserInterface import *
from UserAircraft import *
from UserLaserCollection import *
from SpecialEffects import *
from EnemyShipCollection import *
from EnemyLaserCollection import *
####################################
# customize these functions
####################################
def init(data):
    data.background = Background(data)
    data.userInterface = UserInterface(data)
    data.userAircraft = UserAircraft(data)
    data.userLaserCollection = UserLaserCollection(50, data)
    data.specialEffectCollection = SpecialEffectCollection(150, data)
    data.enemyShipCollection = EnemyShipCollection(30, data)
    data.enemyLaserCollection = EnemyLaserCollection(100, data)


def mousePressed(event, data):
    data.userInterface.mousePressed(event, data)

def keyPressed(event, data):
    data.userInterface.keyPressed(event, data)

def timerFired(data):
    data.userInterface.run(data)

def cursorEntered(event, data):
    data.userInterface.cursorEntered(event, data)

def redrawAll(canvas, data):
    data.userInterface.draw(canvas, data)


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

    def cursorEnterWrapper(event, canvas, data):
        cursorEntered(event,data)
        
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 5
    root = Tk()
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event:
                            cursorEnterWrapper(event, canvas, data))
    root.config(cursor="none")
    timerFiredWrapper(canvas, data)
    root.mainloop()  
    print("bye!")

run(600, 900)