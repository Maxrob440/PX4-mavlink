import math

class ParalellSweep:
    def __init__(self,x,y,z):
        self.initialX=x
        self.initialY=y
        self.initialZ=z
        self.maxX=100
        self.maxY=100
        self.stepSize=10
        self.currentX=x
        self.currentY=y
        self.currentZ=z
        self.movedDown = False
        self.initial=True
        print("SUCCESS")
    
    def step(self):
        print("STEP")
        print(self.currentX)
        print(self.initialX+self.maxX)
        print(self.movedDown)
        if self.initial:
            print(1)
            self.initial=False
            self.currentX=self.initialX+self.maxX
            return self.currentX,self.initialY,self.initialZ
        elif abs(self.currentX-(self.initialX+self.maxX))<1 and not self.movedDown:
            print(2)
            self.movedDown=True
            self.currentY=self.currentY-10
            return self.currentX,self.currentY,self.currentZ

        elif abs(self.currentX-(self.initialX+self.maxX))<1 and self.movedDown:
            print(3)
            self.movedDown=False
            self.currentX=self.initialX-self.maxX
            return self.currentX,self.currentY,self.currentZ

        elif abs(self.currentX-(self.initialX-self.maxX))<1 and not self.movedDown:
            print(4)
            self.movedDown=True
            self.currentY=self.currentY-10
            return self.currentX,self.currentY,self.currentZ
 
        elif abs(self.currentX-(self.initialX-self.maxX))<1 and self.movedDown:
            print(5)
            self.movedDown=False
            self.currentX=self.initialX+self.maxX
            return self.currentX,self.currentY,self.currentZ

