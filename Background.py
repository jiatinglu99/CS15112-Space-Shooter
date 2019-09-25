# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 07/30/2017
# Homework: Term Project
# Title: Background File
import random
class Background(object):
    def __init__(self, data):
        self.width = data.width
        self.height = data.height
        self.stars = self.starsInit(60, 0.5, 2.5)
        self.auroras = list()
        self.currentMultiplier = 20 #this controls the speed
        self.targetMultiplier = 1
    
    def draw(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = 'black')
        self.drawStars(canvas)

    def starsInit(self,n, sMin, sMax):
        temp = list()
        for i in range(n):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            size = random.uniform(sMin, sMax)
            speed = size/4*3**0.5
            temp.append([x, y, size, speed])
        return temp
    
    def drawStars(self, canvas):
        for star in self.stars:
            canvas.create_rectangle(star[0]-star[2],
                                    star[1]-star[2],
                                    star[0]+star[2],
                                    star[1]+star[2],fill = 'snow', width = 0)

    def run(self):
        for star in self.stars:
            star[1] += self.currentMultiplier*star[3] # y + speed
            if star[1] > self.height:
                star[1] -= self.height

    def decelerate(self):
        self.targetMultiplier = 1
        self.currentMultiplier = self.derp(self.currentMultiplier, self.targetMultiplier)

    def accelerate(self):
        self.targetMultiplier = 20
        self.currentMultiplier = self.derp(self.currentMultiplier, self.targetMultiplier)

    def derp(self, a, x):
        # smoothen the deceleration of stars
        # x and y increase toward targeted x and y at an exponential rate
        rate = 0.03
        result = a + (x-a)*rate
        return result