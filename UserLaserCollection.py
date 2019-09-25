# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 07/30/2017
# Homework: Term Prject
# Title: User Laser collection as well as all types of weapons
from ColorTransit import *
import random
class UserLaserCollection(object):
    def __init__(self, maxL, data):
        self.collection = list()
        self.w = data.width
        self.h = data.height
        self.maxLaserNum = maxL
        self.counter = 0
        for i in range(self.maxLaserNum):
            self.collection.append(UserLaser())
            
    def run(self):
        for laser in self.collection:
            laser.run()
            laser.borderDetect(self.w, self.h)

    def addLaser(self, x, y, direction, speed):
        self.collection[self.counter] = UserLaser(True, x, y, direction, speed)
        self.counter += 1
        if self.counter >= self.maxLaserNum:
            self.counter = 0

    def draw(self, canvas):
        for laser in self.collection:
            laser.draw(canvas)

    def getCollection(self):
        return self.collection

class UserLaser(object):
    def __init__(self, present = False, x = 0, y = 0, direction = (0, 0), speed = 0):
        self.x = x
        self.y = y
        self.isPresent = present
        self.direction = direction
        self.speed = speed
        self.damage = 10
        self.color = Color(rgbToHex((255,255,152)), rgbToHex((255,0,0)), 100)
        
    def run(self):
        if self.isPresent:
            self.x += self.direction[0]*self.speed
            self.y += self.direction[1]*self.speed

    def borderDetect(self, w, h):
        margin = 10
        if self.isPresent:
            if (self.x < -margin or self.x > w+margin or
                self.y < -margin or self.y > h+margin):
                self.isPresent = False
    def draw(self, canvas):
        if self.isPresent:
            w = 2.5
            h = 8
            canvas.create_oval(self.x-w, self.y-h,
                               self.x+w, self.y+h, fill = self.color)

    def getPresent(self):
        return self.isPresent

    def destroy(self, effectCollection):
        effectCollection.generateEffect(self.x, self.y, random.randint(3, 8))
        self.isPresent = False # can set a timer of dying

    def randomDirection(self):# generate a random direction
        x = random.uniform(-1, 1)
        y = (1 - x**2)**0.5
        y = -y if random.choice([True, False]) else y # Allow all direction
        return (x, y)

    def getPosition(self):
        return (self.x, self.y)

