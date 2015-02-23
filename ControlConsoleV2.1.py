from tkinter import *
import serial, time, math, random
from PIL import Image, ImageTk
import threading
CAMERA = True
class Console(Frame):

    def __init__(self):
        #self.port = serial.Serial("COM3", 57600)

        self.fwState = True
        self.bwState = True
        self.rtState = True
        self.ltState = True
        self.firstPress = True
        self.pressCount = 0
        self.commands = []
        Frame.__init__(self)
        self.master.title("Rover Control")
        self.grid()

        self._viewVar = StringVar()
        self._viewVar.set("")
        self._viewEntry = Entry(self, textvariable = self._viewVar)
        self._viewEntry.grid(row = 5, columnspan = 3)

        self._randomVar = IntVar()
        
        self._randomToggle = Checkbutton(self, text = "Random Toggle", \
                                         variable = self._randomVar, \
                                         command = self._randomControl)
        self._forwardButton = Button(self, text = "Forward", \
                                     command = self._forward)
        self._backwardButton = Button(self, text = "Backward", \
                                       command = self._backward)
        self._rightButton = Button(self, text = "Right", \
                                   command = self._right)
        self._leftButton = Button(self, text = "Left", \
                                  command = self._left)
        self._stopButton = Button(self, text = "Abort", \
                                  command = self._stop)
        self._beginButton = Button(self, text = "Begin Mission", \
                                   command = self._begin)
        self._undoButton = Button(self, text = "Undo", \
                                  command = self._undo)
        self._restartButton = Button(self, text = "Start Over", \
                                     command = self._restart)
        self._pictureButton = Button(self, text = "Take Picture", \
                                     command = self._takePicture)

        self._forwardButton.grid(row = 0, column = 1)
        self._backwardButton.grid(row = 2, column = 1)
        self._rightButton.grid(row = 1, column = 2)
        self._leftButton.grid(row = 1, column = 0)
        self._randomToggle.grid(row = 2, column = 0)
        self._stopButton.grid(row = 1, column = 1)
        self._beginButton.grid(row = 3, column = 2)
        self._undoButton.grid(row = 3, column = 0)
        self._restartButton.grid(row = 3, column = 1)
        self._pictureButton.grid(row = 2, column = 2)

    def _forward(self):
        self.bwState = True
        self.ltState = True
        self.rtState = True
        if self.fwState:
            if not self.firstPress:
                self.commands.append(self.pressCount.to_bytes(1, "big"))
            self.commands.append(b"\x31")
            self._viewVar.set("Forward cm")
            self.pressCount = 1
            self.fwState = False
            self.firstPress = False
        else:
            self.pressCount+=1
        
    def _backward(self):
        self.fwState = True
        self.ltState = True
        self.rtState = True
        
        if self.bwState:
            if not self.firstPress:
                self.commands.append(self.pressCount.to_bytes(1, "big"))
            self.commands.append(b"\x32")
            self._viewVar.set("Backward cm")
            self.pressCount = 1
            self.bwState = False
            self.firstPress = False
        else:
            self.pressCount += 1
    def _right(self):
        self.fwState = True
        self.bwState = True
        self.ltState = True
        if self.rtState:
            if not self.firstPress:
                self.commands.append(self.pressCount.to_bytes(1, "big"))
            self.commands.append(b"\x33")
            self._viewVar.set("Right 15 degrees")
            self.pressCount = 15
            self.rtState = False
            self.firstPress = False
        else:
            self.pressCount += 15
            
    def _left(self):
        self.fwState = True
        self.bwState = True
        self.rtState = True
        if self.ltState:
            if not self.firstPress:
                self.commands.append(self.pressCount.to_bytes(1, "big"))
            self.commands.append(b"\x34")
            self._viewVar.set("Left 15 degrees")
            self.pressCount = 15
            self.ltState = False
            self.firstPress = False
        else:
            self.pressCount += 15
    def _takePicture(self):
        if not self.firstPress:
            self.commands.append(self.pressCount.to_bytes(1, "big"))
        self.commands.append(b"\x35")
        self._viewVar.set("Take Picture")
    def _stop(self):
        self.port.write(b"\x36")
        self._viewVar.set("Aborting")
        self.commands.clear()
    def _random(self):
        while self._randomVar.get():
            print("Random Mode Enabled")
            while self.firstImage()[0] + self.firstImage()[1] < 100:
                print("Rover not found!")    
            while self._randomVar.get():
                if self.port.read() == b"\x53":
                    self.command = random.randint(49,52)
                    self.distance = random.randint(15,90)
                    self.port.write(self.command.to_bytes(1,"big"))
                    self.port.write(self.distance.to_bytes(1,"big"))
                
                if self.getCenter(center) == [0,0]:
                    print("Rover Lost!")
                    while self.firstImage() == [0,0]:
                        pass
                    print("Rover Found!")
                print(center)
        print("Random Mode Disabled")
        return
    def _randomControl(self):
        self.locationFinder = threading.Thread(target = self._random)
        self.locationFinder.start()
        
    def firstImage(self):
        while True:   
            try:
                self.img = Image.open(r"C:\Users\dklebe\Desktop\Rover\Navigation\current.jpg")
                self.pixels = self.img.load()
                break
            except:
                pass
            
        self.redRatio = 0
        self.maxRed = 0
        self.redLoc = [0,0]
        self.blueRatio = 0
        self.maxBlue = 0
        self.blueLoc = [0,0]

        for x in range(1600):
            for y in range(1200):
                self.dot = self.pixels[x,y]
                if self.dot[0]+self.dot[1]+self.dot[2] > 100:
                    self.redRatio = self.dot[0]/(self.dot[1]+self.dot[2]+1)
                    if  self.redRatio > self.maxRed:
                        self.maxRed = self.redRatio
                        self.redLoc = [x,y]
                    self.blueRatio = self.dot[2]/(self.dot[0]+self.dot[1]+1)
                    if self.blueRatio > self.maxBlue:
                        self.maxBlue = self.blueRatio
                        self.blueLoc = [x,y]

        global center
        center = [int((self.blueLoc[0] + self.redLoc[0])/2), int((self.blueLoc[1] + self.redLoc[1])/2)]
        print(center)
        return center

    def getCenter(self, ct):
        while True:
            try:
                self.img = Image.open(r"C:\Users\dklebe\Desktop\Rover\Navigation\current.jpg")
                self.pixels = self.img.load()
                break
            except:
                pass
        
        self.redRatio = 0
        self.maxRed = 0
        self.redLoc = [0,0]
        self.blueRatio = 0
        self.maxBlue = 0
        self.blueLoc = [0,0]
        for x in range(ct[0]-125, ct[0]+125):
            for y in range(ct[1]-125, ct[1]+125):
                self.dot = self.pixels[x,y]
                if self.dot[0]+self.dot[1]+self.dot[2] > 100:
                    self.redRatio = self.dot[0]/(self.dot[1]+self.dot[2]+1)
                    if  self.redRatio > self.maxRed:
                        self.maxRed = self.redRatio
                        self.redLoc = [x,y]
                    self.blueRatio = self.dot[2]/(self.dot[0]+self.dot[1]+1)
                    if self.blueRatio > self.maxBlue:
                        self.maxBlue = self.blueRatio
                        self.blueLoc = [x,y]

        global center
        center = [int((self.blueLoc[0] + self.redLoc[0])/2), int((self.blueLoc[1] + self.redLoc[1])/2)]
        print(center)
        if center != [0,0]:
            self.boundCheck(center)
            
        return center

    def direction(self, initial, final):
        self.angle = [0,0]
        self.x = initial[0] - final[0]
        self.y = (initial[1]- final[1])
        self.angle = math.degrees(math.atan2(self.x,self.y))
        return self.angle

    def boundCheck(self, ct):
        
        self.boundary = Image.open(r"C:\Users\dklebe\Desktop\Rover\Navigation\boundary.png")
        self.bound = self.boundary.load() #todo: draw actual boundary case
        if self.bound[ct[0], ct[1]] == (255, 255, 255, 255):
            print("Out of Bounds!")
            self.port.write(b"\x36")
            self.time1 = time.time()
            print(self.time1)
            while self.port.read() != b"\x53":
                self.time2 = time.time()
                if self.time2 - self.time1 > 10:
                    print("No feedback received; reattempting connection")
                    return
            print("Rover sucessfully stoped")
            print("Calculating angle 1")
            self.theta1 = self.direction(self.firstImage(), [800,600])
            #print(self.theta1)
            self.theta2 = self.direction(self.firstImage(), self.getYellow(self.firstImage()))
            #print(self.theta2)
            self.theta_1st = int(self.theta1 - self.theta2)
            print(self.theta_1st)
            print("Calculating angle 2")
            self.theta3 = self.direction(self.firstImage(), [800,600])
            #print(self.theta3)
            self.theta4 = self.direction(self.firstImage(), self.getYellow(self.firstImage()))
            #print(self.theta4)
            self.theta_2nd = int(self.theta3 - self.theta4)
            print(self.theta_2nd)
            self.theta = int((self.theta_1st + self.theta_2nd) / 2)
            
            if self.theta < -180:
                self.theta = self.theta + 360
            elif self.theta > 180:
                self.theta = self.theta - 360

            if self.theta < 0:
                self.port.write(b"\x34")
            else:
                self.port.write(b"\x33")
            
            self.theta = abs(self.theta)
            print("Final Angle: ", self.theta)

            self.port.write(self.theta.to_bytes(1, "big"))
            self.time1 = time.time()    
            while self.port.read() != b"\x53":
                self.time2 = time.time()
                if self.time2 - self.time1 > 60:
                    print("No feedback received; reattempting connection")
                    return
                
            print("Turn executed")
            self.firstImage()
            self.dist = int(math.sqrt(math.pow((ct[0] - 800), 2) + math.pow((ct[1] - 600), 2)) / 5)
            print(self.dist)
            self.port.write(b"\x31")
            self.port.write(self.dist.to_bytes(1, "big"))
            self.time1 = time.time()
            while self.port.read() != b"\x53":
                self.time2 = time.time()
                if self.time2 - self.time1 > 60:
                    print("No feedback received; reattempting connection")
                    return
            print("Resuming normal operations")
            
            self.firstImage()

    def getYellow(self, ct):
        
        while True:
            try:
                self.img = Image.open(r"C:\Users\dklebe\Desktop\Rover\Navigation\current.jpg")
                print("Image oppened")
                self.pixels = self.img.load()
                break
            except:
                print("Error reading image file")

        self.yellowRatio = 0
        self.maxYellow = 0
        self.yellowLoc = [0,0]
        
        for x in range(ct[0]-125, ct[0]+125):
            for y in range(ct[1]-125, ct[1]+125):
                self.dot = self.pixels[x,y]
                if self.dot[0]+self.dot[1]+self.dot[2] > 100:
                    self.yellowRatio = (self.dot[0]+self.dot[1])/(self.dot[2]+1)
                    if  self.yellowRatio > self.maxYellow:
                        self.maxYellow = self.yellowRatio
                        self.yellowLoc = [x,y]
        return self.yellowLoc
         
        
    def _begin(self):
        self.fwState = True
        self.bwState = True
        self.rtState = True
        self.ltState = True
        self.firstPress = True
        self._viewVar.set("Sending mission data...")
        for i in range(len(self.commands)):
            self.port.write(self.commands[i])
            print(self.commands[i])
        self.port.write(self.pressCount.to_bytes(1, "big"))
        print(self.pressCount.to_bytes(1, "big"))
        self._viewVar.set("Commands sent")
        self.commands.clear()
        print()
        if CAMERA:
            self._imageWait()
    def _undo(self):
        if len(self.commands) > 0:
            self._viewVar.set("Striking Last Entry")
            self.commands.pop()
            self.pressCount = 0
    def _restart(self):
        self._viewVar.set("")
        self.commands.clear()
        self.pressCount = 0
    def _getImage(self):
        print("displaying image")
        image = Image.open("imageTest.jpg")
        photo = ImageTk.PhotoImage(image)

        top = Toplevel()
        top.title("Collected Image")

        label = Label(top, image = photo)
        label.image = photo
        label.grid()
        
    def _imageWait(self):
        imageLoader = threading.Thread(target = self._imageReceiver)
        imageLoader.start()

    def _imageReceiver(self):
        while True:
            command = self.port.read()
            if command == b"\x97":
        
                print("opening file")
                file = open("imageTest.jpg", "wb")
                time1 = time.time()
                while True:
                    if self.port.inWaiting():
                        file.write(self.port.read())
                        time1 = time.time()
                    else:
                        time2 = time.time()
                        if (time2 - time1) > 1:
                            print("file transfer complete")
                            file.close()
                            self._getImage()
                            return
            elif command == b"\x90":
                return

    
def main():
    Console().mainloop()

main()
            
        
