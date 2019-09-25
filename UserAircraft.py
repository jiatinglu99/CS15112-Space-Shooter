# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 07/30/2017
# Homework: Term Prject
# Title: User Aircraft File
from tkinter import *
import math
import random
def distance(a, b, x, y):
    return ((a-x)**2+(b-y)**2)**0.5
class UserAircraft(object):
    def __init__(self, data):
        self.x = data.width/2
        self.y = data.height/5*4
        self.speed = data.width/300
        self.photo = PhotoImage(file = "User Aircraft.png").subsample(6, 6)
        self.hpVal = 100
        self.hpMax = 100
        self.targetX = self.x
        self.targetY = self.y
        self.timeCounter = 0
        self.switch = False
        self.live = True

    def updateTargetPosition(self, x, y):
        if self.live:
            self.targetX = x
            self.targetY = y

    def run(self, data):
        if self.live:
            self.move()
            self.generateTrail(data.specialEffectCollection)
            self.hitDetect(data.enemyLaserCollection, data.specialEffectCollection)
            if self.timeToShoot(data, 50):
                self.shoot(data)
        else:
            if self.timeToShoot(data, 50):
                data.specialEffectCollection.generateExplosions(self.x, self.y)

    def isAlive(self):
        return self.live

    def hit(self, effectCollection, damage):
        # hit effect
        self.hpVal -= damage
        effectCollection.generateEffect(self.x, self.y, random.randint(3,5))
        if self.hpVal <= 0:
            self.destroy(effectCollection)
            self.hpVal = 0

    def destroy(self, effectCollection):
        self.live = False
    
    def getHP(self):
        return self.hpVal

    def hitDetect(self, laserCollection, effectCollection):
        for enemyLaser in laserCollection.getCollection():
            if enemyLaser.getPresent() and self.isAlive():
                if self.inHitRange(enemyLaser.getPosition()):
                    enemyLaser.destroy()
                    self.hit(effectCollection, 10)

    def inHitRange(self, laserPosition):
        margin = 20
        lx, ly = laserPosition
        if (lx - margin < self.x < lx + margin and 
            ly - margin < self.y < ly + margin and
            distance(lx, ly, self.x, self.y) < margin):
                return True
        return False
    
    def move(self):
        (self.x, self.y) = self.derp(self.x, self.y, self.targetX, self.targetY)

    def generateTrail(self, eCollection): # SpecialEffectCollection
        w = 12
        h = 32
        speed = 6
        gap = 0.05
        eCollection.addEffect(self.x - w, self.y + h, (random.uniform(-gap,gap),1+random.uniform(-0.5, 1)), speed)
        eCollection.addEffect(self.x + w, self.y + h, (random.uniform(-gap,gap),1+random.uniform(-0.5, 1)), speed)

    def shoot(self, data):
        if self.live:
            w = 12
            h = 8
            speed = 8
            if self.switch:
                data.userLaserCollection.addLaser(self.x-w, self.y - h, (0,-1), speed)
            else: data.userLaserCollection.addLaser(self.x+w, self.y - h, (0,-1), speed)
            self.switch = not self.switch
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image = self.photo)
        # temporary Game Fix

    def timeToShoot(self, data, time):
        self.timeCounter += 1
        if self.timeCounter >= time//data.timerDelay:
            self.timeCounter = 0
            return True
        return False

    def derp(self, a, b, x, y):
        # smoothen the movement of the aircraft
        # x and y increase toward targeted x and y at an exponential rate
        rate = 0.15
        resultX = a + (x-a)*rate
        resultY = b + (y-b)*rate
        return (resultX, resultY)