#include <Adafruit_VC0706.h>
#include <SoftwareSerial.h>

#define chipSelect 10

SoftwareSerial cameraConnection = SoftwareSerial(2,3);

Adafruit_VC0706 cam = Adafruit_VC0706(&cameraConnection);

void setup()
{
  Serial.begin(57600);
  pinMode(8, OUTPUT);
  
  if (cam.begin()){}
  else { return; } //Abort the transfer if camera does not initialize
  
  cam.setImageSize(VC0706_640x480);
  cam.setCompression(8);
}

void loop()
{
  if (Serial.read() == 0x01) //Wait for send command
  {
    snapAndSend();
    cam.reset(); //Needed to clear out cached copy (I think)
  }
}
void snapAndSend()
{
  cam.takePicture();
  uint16_t jpgLen = cam.frameLength();
  
  while (jpgLen > 0)
  {                     //Send off 32 bytes of data at a time
    uint8_t *buffer;
    uint8_t bytesToRead = min(32, jpgLen);
    buffer = cam.readPicture(bytesToRead);
    Serial.write(buffer, bytesToRead);
    jpgLen -= bytesToRead;
  }
}
