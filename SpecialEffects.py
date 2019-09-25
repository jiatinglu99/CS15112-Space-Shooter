# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 07/30/2017
# Homework: Term Pr0ject
# Title: User Laser collection as well as all types of weapons
import math
import random
from ColorTransit import *
class SpecialEffectCollection():
    def __init__(self, maxNum, data):
        self.maxEffectNum = maxNum 
        self.w = data.width
        self.h = data.height
        self.collection = list()
        self.counter = 0
        for i in range(self.maxEffectNum):
            self.collection.append(SpecialEffect())

    def run(self):
        for effect in self.collection:
            effect.run()
            effect.borderDetect(self.w, self.h)

    def addEffect(self, x, y, direction, speed, delay = 5, colorTime = 20):
        self.collection[self.counter] = SpecialEffect(True, x, y, direction, speed, delay, colorTime)
        self.counter += 1 
        if self.counter >= self.maxEffectNum:
            self.counter = 0

    def addExplosion(self, x, y, direction, size, delay = 3):
        self.collection[self.counter] = explosionEffect(True, x, y, direction, size, delay)
        self.counter += 1 
        if self.counter >= self.maxEffectNum:
            self.counter = 0

    def draw(self, canvas):
        for effect in self.collection:
            effect.draw(canvas)

    def generateExplosions(self, x, y):
        self.addExplosion(x, y, (0, 0), random.randint(20,25))
        # Add more complexity here
        for i in range(random.randint(3,5)):
            dirt = self.randomDirection()
            size = random.randint(15, 25)
            depth = size**0.5//1
            self.explosionTrail(x, y, dirt, size, depth)
    
    # recursively generate explosion trail
    def explosionTrail(self, x, y, dirt, size, depth):
        if depth == 0:
            return None
        else:
            speed = random.uniform(10, 40)
            x += speed * dirt[0]
            y += speed * dirt[1]
            size -= random.randint(2, 6)
            self.addExplosion(x, y, dirt, size)
            self.explosionTrail(x, y, dirt, size, depth-1)

    def generateEffect(self, x, y, num):
        for i in range(num):
            dirt = self.randomDirection()
            speed = random.uniform(1, 5)
            self.addEffect(x, y,dirt, speed, 3, 20)
            # Add more complication here
            
    def randomDirection(self):# generate a random direction
        x = random.uniform(-1, 1)
        y = (1 - x**2)**0.5
        y = -y if random.choice([True, False]) else y # Allow all direction
        return (x, y)

class SpecialEffect():
    def __init__(self, present = False, x = 0, y = 0, 
                 direction = (0,0), speed = 1, delay = 5, colorTime = 20):
        self.x = x
        self.y = y
        self.isPresent = present
        self.direction = direction
        self.speed = speed
        self.color = Color(rgbToHex((255,255,152)), rgbToHex((255,0,0)), colorTime)
        self.Choice = Color(rgbToHex((0,255,0)), rgbToHex((0,0,0)), colorTime)
        self.timelimit = 80
        self.time = 0
        self.delay = delay

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
            self.time += self.delay
            if self.time >= self.timelimit:
                self.time = 0
                self.isPresent =  False
    
    def draw(self, canvas):
        if self.isPresent:
            w = 1.5
            h = 1.5
            canvas.create_oval(self.x-w, self.y-h,
                               self.x+w, self.y+h, fill = self.color, width = 0)

class explosionEffect(SpecialEffect):
    def __init__(self, present = False, x = 0, y = 0, 
                 direction = (0, 0), size = 20, delay = 10, colorTime = 40):
        super().__init__(present, x, y, direction, 1, delay)
        self.color = Color(rgbToHex((255,255,152)), rgbToHex((255,0,0)), colorTime, False)
        self.size = size
        self.timeLimit = 500

    def run(self):
        if self.isPresent:
            shrinkSpeed = 0.6
            self.size -= shrinkSpeed
            self.x += self.direction[0]*self.speed
            self.y += self.direction[1]*self.speed

    def borderDetect(self, w, h):
        if self.isPresent:
            margin = 10
            if self.size <= 0: 
                self.isPresent = False
            else:
                if (self.x < -margin or self.x > w+margin or
                    self.y < -margin or self.y > h+margin):
                    self.isPresent = False

    def draw(self, canvas):
        if self.isPresent:
            canvas.create_oval(self.x - self.size, self.y - self.size,
                            self.x + self.size, self.y + self.size,
                            fill = self.color, width = 0)
            