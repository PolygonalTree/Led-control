class Experiment {
 // Period[] exp;
  
  ArrayList exp;

  Experiment(){
    exp = new ArrayList();
    //exp = new Period[maxPeriods];
  }
  
//  Period get(int position){
//    return exp.get(position);
//  }
  
  void save(){
    PrintWriter output;    
     output = createWriter("experiment"+str(day())+str(hour())+str(minute())+".txt");
     println("documento salvado");
     for (int i = 0; i<exp.size(); i++){
       Period period = (Period) exp.get(i);
         output.println(period.time+
                         ","+period.isIntervalHours+  
                         ","+period.repetitions+
                         ","+period.ledColour[0]+
                         ","+period.ledColour[1]+
                         ","+period.ledColour[2]+
                         ","+period.ledColour[3]+ 
                         ","+period.switchOnTime[0]+
                         ","+period.switchOnTime[1]+
                         ","+period.switchOffTime[0]+
                         ","+period.switchOffTime[1]+
                         ","+period.isAlwaysOn+
                         ","+period.isAlwaysOff);               
       //}
     }
     output.flush();
     output.close();
     println("documento salvado");
     
  }
  void open(String file){
    String[] lines = loadStrings(file);
    for (int i = 0; i<lines.length; i++){
      String[] pieces = split(lines[i],",");
      println(pieces);
      int time = int(pieces[0]);
      boolean isIntervalHours = boolean(pieces[1]);
      int repetitions= int(pieces[2]);
      int[]ledColour ={int(pieces[3]),int(pieces[4]),int(pieces[5]),int(pieces[6])};
      int[]switchOnTime ={int(pieces[7]),int(pieces[8])};
      int[]switchOffTime ={int(pieces[9]),int(pieces[10])};
      boolean isAlwaysOn = boolean(pieces[11]);
      boolean isAlwaysOff = boolean(pieces[12]);
       
     exp.add(new Period(time, isIntervalHours, repetitions, ledColour, switchOnTime, switchOffTime, isAlwaysOn, isAlwaysOff));
     
    }
    
    this.update();
  }

  void order(){
  }
  
  void delete(int position){
    exp.remove(position);
    
  }
  void update(){
    String s = "";
     for (int i = 0; i<exp.size(); i++){
       Period period = (Period) exp.get(i);
       char interval= 'h';
       if (period.isIntervalHours == false){
         interval = 'm';
       }
       String mode = "LD";
       if (period.isAlwaysOn == true){
         mode = "LL";
       }else if(period.isAlwaysOff == true){
         mode = "DD";
       }
       if (i== 0 && interval == 'm'){
        s = "No Adjustement";
       }else{
         s = i+": Duration="+period.time+interval+
                " | Repetitions="+period.repetitions+
                " | R="+period.ledColour[0]+
                " G="+period.ledColour[1]+
                " B="+period.ledColour[2]+
                " W="+period.ledColour[3]+
                " Mode="+mode;
         if (mode == "LD"){
               s += " | On="+nf(period.switchOnTime[0],2)+":"+nf(period.switchOnTime[1],2)+
                " | Off="+nf(period.switchOffTime[0],2)+ ":"+nf(period.switchOffTime[1],2);
         }
       }
       fill(0);
       text(s,410,30+i*12);
       noFill();
       if (gui.get(Button.class,"deletePeriod"+nf(i,3)) == null){
         addDeleteButton(i);
       }
      
    }
  }
 void set(){  
    int time;
    boolean isIntervalHours;
    int repetitions;
    String sOnTime;
    String sOffTime;  
    boolean isAlwaysOn=false;
    boolean isAlwaysOff=false;
    
    time = int(gui.get(Textfield.class,"durationTextArea").getText());  
    isIntervalHours = boolean(int(gui.get(RadioButton.class,"durationRadioButton").getValue()));  
    println(isIntervalHours);
    repetitions = int(gui.get(Textfield.class,"repetitionsTextArea").getText());
    int [] colours = {int(gui.get(Textfield.class,"colorRedTextArea").getText()),
              int(gui.get(Textfield.class,"colorGreenTextArea").getText()),
              int(gui.get(Textfield.class,"colorBlueTextArea").getText()),
              int(gui.get(Textfield.class,"colorWhiteTextArea").getText())};
    sOnTime = gui.get(Textfield.class,"switchOnTextArea").getText();
    sOffTime = gui.get(Textfield.class,"switchOffTextArea").getText();
    if (gui.get(RadioButton.class,"switchOnRadioButton").getState("LL") == true){
      isAlwaysOn=true;
      println("alw LL");
    }else if(gui.get(RadioButton.class,"switchOnRadioButton").getState("DD")== true){
      isAlwaysOff = true;
      println("alw DD");
    }
    int[] on = int(split(sOnTime, ':'));
    int[] off = int(split(sOffTime,":"));  
  
    //exp[i] = new Period(time, repetitions, colours, on, off);
    exp.add( new Period(time,isIntervalHours, repetitions, colours, on, off, isAlwaysOn, isAlwaysOff));
  }

  int size(){
    return exp.size();
  }
  
  Period get(int i){
    return (Period) exp.get(i);
  }
  

}


   
void controlEvent(ControlEvent theEvent){
   if(theEvent.isController()){
     if(theEvent.controller().name()=="AddPeriod") {
//        for (int i = 0; i<exp.size(); i++){
//           Period period = (Period) exp.get(i);
             exp.set();
            //println(Periods);
            loop();
            //break;
//          }else if (i == 9){
//             println("Max periods already inserted");
//          }
      // } 
     }
     if(theEvent.controller().name()=="Save") {
        exp.save();
     }
     if(theEvent.controller().name()=="Load") {
       selectFile();
        //exp.open();
     }
      if(theEvent.controller().name().indexOf("deletePeriod") > -1) {
        int i = theEvent.controller().name().indexOf("deletePeriod");
        //recover the number of the period, BE Aware, only works for 0 to 9!
        int periodToDelete = int(theEvent.controller().name().substring(i+12,i+12+3));
        removeDeleteButton(exp.size()-1);
        print(periodToDelete);
        exp.delete(periodToDelete);
      }  
      if (theEvent.controller().name() == "Run" && theEvent.controller().value() == 1.0 ){
        println("run");
        threadArduino = new NewThread();
        threadArduino.setPriority(10);
        alreadyRunning = true;
      }else if(theEvent.controller().name() == "Run" && theEvent.controller().value() == 0.0 && alreadyRunning == true){
        threadArduino.interrupt();
        alreadyRunning = false;
        int[] off={0,0,0,0};
        sendDataToArduino(off);
      }
      if(theEvent.controller().name().indexOf("Colour")> -1 && mousePressed==true){
       float value = theEvent.controller().getValue();
       int i = theEvent.controller().name().indexOf("Colour");
       String name = "color"+theEvent.controller().name().substring(i+6)+"TextArea";
       String v = str(int(value));
       gui.get(Textfield.class, name).setValue(v);
      }
       if(theEvent.controller().name().indexOf("color")> -1 &&
       theEvent.controller().name().indexOf("TextArea")> -1){
       int value =int(theEvent.controller().getStringValue());
       int i = theEvent.controller().name().indexOf("color");
       int j = theEvent.controller().name().indexOf("TextArea");
       String name = "Colour"+theEvent.controller().name().substring(i+5,j);
       gui.get(Slider.class, name).setValue(value);
      }     
      if(theEvent.controller().name().indexOf("TextArea")> -1){
       String value = theEvent.controller().getStringValue();
       String name = theEvent.controller().name();
       gui.get(Textfield.class, name).setValue(value);
       ((Textfield)theEvent.controller()).setText(value);
       print(name);
       println(value);

      }     
   }
}
