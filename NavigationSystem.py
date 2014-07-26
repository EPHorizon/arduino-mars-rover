from PIL import Image
import time

def firstImage():
    img = Image.open(r"C:\Users\Robert Davis\Desktop\testDark2.jpg")
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
    print("Red")
    print()
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
    print()
    
    return center

start = time.time()
firstImage()


def getCenter(center):
    img = Image.open(r"C:\Users\Robert Davis\Desktop\testDark.jpg")
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
    for x in range(center[0]-125, center[0]+125):
        for y in range(center[1]-125, center[1]+125):
            dot = pixels[x,y]
            
            if dot[0]+dot[1]+dot[2] > 100:
            #if(True):
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
    center = [int((blueLoc[0] + redLoc[0])/2), int((blueLoc[1] + redLoc[1])/2)]
    print("Center location: ", center)
    end = time.time() - start
    print()
    print("Calculation took", end, "Seconds")
    return center

for i in range(1):
    start = time.time()
    getCenter(center)
