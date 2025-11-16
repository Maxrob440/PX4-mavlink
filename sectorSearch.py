import math
class SectorSearch:
    def __init__(self,x,y,z):
        self.centreX =x
        self.centreY = y
        self.centreZ = z
        self.currentX=x
        self.currentY=y
        self.currentZ=z
        self.currentAngle =0
        self.searchRadius=50
        self.sectorCount = 0
        self.rotationCount=0

    def step(self):
        if self.rotationCount==3:
            self.rotationCount=0
            self.currentAngle=30
            
        if self.sectorCount==0:
            angle=math.radians(self.currentAngle)
            print(angle)
            self.currentX=round(self.currentX+(self.searchRadius)*math.cos(angle),4)
            self.currentY=round(self.currentY+(self.searchRadius)*math.sin(angle),4)
            self.sectorCount+=1
            return self.currentX,self.currentY,self.currentZ

        elif self.sectorCount==1:
            angle=math.radians((self.currentAngle+120)%360)
            print(angle)

            self.currentX=round(self.currentX+(self.searchRadius)*math.cos(angle),4)
            self.currentY=round(self.currentY+(self.searchRadius)*math.sin(angle),4)
            self.sectorCount+=1
            return self.currentX,self.currentY,self.currentZ

        elif self.sectorCount==2:
            self.sectorCount=0
            self.currentAngle=(self.currentAngle+120)%360
            self.currentX=self.centreX
            self.currentY=self.centreY
            self.rotationCount+=1
            return self.centreX,self.centreY,self.centreZ

