#include <Wire.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define PIXELS 348 // Set this to the number of pixels in yout strip
#define SLAVE_ADDRESS 0x04

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXELS, PIN, NEO_GRB + NEO_KHZ800);

// Timer
unsigned long previousMillis = 0;
long millisLockTime = 60000;

// i2c Config
int number = 0;
int state = 0;

// PIR Config
long calibrationTime = 60000;  // How long the sensors need to calibrate
long unsigned int lowIn;
long unsigned int pause = 5000; // How long time before we assume no motion

  // Sensor 1
int pir1 = 7; // choose the input pin (for First sensor)
int pir1State = LOW;  // we start, assuming no motion detected
int val1 = 0; // variable for reading the pin status
boolean lockLow1 = true;
boolean takeLowTime1;  

  // Sensor 2
int pir2 = 8; // choose the input pin (for Second sensor)
int pir2State = LOW;  // we start, assuming no motion detected  
int val2 = 0; // variable for reading the pin status
boolean lockLow2 = true;
boolean takeLowTime2;  

boolean timeoutHappened = false;
boolean timeoutEnabled = true;

// pixelInt
long pixelInt = 0;

void setup() {

  // Set pins
  pinMode(13, OUTPUT);
  pinMode(pir1, INPUT);
  pinMode(pir2, INPUT);

  // Open Serial port (not really neccesary)
  Serial.begin(9600);

  // Initiate Neopixels
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  // Set all pixels to white
  for (int i = 0; i <= PIXELS; i++) {
      strip.setPixelColor(i, 255, 255, 255);
  }
  strip.show();
  
  //give the sensor some time to calibrate. Animate with neopixels
  Serial.print("calibrating sensor ");
  
  long delayTime = calibrationTime/PIXELS;
  
  for(int i = 0; i < PIXELS; i++){
    strip.setPixelColor(PIXELS-i, 0, 0, 0);
    strip.show();
    
    Serial.print(".");
    delay(delayTime);
  }

  strip.setPixelColor(0, 0, 0, 0);
  strip.show();
  
  Serial.println(" done");
  Serial.println("SENSOR ACTIVE");
  delay(50);

  // Open i2c connection
  Wire.setClock(400000L);
  Wire.begin(SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  // Done booting!
  Serial.println("Ready!");
  
  // Flash once Red
  // flashColor(0, 5, 165, 70);
  
}

void loop() {

      if(!timeoutEnabled) {
      unsigned long currentMillis = millis();

      if (currentMillis-previousMillis >= millisLockTime) {
          for(int j=0; j < PIXELS; j++) {
            if (!timeoutHappened) {
              fadeFromBlack(255, 0, 0, 30);
              timeoutHappened = true;
            }
          }
          strip.show();
      } else {
        timeoutHappened = false;
      }
     }
     // Sensor 1 //
     if(digitalRead(pir1) == HIGH){
       digitalWrite(13, HIGH);   //the led visualizes the sensors output pin state
       number = 2;
       sendData();
       if(lockLow1){  
         //makes sure we wait for a transition to LOW before any further output is made:
         lockLow1 = false;            
         Serial.println("---");
         Serial.print("motion detected at ");
         Serial.print(millis()/1000);
         Serial.println(" sec"); 
         delay(50);
         }         
         takeLowTime1 = true;
       }

     if(digitalRead(pir1) == LOW){       
       digitalWrite(13, LOW);  //the led visualizes the sensors output pin state
       number = 0;
       if(takeLowTime1){
        lowIn = millis();          //save the time of the transition from high to LOW
        takeLowTime1 = false;       //make sure this is only done at the start of a LOW phase
        }
       //if the sensor is low for more than the given pause, 
       //we assume that no more motion is going to happen
       if(!lockLow1 && millis() - lowIn > pause){  
           //makes sure this block of code is only executed again after 
           //a new motion sequence has been detected
           lockLow1 = true;                        
           Serial.print("motion ended at ");      //output
           Serial.print((millis() - pause)/1000);
           Serial.println(" sec");
           delay(50);
           }
       }
      // ./Sensor 1 //



      // Sensor 2 //
       if(digitalRead(pir2) == HIGH){
       digitalWrite(13, HIGH);   //the led visualizes the sensors output pin state
       number = 3;
       sendData();
       if(lockLow2){  
         //makes sure we wait for a transition to LOW before any further output is made:
         lockLow2 = false;            
         Serial.println("---");
         Serial.print("motion detected at ");
         Serial.print(millis()/1000);
         Serial.println(" sec"); 
         delay(50);
         }         
         takeLowTime2 = true;
       }

     if(digitalRead(pir2) == LOW){       
       digitalWrite(13, LOW);  //the led visualizes the sensors output pin state
       number = 0;
       if(takeLowTime2){
        lowIn = millis();          //save the time of the transition from high to LOW
        takeLowTime2 = false;       //make sure this is only done at the start of a LOW phase
        }
       //if the sensor is low for more than the given pause, 
       //we assume that no more motion is going to happen
       if(!lockLow2 && millis() - lowIn > pause){  
           //makes sure this block of code is only executed again after 
           //a new motion sequence has been detected
           lockLow2 = true;                        
           Serial.print("motion ended at ");      //output
           Serial.print((millis() - pause)/1000);
           Serial.println(" sec");
           delay(50);
           }
       }
    // ./Sensor 2 //
}

void receiveData(int byteCount) {
  previousMillis = millis();
  
  digitalWrite(13, HIGH);
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
      flashColor(0, 204, 0, 30);
      break;
      
    case 0x02:
      pixelInt = bytes[2] + bytes[3];
      strip.setPixelColor(pixelInt, bytes[4], bytes[5], bytes[6]);
      break;

     case 0x03:
      strip.show();
      break;

     case 0x04:
      flashColor(bytes[2], bytes[3], bytes[4], bytes[5]);
      break;

     case 0x05:
      timeoutEnabled = false;
      break;

    case 0x06:
      strip.setBrightness(bytes[2]);
      break;

    case 0x07:
      number = 42;
      break;
      
      
    default:
      Serial.println("Nothing New");
      break;
      
  }
  
  digitalWrite(13, LOW);
}

void sendData() {
  previousMillis = millis();
  Wire.write(number);
}

void sendString(int Data) {
  Wire.write(Data);
}

void fadeFromBlack(byte Red, byte Green, byte Blue, long n) {
  byte Rstart=0;
  byte Gstart=0;
  byte Bstart=0;
  byte Rend=Red;
  byte Gend=Green;
  byte Bend=Blue;
 
  for(long i = 0; i < n; i++) // larger values of 'n' will give a smoother/slower transition.
  {
    byte Rnew = Rstart + (Rend - Rstart) * i / n;
    byte Gnew = Gstart + (Gend - Gstart) * i / n;
    byte Bnew = Bstart + (Bend - Bstart) * i / n;
    // set pixel color here
    for(int j=0; j < PIXELS; j++) {
      strip.setPixelColor(j, strip.Color(Rnew, Gnew, Bnew));
    }
    strip.show();
  }
}

void flashColor(byte Red, byte Green, byte Blue, long n) {

  byte Rstart=0;
  byte Gstart=0;
  byte Bstart=0;
  byte Rend=Red;
  byte Gend=Green;
  byte Bend=Blue;
 
  for(long i = 0; i < n; i++) // larger values of 'n' will give a smoother/slower transition.
  {
    byte Rnew = Rstart + (Rend - Rstart) * i / n;
    byte Gnew = Gstart + (Gend - Gstart) * i / n;
    byte Bnew = Bstart + (Bend - Bstart) * i / n;
    // set pixel color here
    for(int j=0; j < PIXELS; j++) {
      strip.setPixelColor(j, strip.Color(Rnew, Gnew, Bnew));
    }
    strip.show();
  }

  Rstart=Red;
  Gstart=Green;
  Bstart=Blue;
  Rend=0;
  Gend=0;
  Bend=0;

  for(long i = 0; i < n; i++) // larger values of 'n' will give a smoother/slower transition.
  {
    byte Rnew = Rstart + (Rend - Rstart) * i / n;
    byte Gnew = Gstart + (Gend - Gstart) * i / n;
    byte Bnew = Bstart + (Bend - Bstart) * i / n;
    // set pixel color here
    for(int j=0; j < PIXELS; j++) {
      strip.setPixelColor(j, strip.Color(Rnew, Gnew, Bnew));
    }
    strip.show();
  }

   for(int i = 0; i < PIXELS; i++) {
        strip.setPixelColor(i, 0, 0, 0);
   }
   strip.show();

}

