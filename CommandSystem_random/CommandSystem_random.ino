#include <SoftwareSerial.h>

//Receiving commands//
#define FORWARD 0x31
#define BACKWARD 0x32
#define RIGHT 0x33
#define LEFT 0x34
#define TAKE_PICTURE 0x35
#define STOP 0x36

//Sending commands//
#define CAMERA_ERROR 0x50
#define PHOTO_READY 0x51
#define STOP_EXECUTED 0x52

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

  pinMode(ledPin, OUTPUT);
  pinMode(m1DirPin, OUTPUT);
  pinMode(m1StepPin, OUTPUT);
  pinMode(m2DirPin, OUTPUT);
  pinMode(m2StepPin, OUTPUT);
  pinMode(sleepLeftPin, OUTPUT);
  pinMode(sleepRightPin, OUTPUT);
}
void loop()
{  
  randomize();
}

void drive(int direction, byte distance)
{
  int dist = int(distance)*203;
  
  delayMicroseconds(2);
  digitalWrite(m1DirPin, direction);
  digitalWrite(m2DirPin, direction);
  for(int j = 0; j < dist; j++) //todo: determine distance preset
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

void randomize() 
{
  int choice = random(1,4);
  byte distance = random(1,6);
  digitalWrite(sleepLeftPin, HIGH);
  digitalWrite(sleepRightPin, HIGH);
  if (choice == 1)
  {
    drive(HIGH, distance);
  }
  else if (choice == 2)
  {
    turn(HIGH, distance);
  }
  else if (choice == 3)
  {
    turn(LOW, distance);   
  }
}
void recenter()
{
  Serial.write(STOP_EXECUTED);
  while(!Serial.available());
  byte deg = Serial.read();
  turn(LEFT, deg);
  Serial.write(STOP_EXECUTED);
  while(!Serial.available());
  byte distance = Serial.read();
  drive(FORWARD, distance);
  Serial.write(STOP_EXECUTED);
}
  
