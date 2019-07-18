//Pins R,G,B,W
const int ledPins[] = {5,6,9,10};
char data;
int BrightnessValue = 0;
//intensity 0-255, 0-255, 0-255, 0-255, Frecuency of pulses in miliseconds, width of pulse in miliseconds
float lights[] = {0,0,0,0,0,0,0,0};
unsigned long t = 0;
unsigned long time = 0;
unsigned long frec = 0;
unsigned long error = 0;
unsigned long burst = 0;
unsigned long rest = 0;
unsigned long prevMillis = 0;
unsigned long prevMillisb = 0;
unsigned long currentMillis = 0;
int pW = 0;
boolean pulses = false;
boolean newCommand = false;
volatile int state = LOW;
char act;
int counter = 0;

void setup()
{  
  state = HIGH;
  //attachInterrupt(1,trigger, CHANGE);
  // initialize the serial communication:
  Serial.begin(9600);
  // initialize the ledPin as an output:
  pinMode(2,INPUT);
  for (int i=0; i<4;i++){
        pinMode(ledPins[i], OUTPUT);
        analogWrite(ledPins[i],0);
    }
  //set pulses default parameters
  lights[7] = 2000; //resting time ms
  lights[8] = 10; //pulse of light ms
  //Welcome message
  Serial.println("Led controller");

};

void loop() {

  // check if data has been sent from the computer:
  if (Serial.available()) {
    newCommand = true;
    // read the most recent byte (which will be from 0 to 255):
    data = Serial.read();
    //Serial.println(data);
    if (data == 'R'){
      lights[0] = Serial.parseInt();

      
    }else if (data == 'G'){
      lights[1] = Serial.parseInt();

      
    }else if (data == 'B'){
      lights[2] = Serial.parseInt();

      
    }else if (data == 'W'){
      lights[3] = Serial.parseInt();

    }else if (data == 'F'){
      lights[4] = Serial.parseFloat();
      Serial.print("frec");
      Serial.println(lights[4]);
      frec =lights[4]*1000.;
      //in microseconds
      lights[5] = Serial.parseInt();
      pulses = true;
      prevMillis = micros();
      
    }else if (data == 'N'){
      lights[4] = 0;
      lights[5] = 0;
      pulses = false;
    
    }else if (data == 'I'){
      act = Serial.parseInt();
      Serial.print("I");
      
      if(act == 0){
        detachInterrupt(0); 
        Serial.print("D");
      }else if (act == 1){
        attachInterrupt(0,trigger,CHANGE);
        Serial.print("A");
      }
    
    }else if (data == 'C'){
        delay(100);
       Serial.print("Led controller");
    }
  }     
  
  if(pulses == true && state == true){
    if (lights[4]>=120000){
      time = millis();
      frec = lights[4];
    }else{
      time = micros();
    }
    //time = micros();
    if (time>=t){
      //error 
      error = time-t;
      t = time + frec - error;
      //Serial.println("burst start");
      //burst pulses
      burst=lights[5]*1000.;
      counter = 0;
      currentMillis = micros();
      if (lights[5]>=5000){
        //too slow pulses do not use the locking block
        if (currentMillis - prevMillisb <= burst){
          if (currentMillis - prevMillis >= lights[6]){
              analogWrite(5,lights[0]);
              analogWrite(6,lights[1]);
              analogWrite(9,lights[2]);
              analogWrite(10,lights[3]);
              delay(lights[7]); //pulse 
              analogWrite(5,0);
              analogWrite(6,0);
              analogWrite(9,0);
              analogWrite(10,0);
              prevMillis = currentMillis;
            } 
          }
      }else{
        //if the pulse is short use this locking block
        while(micros()<=burst){
          analogWrite(5,lights[0]);
          analogWrite(6,lights[1]);
          analogWrite(9,lights[2]);
          analogWrite(10,lights[3]);
          delay(lights[7]); //pulse 
          analogWrite(5,0);
          analogWrite(6,0);
          analogWrite(9,0);
          analogWrite(10,0);
          delay(lights[6]); //resting delay
          counter += 1;
        }
      }
      //c code to switch off
      //PORTB = B00000000;
      //PORTD = B00000000;
      //Serial.println(micros());
      //Serial.println("burst end");
      //Serial.print("total time in burst");
      //Serial.println(burst-(lights[5]*1000.));
      //Serial.println(counter);
    newCommand= false;
    
    }

  }else if (pulses == false && newCommand == true){
    if(state == true){
      for (int i=0; i<4;i++){
          analogWrite(ledPins[i],lights[i]);
          newCommand= false;
      }
    }else if(state == false){
      for (int i=0; i<4;i++){
          digitalWrite(ledPins[i],0);
          newCommand= false;
        }
      } 
   }
}

void trigger()
{
  state = ! state;
  //state = false;
  newCommand= true;
}
