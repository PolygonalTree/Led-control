//Pins R,G,B,W
const int ledPins[] = {5,6,9,10};
char data;
int BrightnessValue = 0;
//intensity 0-255, 0-255, 0-255, 0-255, Frecuency of pulses in miliseconds, width of pulse in miliseconds
int lights[] = {0,0,0,0,0,0};
unsigned long t = 0;
unsigned long time = 0;
unsigned long frec =0;
int pW = 0;
boolean pulses = false;
boolean newCommand = false;

void setup()
{
  // initialize the serial communication:
  Serial.begin(9600);
  // initialize the ledPin as an output:

  for (int i=0; i<4;i++){
        pinMode(ledPins[i], OUTPUT);
        analogWrite(ledPins[i],0);
    }
  //Welcome message
  Serial.println("Led controller");
}

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
      //Use F to activate pulses, you need for example F/10/100 for 10 ms pulse every 100 ms 
      lights[4] = Serial.parseInt();
      Serial.println(lights[4]);
      frec =lights[4]*1000.;
      Serial.println(frec);
      lights[5] = Serial.parseInt();
      pulses = true;
      
    }else if (data == 'N'){
      //Use N to stop pulses
      lights[4] = 0;
      lights[5] = 0;
      pulses = false;
      
    //}else if (byte(data)  == 10 || byte(data)  == 13 || byte(data)  == 32){
    //  Serial.println("Fin datos");
    }else if (data == 'C'){
        delay(100);
       Serial.print("Led controller");
    //}else{
     // Serial.println(" Error en los datos");
    //}
    }
  }   
  
  if(pulses == true){
    time = micros();
    if (time>=t){
      t = time+frec;
      
      analogWrite(5,lights[0]);
      analogWrite(6,lights[1]);
      analogWrite(9,lights[2]);
      analogWrite(10,lights[3]);
      delay(lights[5]);
      //c code to switch off
      PORTB = B00000000;
      PORTD = B00000000;
      //Serial.println(micros());
    newCommand= false;
    
    }

  }else if (pulses == false && newCommand == true){
    for (int i=0; i<4;i++){
        analogWrite(ledPins[i],lights[i]);
        newCommand= false;
    }
  }
 
}
