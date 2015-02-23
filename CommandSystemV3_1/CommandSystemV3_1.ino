#include <Adafruit_VC0706.h>
#include <SoftwareSerial.h>
/*
SoftwareSerial cameraConnection = SoftwareSerial(2,3);
Adafruit_VC0706 cam = Adafruit_VC0706(&cameraConnection);
*/
//Receiving commands//
#define FORWARD 0x31
#define BACKWARD 0x32
#define RIGHT 0x33
#define LEFT 0x34
#define TAKE_PICTURE 0x35
#define STOP 0x36
#define RANDOM 0x37

//Sending commands//
#define CAMERA_ERROR 0x50
#define PHOTO_READY 0x51
#define STOP_EXECUTED 0x52
#define ACKNOWLEDGED 0x53

const int m1DirPin = 4;
const int m1StepPin = 5;
const int m2DirPin = 7;
const int m2StepPin = 6;
const int ledPin = 9;
const int sleepLeftPin = 10;
const int sleepRightPin = 11;

boolean trip = false;

void setup()
{
  Serial.begin(57600);
  /*
  if(cam.begin()){}
  else 
  {
    Serial.write(CAMERA_ERROR); //Abort if the camera doesn't intialize
    return;
  }
  */
  pinMode(ledPin, OUTPUT);
  pinMode(m1DirPin, OUTPUT);
  pinMode(m1StepPin, OUTPUT);
  pinMode(m2DirPin, OUTPUT);
  pinMode(m2StepPin, OUTPUT);
  pinMode(sleepLeftPin, OUTPUT);
  pinMode(sleepRightPin, OUTPUT);
  Serial.write(ACKNOWLEDGED); //System is online
}
void loop()
{  
  if(Serial.available())
  {
    digitalWrite(sleepLeftPin, HIGH);
    digitalWrite(sleepRightPin, HIGH);
    readCommand();
    Serial.write(ACKNOWLEDGED); // Command executed
    digitalWrite(sleepLeftPin, LOW);
    digitalWrite(sleepRightPin, LOW);
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
      drive(HIGH, commands[i+1]);
      i++;
    }
    else if(commands[i] == BACKWARD)
    {
      drive(LOW, commands[i+1]);
      i++;
    }
    else if(commands[i] == RIGHT)
    {
      turn(HIGH, commands[i+1]);
      i++;
    }
    else if(commands[i] == LEFT)
    {
      turn(LOW, commands[i+1]);
      i++;
    }
    else if (commands[i] == TAKE_PICTURE)
    {
      Serial.write(PHOTO_READY);
      //takePhoto();
    }
    if (trip)
    {
      trip = false;
      break;
    }
  }
}
void drive(int direction, byte distance)
{
  //Serial.println(distance);
  int dist = int(distance)*203;
  //Serial.println(dist);
  
  delayMicroseconds(2);
  digitalWrite(m1DirPin, direction);
  digitalWrite(m2DirPin, direction);
  for(int j = 0; j < dist; j++)
  {
    if (Serial.read() == STOP)
    {
      trip = true;
      Serial.write(ACKNOWLEDGED);
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

void turn(int direction, byte degrees)
{
  int deg = int(degrees)*41; 
  
  delayMicroseconds(2);
  digitalWrite(m1DirPin, direction);
  digitalWrite(m2DirPin, !direction);
  for(int j = 0; j < deg; j++)
  {
    if (Serial.read() == STOP)
    {
      trip = true;
      recenter();
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
/*
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
*/
  
