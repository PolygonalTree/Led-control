import controlP5.*;
import processing.serial.*; 

//Textarea  data;
int maxPeriods = 10;

//Period[] Periods = new Period[maxPeriods];
Experiment exp;
PFont font;
Serial arduino;
String port;
Boolean alreadyRunning = false;
String time="";
String messages="";
Thread threadArduino;


void setup(){
  size(860,490);
  frameRate(10);
  loadGui();
  font = loadFont("Arial.vlw");
  textFont(font);
  port = detectArduino();
  println(port);
  arduino = new Serial(this, port,9600);
  exp = new Experiment();
  //printGui();
}

void draw(){
  if (exp.size() == 0){
    printGui0();
  }else{
      printGui();
  }
  

//  if (alreadyRunning == false || keyPressed || mouseX != pmouseX || mouseY != pmouseY || mousePressed){
//    printGui();
//  }
  if (alreadyRunning == true ){
     text(time,410,310);
     text(messages,410,330);
    //exp.run(time);
    //delay(10000);
  }else{
    if (messages.indexOf("Ended")>0){
    text(messages,410,330);
    }
  }

}

void keyPressed(){

  if (key == 'Q'){
    alreadyRunning = false;
  }
//  arduinoPort.write(key);
//  println(readData());
}
void mouseMoved() {


}
void mousePressed(){

}
void mouseDragged() {

}
