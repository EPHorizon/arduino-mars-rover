#include <SoftwareSerial.h>
#include <Cam.h>

SoftwareSerial cam_port = SoftwareSerial(2,3);

CAM camera = CAM();

void setup()
{
  Serial.begin(57600);
  if(camera.setup("VGA", 38400, cam_port))
  {
    Serial.println("Camera initialized");
  }
  else(Serial.println("ERROR"));
  camera.shoot(cam_port);
}
void loop()
{
  //if(Serial.read() == 0x01)
  if(1)
  {
    
  } 
}
