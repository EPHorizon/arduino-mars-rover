from PIL import Image
import time
import math
import serial

#port = serial.Serial("COM12", 57600)

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

    global center
    center = [int((blueLoc[0] + redLoc[0])/2), int((blueLoc[1] + redLoc[1])/2)]

    if center != [0,0]:
        boundCheck(center)
        
    return center

def direction(initial, final):
    angle = [0,0]
    x = initial[0] - final[0]
    y = (initial[1]- final[1])
    angle = math.degrees(math.atan2(x,y))
    return angle

def boundCheck(ct):
    
    boundary = Image.open(r"C:\Users\Robert Davis\Documents\GitHub\arduino-mars-rover\boundary.png")
    bound = boundary.load() #todo: draw actual boundary case
    if bound[ct[0], ct[1]] == (255, 255, 255, 255):
        print("Out of Bounds!")
        port.write(b"\x36")
        time1 = time.Time()
        while port.read() != b"\x52":
            time2 = time.Time()
            if time2 - time1 > 10:
                print("No feedback received; reattempting connection")
                return
        print("Rover sucessfully stoped")
        print("Calculating angle 1")
        theta1 = direction(firstImage(), [800,600])
        print(theta1)
        theta2 = direction(firstImage(), getYellow(firstImage()))
        print(theta2)
        theta_1st = int(theta1 - theta2)
        print(theta_1st)
        print("Calculating angle 2")
        theta3 = direction(firstImage(), [800,600])
        print(theta3)
        theta4 = direction(firstImage(), getYellow(firstImage()))
        print(theta4)
        theta_2nd = int(theta3 - theta4)
        print(theta_2nd)
        theta = int((theta_1st + theta_2nd) / 2)
        
        if theta < -180:
            theta = theta + 360
        elif theta > 180:
            theta = theta - 360

        if theta < 0:
            port.write(b"\x01")
            time1 = time.Time()
            while port.read() != b"\x52":
                time2 = time.Time()
                if time2 - time1 > 60:
                    print("No feedback received; reattempting connection")
                    return
        else:
            port.write(b"\x00")
            time1 = time.Time()
            while port.read() != b"\x52":
                time2 = time.Time()
                if time2 - time1 > 60:
                    print("No feedback received; reattempting connection")
                    return
        
        theta = abs(theta)
        print(theta)

        port.write(theta.to_bytes(1, "big"))
        time1 = time.Time()    
        while port.read() != b"\x52":
            time2 = time.Time()
            if time2 - time1 > 60:
                print("No feedback received; reattempting connection")
                return
            
        print("Turn executed")
        firstImage()
        dist = int(math.sqrt(math.pow((ct[0] - 800), 2) + math.pow((ct[1] - 600), 2)) / 5)
        print(dist)
        print(dist.to_bytes(1, "big"))
        port.write(dist.to_bytes(1, "big"))
        time1 = time.Time()
        while port.read() != b"\x52":
            time2 = time.Time()
            if time2 - time1 > 60:
                print("No feedback received; reattempting connection")
                return
        print("Resuming normal operations")
        
        firstImage()

def getYellow(ct):
    
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
                     
def main():
    
    while firstImage()[0] + firstImage()[1] < 100:
        print("Rover not found!")    
    while True:
        if getCenter(center) == [0,0]:
            print("Rover Lost!")
            while firstImage() == [0,0]:
                pass
            print("Rover Found!")
        print(center)

main()

