# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 08/06/2017
# Homework: Term Prject
# Title: Enemy Laser collection as well as all types of weapons
from ColorTransit import *
class EnemyLaserCollection(object):
    def __init__(self, maxL, data):
        self.collection = list()
        self.w = data.width
        self.h = data.height
        self.maxLaserNum = maxL
        self.counter = 0
        for i in range(self.maxLaserNum):
            self.collection.append(EnemyLaser())
            
    def run(self,data):
        for laser in self.collection:
            laser.run()
            laser.borderDetect(self.w, self.h)

    def addLaser(self, x, y, direction, speed):
        self.collection[self.counter] = EnemyLaser(True, x, y, direction, speed)
        self.counter += 1
        if self.counter >= self.maxLaserNum:
            self.counter = 0

    def draw(self, canvas):
        for laser in self.collection:
            laser.draw(canvas)

    def getCollection(self):
        return self.collection

class EnemyLaser(object):
    def __init__(self, present = False, x = 0, y = 0, 
                 direction = (0, 0), speed = 0):
        self.x = x
        self.y = y
        self.isPresent = present
        self.direction = direction
        self.speed = speed
        self.color = Color(rgbToHex((255,255,152)), rgbToHex((255,0,0)), 8, True)
        
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
            w = 6
            h = 6
            canvas.create_oval(self.x-w, self.y-h,
                               self.x+w, self.y+h, fill = self.color)

    def getPresent(self):
        return self.isPresent

    def getPosition(self):
        return (self.x, self.y)

    def destroy(self):
        self.isPresent = False
        
