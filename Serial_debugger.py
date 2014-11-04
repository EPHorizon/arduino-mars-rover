import serial

port = serial.Serial("COM12", 57600)
print("Uplink established")

while True:
    x = input("")
    port.write(b"\x36")
    print("Command sent")
##    while port.read() != b"\x52":
##        pass
##    print("input 1 received")
