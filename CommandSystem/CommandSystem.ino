#define STOP 0x99
#define FORWARD 0x00
#define BACKWARD 0x01
#define RIGHT 0x02
#define LEFT 0x03


const int m1DirPin = 4;
const int m1StepPin = 5;
const int m2DirPin = 7;
const int m2StepPin = 6;

boolean trip = false;

void setup()
{
  Serial.begin(57600);
  
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
  byte commands[10];
  int count = 0;
  while(Serial.available() > 0)
  {
    commands[count] = Serial.read();
    count++;
  }
  for(int i = 0; i < 10; i++)
  {
    if(commands[i] == FORWARD)
    {
      drive(HIGH);
    }
    else if(commands[i] == BACKWARD)
    {
      drive(LOW);
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
    takePhoto();
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
  
}
