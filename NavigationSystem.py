from PIL import Image
import time
import math

def firstImage():
    print("--------------------1--------------------")
    img = Image.open(r"C:\Users\Robert Davis\Pictures\Rover Files\navPics\1.jpg")
    pixels = img.load()

    redRatio = 0
    maxRed = 0
    redLoc = [0,0]
    blueRatio = 0
    maxBlue = 0
    blueLoc = [0,0]
    greenRatio = 0
    maxGreen = 0
    greenLoc = [0,0]
    for x in range(1600):
        for y in range(1200):
            dot = pixels[x,y]
            if dot[0]+dot[1]+dot[2] > 100:
                redRatio = dot[0]/(dot[1]+dot[2]+1)
                if  redRatio > maxRed:
                    maxRed = redRatio
                    redLoc = [x,y]
                blueRatio = dot[2]/(dot[0]+dot[1]+1)
                if blueRatio > maxBlue:
                    maxBlue = blueRatio
                    blueLoc = [x,y]
                greenRatio = dot[1]/(dot[0]+dot[2]+1)
                if greenRatio > maxGreen:
                    maxGreen = greenRatio
                    greenLoc = [x,y]
    print()
    print("Red")
    print("Maximum red ratio: ", maxRed)
    print("At location: ", redLoc)
    print("Pixel RGB levels: ", pixels[redLoc[0], redLoc[1]])
    print()

    print("Blue")
    print("Maximum blue ratio: ", maxBlue)
    print("At location: ", blueLoc)
    print("Pixel RGB levels: ", pixels[blueLoc[0], blueLoc[1]])
    print()
    
    global center
    center = [int((blueLoc[0] + redLoc[0])/2), int((blueLoc[1] + redLoc[1])/2)]
    print("Center location: ", center)

    end = time.time() - start
    print()
    print("Calculation took", end, "Seconds")
    print()
    
    return center

start = time.time()
firstImage()


def getCenter(ct, image):
    img = Image.open(r"C:\Users\Robert Davis\Pictures\Rover Files\navPics\%i.jpg" %image)
    
    pixels = img.load()
    
    redRatio = 0
    maxRed = 0
    redLoc = [0,0]
    blueRatio = 0
    maxBlue = 0
    blueLoc = [0,0]
    greenRatio = 0
    maxGreen = 0
    greenLoc = [0,0]
    
    for x in range(ct[0]-125, ct[0]+125):
        for y in range(ct[1]-125, ct[1]+125):
            dot = pixels[x,y]
            if dot[0]+dot[1]+dot[2] > 100:
                redRatio = dot[0]/(dot[1]+dot[2]+1)
                if  redRatio > maxRed:
                    maxRed = redRatio
                    redLoc = [x,y]
                blueRatio = dot[2]/(dot[0]+dot[1]+1)
                if blueRatio > maxBlue:
                    maxBlue = blueRatio
                    blueLoc = [x,y]
                greenRatio = dot[1]/(dot[0]+dot[2]+1)
                if greenRatio > maxGreen:
                    maxGreen = greenRatio
                    greenLoc = [x,y]
                    
    print("--------------------%i--------------------" %image)
    print()
    print("Red")
    print("Maximum red ratio: ", maxRed)
    print("At location: ", redLoc)
    print("Pixel RGB levels: ", pixels[redLoc[0], redLoc[1]])
    print()

    print("Blue")
    print()

    print("Maximum blue ratio: ", maxBlue)
    print("At location: ", blueLoc)
    print("Pixel RGB levels: ", pixels[blueLoc[0], blueLoc[1]])
    print()
    global center
    center = [int((blueLoc[0] + redLoc[0])/2), int((blueLoc[1] + redLoc[1])/2)]
    print("Center location: ", center)
    end = time.time() - start
    print()
    print("Calculation took", end, "Seconds")
    boundary = Image.open(r"C:\Users\Robert Davis\Desktop\boundTest5.png")
    bound = boundary.load()
    if bound[center[0], center[1]] == (255, 255, 255, 255):
        print("Out of Bounds!")
    else:
        print("All good")
    return center

def direction(initial, final):
    x = final[0] - initial[0]
    y = -1*(final[1] - initial[1]) #negative is because the orgin starts upper
    angle = math.atan2(y, x)       #lefthand corner, with y downwards
    #return angle
    if angle <= math.pi/4 or angle >= 7*math.pi/4:
        return "E"
    if angle <= 3*math.pi/4 and angle >= math.pi/4:
        return "N"
    if angle <= 5*math.pi/4 and angle >= 3*math.pi/4:
        return "W"
    if angle <= 7*math.pi/4 and angle >= 5*math.pi/4:
        return "S"
def getYellow(ct, image):
    img = Image.open(r"C:\Users\Robert Davis\Pictures\Rover Files\navPics\%i.jpg" %image)
    pixels = img.load()

    yellowRatio = 0
    maxYellow = 0
    yellowLoc = [0,0]
    
    for x in range(ct[0]-125, ct[0]+125):
        for y in range(ct[1]-125, ct[1]+125):
            dot = pixels[x,y]
            if dot[0]+dot[1]+dot[2] > 100:
                yellowRatio = (dot[0]+dot[1])/(dot[2]+1)
                if  yellowRatio > maxYellow:
                    maxYellow = yellowRatio
                    yellowLoc = [x,y]
    return yellowLoc

for i in range(19):
    start = time.time()
    getCenter(center, i+2)

##start1 = getCenter(center, 8)
##end = getCenter(center, 9)
##print(direction(start1, getYellow(center, 8)))
##print(getYellow(center, 8))


