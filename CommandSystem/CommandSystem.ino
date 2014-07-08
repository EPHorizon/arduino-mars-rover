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
#define PHOTO_READY 0x97
#define STOP_EXECUTED 0x90

const int m1DirPin = 4;
const int m1StepPin = 5;
const int m2DirPin = 7;
const int m2StepPin = 6;
const int ledPin = 9;

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
  pinMode(ledPin, OUTPUT);
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
  byte commands[50]; //arbirary limit
  int count = 0;
  
  for (int i = 0; i < 50; i++) //initialize the array/clean it
  {
    commands[i] = 0;
  }
  while(Serial.available())
  {
    commands[count] = Serial.read();
    count++;
    delay(100);
  }
  for(int i = 0; i < 50; i++)
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
      Serial.write(STOP_EXECUTED);
      break;
    }
  }
  if (!trip)
  {
    Serial.write(PHOTO_READY);
    takePhoto();
  }
  else
  {
    trip = false;
  }
  
}
void drive(int direction)
{
  delayMicroseconds(2);
  digitalWrite(m1DirPin, direction);
  digitalWrite(m2DirPin, direction);
  for(int j = 0; j < 1600; j++) //todo: determine distance preset
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
  for(int j = 0; j < 425; j++) //todo: determine turn degrees
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
  digitalWrite(ledPin, HIGH);
  delay(500);
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
  digitalWrite(ledPin, LOW);
  cam.resumeVideo();
}

