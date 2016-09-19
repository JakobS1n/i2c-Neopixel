#include <Wire.h>
#include <Adafruit_NeoPixel.h>


#define PIN 3
#define SLAVE_ADDRESS 0x04

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(10, PIN, NEO_GRB + NEO_KHZ800);

int number = 0;
int state = 0;

void setup() {
  
  pinMode(13, OUTPUT);
  Serial.begin(9600);

  Wire.begin(SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  
  Serial.println("Ready!");
  
}

void loop() {
   delay(100);
}

void receiveData(int byteCount) {
  int bytes[byteCount];
  int i = 0;
  
  while (Wire.available()) {
    number = Wire.read();
    bytes[i] = number;
    
    Serial.println(number); 
    i++;
  }

  switch (bytes[0]) {
    
    case 0x01:
      Serial.println("Life is discovered");
      number = 1;
      break;

    case 0x02:
      /*long byteN = bytes[1];
      int byteState = bytes[2];
      int byteGreen = bytes[3];
      int byteRed = bytes[4];
      int byteBlue = bytes[5];*/
      Serial.println("0x02");

      strip.setPixelColor(bytes[2], bytes[3], bytes[4], bytes[5]);
      Serial.println(bytes[1]);
      Serial.println(bytes[2]);
      Serial.println(bytes[3]);
      Serial.println(bytes[4]);
      break;

     case 0x03:
      strip.show();
      break;

    default:
      Serial.println("Nothing New");
      break;
      
  }
  
}

void sendData() {
  Wire.write(number);
}

void sendString(int Data) {
  Wire.write(Data);
}


