# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 08/07/2017
# Homework: Term Project
# Title: User Interface File

import math
import random
from tkinter import *
from Background import *
from UserAircraft import *
from UserLaserCollection import *
from SpecialEffects import *
from EnemyShipCollection import *
from EnemyLaserCollection import *

class runningText(object):
    def __init__(self, text = ' ', interval = 4):
        self.currentText = ''
        self.targetText = text
        self.finalLen = len(text)
        self.timeCounter = 0
        self.interval = interval
        
    def __str__(self):
        self.transit()
        return self.currentText

    def transit(self):
        if self.finalLen > len(self.currentText):
            self.timeCounter += 1
            if self.timeCounter >= self.interval:
                self.currentText = self.currentText + self.targetText[0]
                self.targetText = self.targetText[1:]
                self.timeCounter = 0


class myButton(object):
    def __init__(self, x, y, text, size = 30, w= 40, h= 20):
        self.x = x
        self.y = y
        self.text = text
        self.w = w
        self.h = h
        self.mouseOn = False
        self.size = size

    def draw(self, canvas, data):
        font = 'Arial ' + str(self.size)
        if self.mouseOn: 
            font += ' bold'
            self.generateEffect(data.specialEffectCollection, 1)
        # canvas.create_rectangle(self.x - self.w, self.y - self.h,
        #                         self.x + self.w, self.y + self.h, outline = 'blue')
        canvas.create_text(self.x, self.y, text = self.text, 
                           font = font, fill = 'snow')

    def checkMouse(self, event):
        if (self.x - self.w <= event.x <= self.x + self.w and
            self.y - self.h <= event.y <= self.y + self.h):
            self.mouseOn = True
        else:
            self.mouseOn = False

    def getMouseOn(self):
        return self.mouseOn

    def generateEffect(self, effectCollection, num):
        for i in range(num):
            dirt = self.randomDirection()
            speed = random.uniform(1, 5)
            effectCollection.addEffect(self.x, self.y,dirt, speed, 3, 20)

    def randomDirection(self):# generate a random direction
        x = random.uniform(-1, 1)
        y = (1 - x**2)**0.5
        y = -y if random.choice([True, False]) else y # Allow all direction
        return (x, y)

class UserInterface(object):
    def __init__(self, data):
        self.w = data.width
        self.h = data.height
        self.cursorX = self.w/2
        self.cursorY = self.h/2
        self.cursorPhoto = PhotoImage(file = "Cursor.png").subsample(6, 6)
        self.command = 'Start'
        self.bossIsOn = False
        self.resetButtonsText()

    def restart(self, data):
        self.__init__(data)
        data.userAircraft = UserAircraft(data)
        data.userLaserCollection = UserLaserCollection(50, data)
        data.specialEffectCollection = SpecialEffectCollection(150, data)
        data.enemyShipCollection = EnemyShipCollection(30, data)
        data.enemyLaserCollection = EnemyLaserCollection(100, data)

    def resetButtonsText(self):
        self.buttonStart = myButton(self.w/2, self.h/2, text = 'Start')
        gap = 80
        self.buttonHelp = myButton(self.w/2, self.h/2 + gap, text = 'Help')
        self.buttonCredit = myButton(self.w/2, self.h/2 + 2*gap, text = 'Credits')
        self.buttonReturn = myButton(self.w/2, self.h/2 + 4*gap, text = 'Return')
        margin = 50
        self.buttonPause = myButton(margin, self.h - margin/2, text = 'Pause', size = 20)
        x = 600 - margin
        self.buttonQuit = myButton(x, self.h - margin/2, text = 'Quit', size = 20)
        self.title = runningText('Alien Strike')
        #self.titleColor = 
        hT = '''
        Aliens are Invading Earth!

        You must destroy all our enemies.

        Use your mouse to control the fighter.

        Dodge enemy lasers and shoot.

        Don't die, Good luck!              
        
                    -- Imperial Fleet Commander
        '''
        self.helpText = runningText(hT)
        cT = '''
        Myself(Terry Lu)
        .
        .
        .
        .
        (jk)
        Instructor: Professor Paul Davis
        2017 Summer 15-112 Section A TAs:
            Roman
            Deborah
            Matt
        Special Thanks to:
            Professor Davis and my mentor Matt
        Continuous Psychological Support:
            George and Oktay
        '''
        self.creditText = runningText(cT)

    def needCursor(self, data):
        if not self.command == 'Fight':
            return True
        else:
            if not data.userAircraft.isAlive():
                return True
        return False

    def updateCursorPosition(self, x, y):
        self.cursorX = x
        self.cursorY = y

    def mousePressed(self, event, data):
        if self.command == 'Start':
            if self.buttonStart.getMouseOn():
                self.command = 'Fight'
                self.resetButtonsText()
            elif self.buttonHelp.getMouseOn():
                self.command = 'Help'
                self.resetButtonsText()
            elif self.buttonCredit.getMouseOn():
                self.command = 'Credit'
                self.resetButtonsText()
        elif self.command == 'Help' or self.command == 'Credit':
            if self.buttonReturn.getMouseOn():
                self.command = 'Start'
                self.resetButtonsText()
                #self.restart(data)
        elif self.command == 'Fight':
            if self.buttonPause.getMouseOn():
                self.command = 'Paused'
                self.resetButtonsText()
            elif self.buttonQuit.getMouseOn():
                self.command = 'Start'
                self.resetButtonsText()
                self.restart(data)
            elif (not data.userAircraft.isAlive()):
                self.restart(data)
            elif self.bossIsOn and self.findBoss(data).getHP() <= 0:
                self.restart(data)
                self.command = 'Credit'
                self.resetButtonsText()
        elif self.command == 'Paused':
            if not self.buttonQuit.getMouseOn():
                self.command = 'Fight'
                self.resetButtonsText()
            else: 
                self.restart(data)
                self.command = 'Start'
                self.resetButtonsText()
        
    def keyPressed(self, event, data):
        self.isOnStartMenu = not self.isOnStartMenu
        self.isFighting = not self.isFighting

    def cursorEntered(self, event, data):
        data.userAircraft.updateTargetPosition(event.x, event.y)
        if self.command == 'Start':
            self.buttonStart.checkMouse(event)    
            self.buttonHelp.checkMouse(event)  
            self.buttonCredit.checkMouse(event)  
        elif self.command == 'Help' or self.command == 'Credit':
            self.buttonReturn.checkMouse(event)
        elif self.command == 'Fight':
            self.buttonPause.checkMouse(event)
            self.buttonQuit.checkMouse(event)
        elif self.command == 'Paused':
            self.buttonQuit.checkMouse(event)
        
        if self.needCursor(data):
            self.updateCursorPosition(event.x, event.y)
        
    def run(self, data):
        if self.command == 'Start':
            data.background.run()
            data.background.accelerate()
            data.specialEffectCollection.run()
        elif self.command == 'Help':
            data.background.run()
            data.background.decelerate()
            data.specialEffectCollection.run()
        elif self.command == 'Credit':
            data.background.run()
            data.background.decelerate()
            data.specialEffectCollection.run()
        elif self.command == 'Fight':
            data.background.run()
            data.background.decelerate()
            data.userAircraft.run(data)
            data.userLaserCollection.run()
            data.specialEffectCollection.run()
            if data.userAircraft.isAlive():
                data.enemyShipCollection.spawnShips(data, 1)
            data.enemyShipCollection.run(data)
            data.enemyLaserCollection.run(data)
            

    def turnOnBoss(self):
        data.enemyShipCollection.spawnBoss(data.width/2)
        self.bossIsOn = True

    def draw(self, canvas, data):
        if self.command == 'Start':
            data.background.draw(canvas)
            data.specialEffectCollection.draw(canvas)
            self.drawStartMenu(canvas, data)
        elif self.command == 'Fight':
            data.background.draw(canvas)
            data.enemyShipCollection.draw(canvas)
            data.enemyLaserCollection.draw(canvas)
            data.userAircraft.draw(canvas)
            data.userLaserCollection.draw(canvas)
            data.specialEffectCollection.draw(canvas)
            self.drawHP(canvas, data)
            if self.bossIsOn:
                self.drawBossHP(canvas, data)
                if self.findBoss(data).getHP() <= 0 and data.userAircraft.isAlive():
                    canvas.create_text(300, 450, text = 'Congradulations', font = 'Arial 20', fill = 'snow')
                    canvas.create_text(300, 480, text = 'You saved Mother Earth', font = 'Arial 20', fill = 'snow')
                    canvas.create_text(300, 510, text = 'Click to See Credit', font = 'Arial 20', fill = 'snow')
            self.buttonPause.draw(canvas, data)
            self.buttonQuit.draw(canvas, data)
            if (not data.userAircraft.isAlive()):
                canvas.create_text(300, 450, text = 'Game Over', font = 'Arial 20', fill = 'snow')
                canvas.create_text(300, 500, text = 'Click to Restart', font = 'Arial 20', fill = 'snow')
        elif self.command == 'Help':
            data.background.draw(canvas)
            data.specialEffectCollection.draw(canvas)
            self.drawHelpMenu(canvas, data)
        elif self.command == 'Credit':
            data.background.draw(canvas)
            data.specialEffectCollection.draw(canvas)
            self.drawCreditMenu(canvas, data)
        elif self.command == 'Paused':
            data.background.draw(canvas)
            data.enemyShipCollection.draw(canvas)
            data.enemyLaserCollection.draw(canvas)
            data.userAircraft.draw(canvas)
            data.userLaserCollection.draw(canvas)
            data.specialEffectCollection.draw(canvas)
            self.drawHP(canvas, data)
            if self.bossIsOn:
                self.drawBossHP(canvas, data)
            self.buttonQuit.draw(canvas, data)
            canvas.create_text(300, 500, text = 'Click to Unpause', font = 'Arial 20', fill = 'snow')

        if self.needCursor(data):
            self.drawCursor(canvas)

    def drawHelpMenu(self, canvas, data):
        x, y = 10, 200
        canvas.create_text(x, y, text = self.helpText, 
                           font = 'Arial 20', anchor = 'nw', fill = 'snow')
        self.buttonReturn.draw(canvas, data)


    def drawCreditMenu(self, canvas, data):
        x, y = 10, 200
        canvas.create_text(x, y, text = self.creditText, 
                           font = 'Arial 20', anchor = 'nw', fill = 'snow')
        self.buttonReturn.draw(canvas, data)

    def drawCursor(self, canvas):
        canvas.create_image(self.cursorX, self.cursorY, image = self.cursorPhoto)

    def drawHP(self, canvas, data):
        x = 20
        y = 20
        w = data.width//5*2
        h = data.height//60
        canvas.create_rectangle(x, y, x+w, y+h, outline = 'green', width = 2)
        margin = 4
        hp = data.userAircraft.getHP()/100
        if hp < 0: hp = 0
        canvas.create_rectangle(x + margin, y + margin,
                                x + w*hp - margin, y + h -margin,
                                fill = 'green', width = 0)
        x = 20
        y = 38
        canvas.create_text(x, y, 
                           text = 'HP '+str(data.userAircraft.getHP()),
                           font = 'Arial 16', anchor = 'nw', fill = 'green')

    def findBoss(self, data):
        for enemy in data.enemyShipCollection.getCollection():
            if type(enemy) == Boss:
                return enemy
        return None
    def drawBossHP(self, canvas, data):
        x = 320
        y = 20
        w = data.width//5*2
        h = data.height//60
        canvas.create_rectangle(x, y, x+w, y+h, outline = 'orange', width = 2)
        margin = 4
        hp = self.findBoss(data).getHP()/1000
        if hp < 0: hp = 0
        w = w - 2*margin
        h = h - 2*margin
        x += margin
        y += margin
        canvas.create_rectangle(x, y,
                                x + w*hp, y + h,
                                fill = 'orange', width = 0)
        x = data.width- 100
        y = 38
        canvas.create_text(x, y, 
                           text = 'HP '+str(self.findBoss(data).getHP()),
                           font = 'Arial 16', anchor = 'nw', fill = 'orange')

    def drawStartMenu(self, canvas, data):
        x = self.w/2
        y = self.h/3
        canvas.create_text(x, y, text = self.title, 
                           font = 'Arial 60', fill = 'snow')
        self.buttonStart.draw(canvas, data)
        self.buttonHelp.draw(canvas, data)
        self.buttonCredit.draw(canvas, data)
        
        