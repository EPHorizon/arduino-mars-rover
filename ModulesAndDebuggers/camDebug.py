from SimpleCV import *

cam = Camera(1)
while True:
    try:
        img = cam.getImage()
        img.save("current.jpg")
        break
    except:
        print("Error taking image")
    
