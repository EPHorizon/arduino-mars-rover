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
#define MAX_BAUD1 0x2A
#define MAX_BAUD2 0xC8
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
  
  //setBaud();
  //clearBytes();
  
  //camSerial.end();
  //camSerial.begin(115200);
  
  //setImageSize();
  //clearBytes();
  
  
}

void loop()
{
  //if (Serial.read() == START)
  //{
    //Serial.println("Toggling frame select");
    toggleImage(ONE);
    //Serial.println("Clearing bytes");
    clearBytes();
    //Serial.println("Saving image length");
    unsigned short jpgLen = readImageSize();
    Serial.println(jpgLen);
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
  //}
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
  /*
  camSerial.write(CAM);
  camSerial.write((byte)ZERO);
  camSerial.write(RESET);
  camSerial.write((byte)ZERO); */
  
  byte byteData[] = {CAM, (byte)ZERO, RESET, (byte)ZERO};
  camSerial.write(byteData, 4);
  delay(10);
}

void toggleImage(byte toggle)
{
  frameptr = 0;
  /*
  camSerial.write(CAM);
  camSerial.write((byte)ZERO);
  camSerial.write(TOGGLE_PICTURE);
  camSerial.write(toggle);
  camSerial.write((byte)ZERO);
  */
  byte byteData[] = {CAM, (byte)ZERO, TOGGLE_PICTURE, toggle, (byte)ZERO};
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

void resumeImage()
{
  camSerial.write(CAM);
  camSerial.write((byte)ZERO);
  camSerial.write(TOGGLE_PICTURE);
  camSerial.write(ONE);
  camSerial.write(THREE);
}

void setImageSize()
{
  camSerial.write(CAM);
  camSerial.write((byte)ZERO);
  camSerial.write(SET_DIMENSIONS);
  camSerial.write(FIVE);
  camSerial.write(FOUR);
  camSerial.write(ONE);
  camSerial.write((byte)ZERO);
  camSerial.write(NINETEEN);
  camSerial.write((byte)ZERO);
}

void setBaud()
{
  camSerial.write(CAM);
  camSerial.write((byte)ZERO);
  camSerial.write(SET_BAUD);
  camSerial.write(THREE);
  camSerial.write(ONE);
  camSerial.write(MAX_BAUD1);
  camSerial.write(MAX_BAUD2);
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
  
  while ((timeout != counter) && (bufferLen != bytesToRead+5))
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
    }
  }
  frameptr += bytesToRead;
  
  return cameraBuff;
}
