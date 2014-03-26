
Textlabel[] guiLabels = new Textlabel[9];
RadioButton HourMinButton;
RadioButton HourAdjustButton;
PImage radioButtonActive;
PImage radioButtonOver;
PImage radioButtonDefault;

    
ControlP5 gui;
ColorPicker cp;
    
void loadGui(){
  
  gui = new ControlP5(this);
  
  
  
  // Labels
      guiLabels[0] = gui.addTextlabel("title")
                        .setText("Add New Period")
                        .setPosition(25,25)
                        .setColorValue(0)
                        .setFont(createFont("Arial",18))
                        ;
      guiLabels[1] = gui.addTextlabel("durationLabel")
                        .setText("Duration of Period")
                        .setPosition(35,55)
                        .setColorValue(0)
                        .setFont(createFont("Arial",12))
                        ;
      guiLabels[2] = gui.addTextlabel("repetitionsLabel")
                        .setText("Repetitions")
                        .setPosition(35,75)
                        .setColorValue(0)
                        .setFont(createFont("Arial",12))
                        ;
      guiLabels[3] = gui.addTextlabel("LightLabel")
                        .setText("Light Tipe")
                        .setPosition(35,95)
                        .setColorValue(0)
                        .setFont(createFont("Arial",12))
                        ; 
      guiLabels[4] = gui.addTextlabel("colorLabel")
                        .setText("-RGBW Color")
                        .setPosition(45,115)
                        .setColorValue(0)
                        .setFont(createFont("Arial",12))
                        ;                           
      guiLabels[5] = gui.addTextlabel("SwitchOnLabel")
                        .setText("-Hour of Switch On")
                        .setPosition(45,165)
                        .setColorValue(0)
                        .setFont(createFont("Arial",12))
                        ;  
      guiLabels[6] = gui.addTextlabel("switchOffLabel")
                        .setText("-Hour of Switch Off")
                        .setPosition(45,185)
                        .setColorValue(0)
                        .setFont(createFont("Arial",12))
                        ;
  
                        
///Help for textAreas     
      gui.addTextlabel("helpDuration")
         .setText("i.e 24 in hours or minutes")
         .setPosition(250,58)
         .setColorValue(0)
         ;
     guiLabels[7]=gui.addTextlabel("helpHour")
         .setText("Hours")
         .setPosition(210,52)
         .setColorValue(0)
         ;
      guiLabels[8]=gui.addTextlabel("helpMn")
         .setText("Minutes")
         .setPosition(210,69)
         .setColorValue(0)
         ;
      gui.addTextlabel("helpOn")
         .setText("LL")
         .setPosition(210,169)
         .setColorValue(0)
         ;
      gui.addTextlabel("helpOff")
         .setText("DD")
         .setPosition(210,192)
         .setColorValue(0)
         ;
      gui.addTextlabel("helpRepetitions")
         .setText("Times the cycle repeats, i.e 2")
         .setPosition(200,80)
         .setColorValue(0)
         ;
      gui.addTextlabel("helpSwithOn")
         .setText("i.e 09:23")
         .setPosition(300,168)
         .setColorValue(0)
         ;
      gui.addTextlabel("helpSwithOff")
         .setText("i.e 23:45")
         .setPosition(300,188)
         .setColorValue(0)
         ;
               
            gui.addSlider("ColourRed")
               .setPosition(190,120)
               .setRange(0,255)
               .setColorCaptionLabel(color(0))
               .setColorBackground(color(255,0,0))
               ;  
            gui.addSlider("ColourGreen")
               .setPosition(190,130)
               .setRange(0,255)
               .setColorValueLabel(color(0))
               .setColorCaptionLabel(color(0))
               .setColorBackground(color(0,255,0))
               ;
            gui.addSlider("ColourBlue")
               .setPosition(190,140)
               .setRange(0,255)
               .setColorCaptionLabel(color(0))
               
               .setColorBackground(color(0,0,255))
               ;
            gui.addSlider("ColourWhite")
               .setPosition(190,150)
               .setRange(0,255)
               .setColorValueLabel(color(0))
               .setColorCaptionLabel(color(0))
               .setColorBackground(color(200))
               ;
  
  // TextAreas                       
        gui.addTextfield("durationTextArea")
           .setPosition(160,55)
           .setSize(20,16)
           .setFont(createFont("Arial",12))
           .setCaptionLabel("")
           .setColor(color(0))
           .setColorCursor(color(0))
           .setColorBackground(color(255))
           .setAutoClear(false)
           .setValue("24")
           ;
         
        gui.addTextfield("repetitionsTextArea")
           .setPosition(160,75)
           .setCaptionLabel("")
           .setSize(20,16)
           .setFont(createFont("Arial",12))
           .setColor(color(0))
           .setColorCursor(color(0))
           .setColorBackground(color(255))
           .setAutoClear(false)
           .setValue("1")
           ;
        gui.addTextfield("colorRedTextArea")
           .setPosition(160,120)
           .setLabelVisible(false)
           .setSize(20,10)
           .setFont(createFont("Arial",9))
           .setColor(color(0))
           .setColorCursor(color(0))
           .setCaptionLabel("")
           .setColorBackground(color(255))
           .setAutoClear(false)
           .setValue("000")
           ;
        gui.addTextfield("colorGreenTextArea")
           .setPosition(160,130)
           .setLabelVisible(false)
           .setSize(20,10)
           .setFont(createFont("Arial",9))
           .setColor(color(0))
           .setAutoClear(false)
           .setCaptionLabel("")
           .setColorBackground(color(255))
           .setColorCursor(color(0))
           .setValue("000")
           ;
        gui.addTextfield("colorBlueTextArea")
           .setPosition(160,140)
           .setLabelVisible(false)
           .setSize(20,10)
           .setFont(createFont("Arial",9))
           .setColor(color(0))
           .setColorCursor(color(0))
           .setCaptionLabel("")
           .setColorBackground(color(255))
           .setAutoClear(false)
           .setValue("000")
           ;
        gui.addTextfield("colorWhiteTextArea")
           .setPosition(160,150)
           .setLabelVisible(false)
           .setSize(20,10)
           .setFont(createFont("Arial",9))
           .setColor(color(0))
           .setColorCursor(color(0))
           .setCaptionLabel("")
           .setColorBackground(color(255))
           .setAutoClear(false)
           .setValue("000")
           ;
        gui.addTextfield("switchOnTextArea")
           .setPosition(160,165)
           .setLabelVisible(false)
           .setSize(36,16)
           .setFont(createFont("Arial",12))
           .setColor(color(0))
           .setColorCursor(color(0))
           .setCaptionLabel("")
           .setColorBackground(color(255))
           .setAutoClear(false)
           .setValue("09:00")
           ;
        gui.addTextfield("switchOffTextArea")
           .setPosition(160,185)
           .setLabelVisible(false)
           .setSize(36,16)
           .setFont(createFont("Arial",12))
           .setColor(color(0))
           .setColorCursor(color(0))
           .setCaptionLabel("")
           .setColorBackground(color(255))
           .setAutoClear(false)
           .setValue("00:00")
           ;
           
    //RadioButton//
      radioButtonActive = loadImage("checked.png");
      radioButtonOver = loadImage("partial.png");
      radioButtonDefault = loadImage("unchecked.png");
      
      HourMinButton=gui.addRadioButton("durationRadioButton")
                .setPosition(200, 52)
                .setColorForeground(color(200))
                .setColorActive(color(200))
                .setColorLabel(color(0))
                .setSize(10, 10)
                .setItemsPerRow(1)
                .setSpacingColumn(10)
                .setSpacingRow(5)
                .addItem("Hours", 1)
                .addItem("Minutes", 0)
                .activate("Hours")
                .hideLabels()
                .setImages(radioButtonDefault,radioButtonOver,radioButtonActive)
                ;
      
             gui.addRadioButton("switchOnRadioButton")
                .setPosition(200, 168)
                .setImages(radioButtonDefault,radioButtonOver,radioButtonActive)
                .setColorForeground(color(120))
                .setColorActive(color(200))
                .setColorLabel(color(0))
                .setSize(10, 10)
                .setItemsPerRow(1)
                .setSpacingColumn(10)
                .setSpacingRow(10)
                .addItem("LL", 1)
                .addItem("DD", 0)                
                ;
                
   //buttons
     controlP5.Button addButton = gui.addButton("AddPeriod")
                                     .setPosition(100,220)
                                     .setSize(200,19)
                                     .setCaptionLabel("Add Period")
                                     ;
     
  controlP5.Button saveButton = gui.addButton("Save")
                                   .setPosition(500,220)
                                   .setSize(200,19)
                                   .setCaptionLabel("Save Experiment")
                                   ;

  controlP5.Button loadButton = gui.addButton("Load")
                                   .setPosition(100,460)
                                   .setSize(200,19)
                                   .setCaptionLabel("Load Experiment")
                                   ;
  controlP5.Toggle runToggle = gui.addToggle("Run")
                                   .setPosition(500,460)
                                   .setSize(200,19)
                                   .setValue(false)
                                   .setCaptionLabel("Run Experiment")
                                   .setColorCaptionLabel(color(255))
                                   ;  
          runToggle.captionLabel().style().marginTop =-17;
          runToggle.captionLabel().style().marginLeft = 5 ;
          
}

void addDeleteButton(int i){
  gui.addButton("deletePeriod"+nf(i,3))
     .setPosition(810,22+i*12)
     .setSize(10,10)
     .setCaptionLabel("X")
     ;
}
void removeDeleteButton(int i){
    gui.remove("deletePeriod"+nf(i,3));
    loop();
}
void isRunning(){
    if (gui.get(Toggle.class,"Run").getValue() == 1.0 && alreadyRunning == false){
      fill(0);
      String time ="The experiment started at"+day()+"/"+month()+"/"+year()+
                    "at"+hour()+":"+minute()+":"+second();
      text(time,410,310);
      noFill();
      alreadyRunning = true;
      loop();
    }else if(gui.get(Toggle.class,"Run").getValue() == 0.0){
      alreadyRunning = false;   
    }
}


void printGui(){
  background(200);
  stroke(0);
  fill(255);
  rect(10,10,380,230) ; 
  rect(400,10,450,230);
  rect(10,250,380,230);
  rect(400,250,450,230);
  guiLabels[0].setText("Add new Period");
  guiLabels[2].setText("Repetitions");
  guiLabels[8].setText("Minutes");
  exp.update();
  if(alreadyRunning ==false){
    gui.get(Toggle.class,"Run").setValue(false);
  }
}

void printGui0(){
  background(200);
  stroke(0);
  fill(255);
  rect(10,10,380,230) ; 
  rect(400,10,450,230);
  rect(10,250,380,230);
  rect(400,250,450,230);
  guiLabels[0].setText("Add Adjustement Period");
  guiLabels[2].setText("Days of adjustement");
  guiLabels[8].setText("No adjustement");
  if(alreadyRunning ==false){
    gui.get(Toggle.class,"Run").setValue(false);
  }
}
