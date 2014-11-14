from PIL import Image
import time
import math
import serial

port = serial.Serial("COM12", 57600)

def firstImage():
    while True:
        
        try:
            img = Image.open(r"C:\Users\Robert Davis\Documents\GitHub\arduino-mars-rover\current.jpg")
            pixels = img.load()
            break
        except:
            pass
        
    

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
    
    global center
    center = [int((blueLoc[0] + redLoc[0])/2), int((blueLoc[1] + redLoc[1])/2)]
    return center




def getCenter(ct):
    while True:
        try:
            img = Image.open(r"C:\Users\Robert Davis\Documents\GitHub\arduino-mars-rover\current.jpg")
            pixels = img.load()
            break
        except:
            pass
    
    
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
    global center
    center = [int((blueLoc[0] + redLoc[0])/2), int((blueLoc[1] + redLoc[1])/2)]
    
    boundary = Image.open(r"C:\Users\Robert Davis\Documents\GitHub\arduino-mars-rover\boundary.png")
    bound = boundary.load() #todo: draw actual boundary case
    if bound[center[0], center[1]] == (255, 255, 255, 255):
        print("Out of Bounds!")
        port.write(b"\x36")
        while port.read() != b"\x52":
            pass
        print("input 1 received")
        for i in range(4):
            data = direction([800, 600], getYellow(firstImage()))
            direction0 = data[0]
            port.write(direction0.to_bytes(1, "big"))
            while port.read() != b"\x52":
                pass
            deg = int(data[1] * (180/math.pi))
            print(deg)
            port.write(deg.to_bytes(1, "big"))
            while port.read() != b"\x52":
                pass

        
        print("input 2 received")
        dist = int(math.sqrt(math.pow((center[0] - 800), 2) + math.pow((center[1] - 600), 2)) / 5)
        print(dist)
        print(dist.to_bytes(1, "big"))
        #todo: need to find what the conversion from pixels to inches is
        port.write(dist.to_bytes(1, "big"))
        while port.read() != b"\x52":
            pass
        print("input 3 received")
        #todo: maybe send this command to another function call
        firstImage()

        
    return center

def direction(initial, final):
    angle = [0,0]
    x = final[0] - initial[0]
    y = -1*(final[1] - initial[1]) #negative is because the orgin starts upper
    angle[1] = math.atan2(y, x)       #lefthand corner, with y downwards
    
    if angle[1] >= 0:
        angle[0] = 1
        print(angle)
        return angle
    else:
        angle[0] = 0
        angle[1] = abs(angle[1])
        print(angle)
        return angle    #This output depends on what they want

    if angle <= math.pi/4 or angle >= 7*math.pi/4:
        return "E"
    if angle <= 3*math.pi/4 and angle >= math.pi/4:
        return "N"
    if angle <= 5*math.pi/4 and angle >= 3*math.pi/4:
        return "W"
    if angle <= 7*math.pi/4 and angle >= 5*math.pi/4:
        return "S"
def getYellow(ct):  #todo: once a green led is added, change to that
    while True:
        try:
            img = Image.open(r"C:\Users\Robert Davis\Documents\GitHub\arduino-mars-rover\current.jpg")
            pixels = img.load()
            break
        except:
            print("Error reading image file")

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

##for i in range(19):
##    start = time.time()
##    getCenter(center, i+2)

##start1 = getCenter(center, 8)
##end = getCenter(center, 9)
##print(direction(start1, getYellow(center, 8)))
##print(getYellow(center, 8))

def main():
    while firstImage() == 0:
        pass
    while True:
        if getCenter(center) == 0:
            print("Error reading image file")
        print(center)
main()


