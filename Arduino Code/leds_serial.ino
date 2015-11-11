const int redLedPin = 5;      // the pin that the LED is attached to
const int greenLedPin = 6;
const int blueLedPin = 9;
const int whiteLedPin = 10;

void setup()
{
  // initialize the serial communication:
  Serial.begin(9600);
  // initialize the ledPin as an output:
  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(blueLedPin, OUTPUT);
  pinMode(whiteLedPin, OUTPUT);
  int BrightnessValue = 0;
  analogWrite(redLedPin, 255 - BrightnessValue);
  analogWrite(greenLedPin, 255 - BrightnessValue);
  analogWrite(blueLedPin, 255 - BrightnessValue);
  analogWrite(whiteLedPin, 255 - BrightnessValue);
  //Welcome message
  Serial.println("Now you are conected to Led controller");
}

void loop() {
  char data;
  int BrightnessValue = 0;
  // check if data has been sent from the computer:
  if (Serial.available()) {
    // read the most recent byte (which will be from 0 to 255):
    data = Serial.read();
    //Serial.println(data);
    if (data == 'R'){
      BrightnessValue = Serial.parseFloat();
      if (BrightnessValue < 256){
        analogWrite(redLedPin, 255 - BrightnessValue);
        Serial.print("Red LED set to ");
        Serial.println(BrightnessValue);
      } else{
        Serial.println("Error, Exceded value on Red LED, max value 255");
      }
      
    }else if (data == 'G'){
      BrightnessValue = Serial.parseFloat();
      if (BrightnessValue < 256){
        analogWrite(greenLedPin, 255 - BrightnessValue);
        Serial.print("Green LED set to ");
        Serial.println(BrightnessValue);
      } else{
        Serial.println("Error, Exceded value on Green LED, max value 255");
      }
      
    }else if (data == 'B'){
      BrightnessValue = Serial.parseFloat();
      if (BrightnessValue < 256){
        analogWrite(blueLedPin, 255 - BrightnessValue);
        Serial.print("Blue LED set to ");
        Serial.println(BrightnessValue);
      } else{
        Serial.println("Error, Exceded value on Blue LED, max value 255");
      }
      
    }else if (data == 'W'){
      BrightnessValue = Serial.parseFloat();
      if (BrightnessValue < 256){
        analogWrite(whiteLedPin,255 - BrightnessValue);
        Serial.print("White LED set to ");
        Serial.println(BrightnessValue);
      }else{
        Serial.println("Error, Exceded value on White LED, max value 255");
      }
      
    }else if (byte(data)  == 10 || byte(data)  == 13 || byte(data)  == 32){
      Serial.println("Fin datos");
    }else if (data == 'C'){
        delay(100);
       Serial.print("I'm an Arduino ");
    }else{
      Serial.print(byte(data));
      Serial.println(" Error en los datos");
    }
    
  }   
 
  }
