import math

class ExpandingBox:
    def __init__(self,x,y,z,
                 initialDirection=0):
        self.initialX=x
        self.initialY=y
        self.initialZ=z
        self.initialDistanceLength = 30       
        self.previousDistanceLength = 10
        self.expandNext=False
        self.expansionFactor=1
        self.previousDirection=initialDirection
        self.currentX = x
        self.currentY = y
        self.currentZ = z

    def step(self):
        if self.expandNext:
            self.expandNext = False
            self.expansionFactor+=1
        else:
            self.expandNext=True
        newDirection = (self.previousDirection+90)%360
        newDirection = math.radians(newDirection)
        self.previousDirection=math.degrees(newDirection)
        self.currentX=round(self.currentX+(self.initialDistanceLength*self.expansionFactor)*math.cos(newDirection),2)
        self.currentY=round(self.currentY+(self.initialDistanceLength*self.expansionFactor)*math.sin(newDirection),2)
        return self.currentX,self.currentY,self.currentZ

