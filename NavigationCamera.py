from SimpleCV import *

cam = Camera(1)
while True:
    img = cam.getImage()
    img.save("current.png")
