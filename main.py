from controller import Controller
def coordinateInput():
    valid = False
    while not valid:
        coords = input("Enter coordinates in form: x,y,z, or press enter to skip: ")
        if not coords:
            valid = True
            x,y,z=-10,-10,10
        else:
            coords=coords.split(",")
            try:
                coords = [int(coord) for coord in coords]
                if len(coords)!=3:raise TypeError  
                x,y,z=coords
                return x,y,z
            except Exception:
                print("Coords invalid")

def main():
    controller = Controller()
    input("Press enter to arm drone...")
    controller.arm()
    input("Press enter to take off...")
    controller.takeOff(5)
    patterns=["EB","SS","FF"]
    pattern = ''
    while pattern.upper() not in patterns:
        pattern = input("Enter search pattern: 'EB': expanding box, 'SS': Sector seach, 'FF': Free flight: ")
    x,y,z=coordinateInput()
    controller.moveTo(x,y,z)
    controller.beginTakePhoto()
    if pattern == "EB":
        controller.createExpandingBox(x,y,z,45)
    elif pattern == "SS":
        controller.createSectorSearch(x,y,z)
    else:
        while True:
            x,y,z=coordinateInput()
            controller.moveTo(x,y,z)
    for x in range(25):
        controller.patternStep()
    controller.setRTL()

main()
