from tkinter import *
import serial, time
from PIL import Image, ImageTk
import threading
CAMERA = True
class Console(Frame):

    def __init__(self):
        self.port = serial.Serial("COM12", 57600)
        
        self.commands = []
        Frame.__init__(self)
        self.master.title("Rover Control")
        self.grid()

        self._viewVar = StringVar()
        self._viewVar.set("")
        self._viewEntry = Entry(self, textvariable = self._viewVar)
        self._viewEntry.grid(row = 5, columnspan = 3)

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

        self._forwardButton.grid(row = 0, column = 1)
        self._backwardButton.grid(row = 2, column = 1)
        self._rightButton.grid(row = 1, column = 2)
        self._leftButton.grid(row = 1, column = 0)
        self._stopButton.grid(row = 1, column = 1)
        self._beginButton.grid(row = 3, column = 2)
        self._undoButton.grid(row = 3, column = 0)
        self._restartButton.grid(row = 3, column = 1)

    def _forward(self):
        self.commands.append(b"\x05")
        self._viewVar.set("Forward 1 ft")
    def _backward(self):
        self.commands.append(b"\x06")
        self._viewVar.set("Backward 1 ft")
    def _right(self):
        self.commands.append(b"\x07")
        self._viewVar.set("Right 45 degrees")
    def _left(self):
        self.commands.append(b"\x08")
        self._viewVar.set("Left 45 degrees")
    def _stop(self):
        self.port.write(b"\x99")
        self._viewVar.set("Aborting")
        self.commands.clear()
    def _begin(self):
        self._viewVar.set("Sending mission data...")
        for i in range(len(self.commands)):
            self.port.write(self.commands[i])
            print(self.commands[i])
        self._viewVar.set("Commands sent")
        self.commands.clear()
        if CAMERA:
            self._imageWait()

    def _undo(self):
        if len(self.commands) > 0:
            self._viewVar.set("Striking Last Entry")
            self.commands.pop()
    def _restart(self):
        self._viewVar.set("")
        self.commands.clear()
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
