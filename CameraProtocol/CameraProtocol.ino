/*

As of 6/28/14, this can be considered abandoned. Despite my best
efforts, this camera simply refuses to go at any speed higher than
38400 baud. 

Completely recoding the library (this here) allows
for taking an image (albeit with considerable caveats: automatically
caches the image and will no release it, occasionally currupts the
file, etc), but breaks the moment the baud change occurs. 

Modifying the Adafruit library also causes issues, though I am
not sufficient enough at C++ to fully understand why. Adding the
needed functions does nothing noticeable, other than breaking it.

If you are here trying to speed up the VC0706 TTL Camera, I would
advise against it. Not going to happen any time soon.

~Coded by Robert Davis

*/

#include <SoftwareSerial.h>

SoftwareSerial camSerial = SoftwareSerial(2,3);

//Defaults
#define CAM 0x56
#define ZERO 0x00 //Might need to change this
#define ONE 0x01
#define TWELVE 0x0C
#define TEN 0x0A
#define TWO 0x02
#define THREE 0x03
#define FOUR 0x04
#define FIVE 0x05
#define NINETEEN 0x19
#define MAX_BAUD1 0x0D
#define MAX_BAUD2 0xA6
#define TEST 0x0F
//Commands
#define RESET 0x26
#define SIZE 0x34
#define TOGGLE_PICTURE 0x36
#define READ_IMAGE 0x32
#define SET_BAUD 0x24
#define SET_DIMENSIONS 0x31

unsigned short address = 0x0000;
byte incomingbyte;
unsigned short frameptr;
byte bufferLen, cameraBuff[101];

#define START 0x99
#define CAMERA_DELAY 10

union four_bytes
{
  unsigned long sizebytes;
  unsigned char read_byte[2];
}imageSize;

void sendReset();
void freezeImage();
byte* readImage(byte num);
void resumeImage();
unsigned long readImageSize();
void setBaud();
void setImageSize();


void setup()
{
  Serial.begin(57600);
  //Serial.flush();
  
  camSerial.begin(38400);
  delay(1000);
  
  //Serial.println("Resetting camera");
  sendReset();
  clearBytes();
  
  setBaud();
  //clearBytes();
  
  camSerial.end();
  camSerial.begin(115200);
  clearBytes();
  //setImageSize();
  //clearBytes();
  
  
}

void loop()
{
  if (Serial.read() == START)
  //if (1)
  {
    //Serial.println("Toggling frame select");
    toggleImage((byte)ZERO);
    //Serial.println("Clearing bytes");
    clearBytes();
    //Serial.println("Saving image length");
    unsigned long jpgLen = readImageSize();
    //Serial.println(jpgLen);
    while (jpgLen > 0)
    {
      //Serial.println("Sending data");
      byte *buffer;
      byte bytesToRead = min(32, jpgLen);
      buffer = readImage(bytesToRead);
      Serial.write(buffer, bytesToRead);
      jpgLen -= bytesToRead;
    }
    toggleImage(TWO);
    sendReset();
    clearBytes();
  }
}

void clearBytes()
{
  while (camSerial.available() > 0)
  {
    //Serial.println(camSerial.read());
    camSerial.read();
    //Serial.println("ping");
  }
}

void sendReset()
{ 
  byte byteData[] = {CAM, (byte)ZERO, RESET, (byte)ZERO};
  camSerial.write(byteData, 4);
  delay(10);
}

void toggleImage(byte toggle)
{
  frameptr = 0;
  byte byteData[] = {CAM, (byte)ZERO, TOGGLE_PICTURE, ONE, toggle};
  camSerial.write(byteData, 5);
}

unsigned long readImageSize()
{
  //Serial.println("sending commands");
  camSerial.write(CAM);
  camSerial.write((byte)ZERO);
  camSerial.write(SIZE);
  camSerial.write(ONE);
  camSerial.write((byte)ZERO);
  //Serial.println("commands sent, waiting for reply...");
  delay(10);
  while (!camSerial.available());
  //Serial.println("Reply made");
  for (int i = 0; i < 9; i++)
  {
    incomingbyte = camSerial.read();
    
    if (i > 6)
    {
      imageSize.read_byte[8-i] = incomingbyte;
    }
  }
  return imageSize.sizebytes;
}

void setBaud()
{
  byte byteData[] = {CAM, (byte)ZERO, SET_BAUD, THREE, ONE, MAX_BAUD1, MAX_BAUD2};
  camSerial.write(byteData, 7);
}

byte* readImage(byte bytesToRead)
{
  byte timeout = CAMERA_DELAY;
  
  camSerial.write(CAM);
  camSerial.write((byte)ZERO);
  camSerial.write(READ_IMAGE);
  camSerial.write(TWELVE);
  camSerial.write((byte)ZERO); //Frame type
  camSerial.write(TEN);        //Control Mode
  camSerial.write((byte)ZERO); //Starting address
  camSerial.write((byte)ZERO);
  camSerial.write(frameptr >> 8);
  camSerial.write(frameptr & 0xFF);
  camSerial.write((byte)ZERO); //Data length spacers
  camSerial.write((byte)ZERO);
  camSerial.write((byte)ZERO);
  camSerial.write(bytesToRead);//Actual data length
  camSerial.write((byte)(CAMERA_DELAY >> 8)); //Delay
  camSerial.write((byte)(CAMERA_DELAY & 0xFF));
  
  unsigned short counter = 0;
  bufferLen = 0;
  int avail;
  int stripCount = 0;
  
  while ((timeout != counter) && (bufferLen != (bytesToRead+5)))
  {
    avail = camSerial.available();
    if (avail <= 0)
    {
      delay(1);
      counter++;
    }
    if (stripCount < 5)
    {
      camSerial.read();
      stripCount++;
    }
    else
    {
      counter = 0;
      cameraBuff[bufferLen++] = camSerial.read();
      //Serial.println(bufferLen); //tester
    }
  }
  frameptr += bytesToRead;
  
  return cameraBuff;
}
