#include <Adafruit_VC0706.h>
#include <SoftwareSerial.h>

SoftwareSerial cameraConnection = SoftwareSerial(2,3);
Adafruit_VC0706 cam = Adafruit_VC0706(&cameraConnection);


#define STOP 0x99
#define FORWARD 0x05
#define BACKWARD 0x06
#define RIGHT 0x07
#define LEFT 0x08

#define CAMERA_ERROR 0x98 //todo: decide hex commands


const int m1DirPin = 4;
const int m1StepPin = 5;
const int m2DirPin = 7;
const int m2StepPin = 6;

boolean trip = false;

void setup()
{
  Serial.begin(57600);
  
  if(cam.begin()){}
  else 
  {
    Serial.write(CAMERA_ERROR); //Abort if the camera doesn't intialize
    return;
  }
  
  pinMode(m1DirPin, OUTPUT);
  pinMode(m1StepPin, OUTPUT);
  pinMode(m2DirPin, OUTPUT);
  pinMode(m2StepPin, OUTPUT);
}
void loop()
{  
  if(Serial.available())
  {
    readCommand();
  }
}
void readCommand()
{
  byte commands[100];
  int count = 0;
  while(Serial.available() > 0)
  {
    commands[count] = Serial.read();
    count++;
    delay(100);
  }
  for(int i = 0; i < 100; i++)
  { 
    if(commands[i] == FORWARD)
    {
      drive(1);
    }
    else if(commands[i] == BACKWARD)
    {
      drive(0);
    }
    else if(commands[i] == RIGHT)
    {
      turn(HIGH);
    }
    else if(commands[i] == LEFT)
    {
      turn(LOW);
    }
    if (trip)
    {
      break;
    }
  }
  if (!trip)
  {
    
    for (int i = 0; i < 100; i++)
    {
      Serial.println(commands[i]);
      commands[i] = 0;
    } 
    takePhoto();
  }
  else
  {
    drive(LOW);
    trip = false;
    
  }
  
}
void drive(int direction)
{
  delayMicroseconds(2);
  digitalWrite(m1DirPin, direction);
  digitalWrite(m2DirPin, direction);
  for(int j = 0; j < 3200; j++) //todo: determine distance preset
  {
    if (Serial.read() == STOP)
    {
      trip = true;
      break;
    }
    digitalWrite(m1StepPin,LOW);
    digitalWrite(m2StepPin,LOW);
    delayMicroseconds(2);
    digitalWrite(m1StepPin,HIGH);
    digitalWrite(m2StepPin,HIGH);
    delay(1);
  }
}

void turn(int direction)
{
  delayMicroseconds(2);
  digitalWrite(m1DirPin, direction);
  digitalWrite(m2DirPin, !direction);
  for(int j = 0; j < 1600; j++) //todo: determine turn degrees
  {
    if (Serial.read() == STOP)
    {
      trip = true;
      break;
    }
    digitalWrite(m1StepPin,LOW);
    digitalWrite(m2StepPin,LOW);
    delayMicroseconds(2);
    digitalWrite(m1StepPin,HIGH);
    digitalWrite(m2StepPin,HIGH);
    delay(1);
  }
}

void takePhoto()
{
  cam.takePicture();
  unsigned int jpgLen = cam.frameLength();
  
  while (jpgLen > 0)
  {                     //Send off 32 bytes of data at a time
    byte *buffer;
    byte bytesToRead = min(32, jpgLen);
    buffer = cam.readPicture(bytesToRead);
    Serial.write(buffer, bytesToRead);
    jpgLen -= bytesToRead;
  }
  cam.resumeVideo();
}

