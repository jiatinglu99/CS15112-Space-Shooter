# 15-122 Foundamentals of Programming and Computer Science
# Full Name: Terry Lu
# Andrew ID: jiatingl
# Section: A
# Date: 08/06/2017
# Homework: Term Prject
# Title: Enemy Ships Collection File
from tkinter import *
from ColorTransit import *
import math
import random

def degreeToRadian(degree):
    degree %= 360
    return degree/math.pi

def degreeToDir(degree):
    rad = degreeToRadian(degree)
    x = math.cos(rad)
    y = math.sin(rad)
    return (x, y)
    

class EnemyShipCollection(object):
    def __init__(self, maxE, data):
        self.collection = list()
        self.w = data.width
        self.h = data.height
        self.maxEnemyNum = maxE
        self.interval = 400
        self.counter = 0 # list index counter
        self.timeCounter = 0# spawn interval counter
        self.modelList = list()
        self.amount = 0 # how many normal enemy have we spawned
        self.spinnerInterval = 7
        for i in range(1, 6):
            file = 'Enemy' + str(i) + '.png'
            self.modelList.append(PhotoImage(file = file))
        for i in range(self.maxEnemyNum):
            self.collection.append(EnemyShip())

    def spawnShips(self, data, num):
        if self.timeToSpawn(data, self.interval):
            if self.amount < 30:# num of ships to boss
                margin = 100
                for i in range(num):
                    self.spawnNormal(random.randint(margin, self.w - margin))
                    if (self.amount % self.spinnerInterval == 0):# spawn a spinner for every 5++ second 
                        self.spawnSpinner(random.randint(margin, self.w - margin))
            elif not data.userInterface.bossIsOn:
                self.spawnBoss(data.width /2)
                data.userInterface.bossIsOn = True
    def spawnNormal(self, x):
        self.amount += 1
        self.collection[self.counter] = EnemyShip(True, x, (0, 1), 1, 270, self.modelList)
        self.counter += 1
        if self.counter >= self.maxEnemyNum:
            self.counter = 0
    
    def spawnSpinner(self, x):
        self.amount += 1
        self.collection[self.counter] = EnemySpinner(True, x, (0, 1), 1, 270)
        self.counter += 1
        if self.counter >= self.maxEnemyNum:
            self.counter = 0

    def spawnBoss(self, x):
        self.collection[self.counter] = Boss(True, x)
        self.counter += 1
        if self.counter >= self.maxEnemyNum:
            self.counter = 0

    def run(self, data):
        for enemyShip in self.collection:
            enemyShip.run(data)
            enemyShip.borderDetect(self.w, self.h)
            enemyShip.hitDetect(data.userLaserCollection, data.specialEffectCollection)

    def draw(self, canvas):
        for enemyShip in self.collection:
            enemyShip.draw(canvas)
    
    def timeToSpawn(self, data, time):
        self.timeCounter += 1
        if self.timeCounter > time//data.timerDelay:
            self.timeCounter = 0
            return True
        return False

    def getCollection(self):
        return self.collection

def distance(a, b, x, y):
    return ((a-x)**2+(b-y)**2)**0.5

def randomDirectionDown():# generate a random direction pointing down 
        x = random.uniform(-0.2, 0.2)
        y = (1 - x**2)**0.5
        return (x, y)

class EnemyShip(object):
    def __init__(self, present = False, x = 0, direction = (0,0), speed = 0, degree = 0, modelList = []):
        self.x = x
        self.y = -20
        self.isPresent = present
        self.photo = random.choice(modelList).subsample(6, 6) if present and not modelList == [] else 0
        self.direction = direction
        self.enterDir = randomDirectionDown()
        self.enterSpeed = 4
        self.decelerate = 0.05
        self.speed = speed
        self.timeCounter = 0
        self.degree = 270
        self.health = 20
        self.damage = 10
        self.shootInterval = 400

    def run(self, data):
        if self.isPresent:
            self.move()
            #self.generateTrail(data.specialEffectCollection)
            if self.timeToShoot(data, self.shootInterval):
                self.shoot(data)

    def forcedPositionChange(self, x, y):
        self.x = x
        self.y = y
    
    def getPresent(self):
        return self.isPresent

    def hitDetect(self, laserCollection, effectCollection):
        for userLaser in laserCollection.getCollection():
            if userLaser.getPresent() and self.getPresent():
                if self.inHitRange(userLaser.getPosition()):
                    userLaser.destroy(effectCollection)
                    self.getHit(userLaser.damage, effectCollection)

    def getHit(self, damage, effectCollection):
        self.health -= damage
        if self.health <= 0:
            self.destroy(effectCollection)

    def inHitRange(self, laserPosition):
        margin = 20
        lx, ly = laserPosition
        if (lx - margin < self.x < lx + margin and 
            ly - margin < self.y < ly + margin and
            distance(lx, ly, self.x, self.y) < margin):
                return True
        return False
            
    def destroy(self, effectCollection):
        effectCollection.generateExplosions(self.x, self.y)
        self.isPresent = False # can set a timer of dying

    def move(self):
        if self.isPresent:
            self.x = self.speed * self.direction[0]+self.x + self.enterSpeed * self.enterDir[0]
            self.y = self.speed * self.direction[1]+self.y + self.enterSpeed * self.enterDir[1]
            if self.enterSpeed > 0:
                self.enterSpeed -= self.decelerate
                if self.enterSpeed < 0:
                    self.enterSpeed = 0

    # def generateTrail(self, eCollection): # SpecialEffectCollection
    #     w = 12
    #     h = 32
    #     speed = 6
    #     gap = 0.05
    #     eCollection.addEffect(self.x - w, self.y + h, (random.uniform(-gap,gap),1+random.uniform(-0.5, 1)), speed)
    #     eCollection.addEffect(self.x + w, self.y + h, (random.uniform(-gap,gap),1+random.uniform(-0.5, 1)), speed)

    def shoot(self, data):
        if self.isPresent:
            w = 0
            h = 0
            speed = 4
            data.enemyLaserCollection.addLaser(self.x-w, self.y - h, (0,1), speed)

    def draw(self, canvas):
        if self.isPresent:
            #tempPhoto = self.photo.rotate(self.degree)
            canvas.create_image(self.x, self.y, image = self.photo)

    # TODO: enemy shoot
    def timeToShoot(self, data, time):
        self.timeCounter += 1
        if self.timeCounter >= time//data.timerDelay:
            self.timeCounter = 0
            return True
        return False

    def borderDetect(self, w, h):
        if self.isPresent:
            margin = 20
            if self.y > h: 
                self.isPresent = False

class EnemySpinner(EnemyShip):
    def __init__(self, present = False, x = 0, direction = (0,0), speed = 0, degree = 0):
        super().__init__(present, x, direction, speed, degree, [])
        self.photo = PhotoImage(file = 'EnemySpin.png').subsample(5, 5)
        self.angle = 15
        self.health = 60
        self.shootInterval = 50
        self.angleIncrement = 20

    def shoot(self, data):
        if self.isPresent:
            w = 0
            h = 0
            speed = 4
            self.angle = (self.angle + self.angleIncrement)%360
            dirt = (math.cos(self.angle/180*math.pi), math.sin(self.angle/180*math.pi))
            data.enemyLaserCollection.addLaser(self.x-w, self.y - h, dirt, speed)

    def inHitRange(self, laserPosition):
        margin = 40
        lx, ly = laserPosition
        if (lx - margin < self.x < lx + margin and 
            ly - margin < self.y < ly + margin and
            distance(lx, ly, self.x, self.y) < margin):
                return True
        return False

class Boss(EnemyShip):
    def __init__(self, present = False, x = 0, direction = (0,0), speed = 0, degree = 0):
        super().__init__(present, x, direction, speed, degree, [])
        self.photo = PhotoImage(file = 'Boss.png').subsample(1, 1)
        self.direction = (1, 0)
        self.enterDir = (0,1)
        self.enterSpeed = 5
        self.decelerate = 0.03
        self.speed = 0
        self.turrets = []
        # turrets have no direction or speed
        self.turrets.append(EnemySpinner(True, x, (0, 0), 0, 270))
        self.turrets.append(EnemySpinner(True, x, (0, 0), 0, 270))
        self.turrets[1].angleIncrement = -20
        self.turrets.append(EnemyShip(True, x, (0, 0), 0, 270))
        self.turrets[2].shootInterval = 100
        self.turrets.append(EnemyShip(True, x, (0, 0), 0, 270))
        self.turrets[3].shootInterval = 100
        self.turretColor = Color(rgbToHex((255,255,152)), rgbToHex((255,0,0)), 40)
        for turret in self.turrets:
            turret.health = 250
        self.health = 1000
        self.y = -200
        self.isAlive = True

    def run(self, data):
        if self.isAlive:
            self.move()
            #self.generateTrail(data.specialEffectCollection)
            if self.timeToShoot(data, 1000):# shoot after 3 seconds
                for turret in self.turrets:
                    turret.run(data)
            self.forceEditPositions()
            self.turretHitDetection(data)
            self.healthCheck()
            self.deadTurretCheck(data)
        else:
            self.timeCounter = (self.timeCounter + 1)%4
            if self.timeCounter == 0:
                data.specialEffectCollection.generateExplosions(self.x+random.randint(-200,200), 
                                                self.y+random.randint(-100,100))
    def getAlive(self):
        return self.isAlive

    def deadTurretCheck(self, data):
        for turret in self.turrets:
            if not turret.isPresent:
                turret.timeCounter = (turret.timeCounter + 1)%20
                if turret.timeCounter == 0:
                    turret.destroy(data.specialEffectCollection)
                # keep making the explosions

    def healthCheck(self):
        result = 0
        for turret in self.turrets:
            result += turret.health
        self.health = result
        if self.health <= 0:
            self.isAlive = False

    def turretHitDetection(self, data):
        for turret in self.turrets:
            turret.hitDetect(data.userLaserCollection, data.specialEffectCollection)

    def move(self):
        if self.isPresent:
            self.x = self.speed * self.direction[0]+self.x + self.enterSpeed * self.enterDir[0]
            self.y = self.speed * self.direction[1]+self.y + self.enterSpeed * self.enterDir[1]
            if self.enterSpeed > 0:
                self.enterSpeed -= self.decelerate
                if self.enterSpeed < 0:
                    self.enterSpeed = 0
            w = 600
            margin = 200
            if self.x < margin or self.x > w-margin:
                self.direction = (-self.direction[0],self.direction[1])
                self.x = self.speed * self.direction[0]+self.x + self.enterSpeed * self.enterDir[0]
                self.y = self.speed * self.direction[1]+self.y + self.enterSpeed * self.enterDir[1]

    def forceEditPositions(self):
        w = 150
        h = 0
        self.turrets[0].forcedPositionChange(self.x - w, self.y - h)
        self.turrets[1].forcedPositionChange(self.x + w, self.y - h)
        w = 80
        h = 140
        self.turrets[2].forcedPositionChange(self.x - w, self.y + h)
        self.turrets[3].forcedPositionChange(self.x + w, self.y + h)

    def draw(self, canvas):
        if self.isPresent:
            canvas.create_image(self.x, self.y, image = self.photo)
            for turret in self.turrets[:2]:
                w = 20
                h = 20
                c = self.turretColor if turret.getPresent() else 'snow'
                canvas.create_rectangle(turret.x - w, turret.y - h,
                                        turret.x + w, turret.y + h,
                                        fill = c, width = 2)
            for turret in self.turrets[2:]:
                w = 10
                h = 40
                c = self.turretColor if turret.getPresent() else 'snow'
                canvas.create_rectangle(turret.x - w, turret.y - h,
                                        turret.x + w, turret.y + h,
                                        fill = c, width = 2)

    def timeToShoot(self, data, time):
        self.timeCounter += 1
        if self.timeCounter >= time//data.timerDelay:
            self.speed = 1
            #self.timeCounter = 0 # not resetting it
            return True
        return False
    
    def inHitRange(self, laserPosition):
        margin = -1 # boss cannot be hurt 
        lx, ly = laserPosition
        if (lx - margin < self.x < lx + margin and 
            ly - margin < self.y < ly + margin and
            distance(lx, ly, self.x, self.y) < margin):
                return True
        return False

    def getHP(self):
        return self.health