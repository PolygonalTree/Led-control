 
String detectArduino(){
   String [] port_list;
   Serial arduinoPort;
   String data;
   String port="";
   port_list = Serial.list();
   println( port_list);
   for (int i = 0; i<Serial.list().length; i++) {
     if (port_list[i].indexOf("usbserial")> -1 
     || port_list[i].indexOf("USB")> -1
     || port_list[i].indexOf("COM")> -1){
       println("buscando Arduino");
       messages="Searching Controller";
       data ="";
       arduinoPort = new Serial(this, port_list[i],9600);
       delay(50);
       arduinoPort.write("C");
       println("enviando datos");
       delay(3000);
       println(arduinoPort.available());
     if (arduinoPort.available() > 0){
       data = arduinoPort.readString();
       println(data);
       }
      if (data.indexOf("Led controller") > -1 || data.indexOf("Arduino")>-1){
        println("Arduino encontrado");
        messages="Controller found.";
        port = port_list[i];
        arduinoPort.stop();
        break;
      }else{
      arduinoPort.stop();
      println("stop");
      messages="Controller not detected";
      }
     }
    }
    return port;

 }
 
// String readData(){
//   String data="";
//   delay(1000);
//   if (arduino.available() > 0){
//      data = arduino.readString();
//     }
//       return data;
// }
// 
 
void sendDataToArduino(int[] colour){
       String data = "R"+colour[0]+"G"+colour[1]+"B"+colour[2]+"W"+colour[3];
       //arduino.write(data);
       println(data);
       //String response = readData();
       println("readData");
     }



// Create a second thread by extending Thread
class NewThread extends Thread {
   NewThread() {
      // Create a new, second thread
      super("Arduino Control");
      System.out.println("Child thread: " + this);
      start(); // Start the thread
   }

  
public void run(){
  
    int[] startTime = {year(), month(), day(),hour(), minute()}; //experiment starts time.
    float expHours = 0; //days of experimentation for a period
    int expMinutes= 0; //minutes of a period.
    int numberPeriod = 0; //Period position in array, 0 when the experiment starts
    float startHour;
    float endHour;
    float zt0;
    int[] off={0,0,0,0};
    
     //Avoid start experiment without periods.  
    if (exp.size() <= 1){
      println("Experiment not set");
      messages = "Experiment not Set properly, maybe it miss a period";
      delay(2000);
      alreadyRunning = false;
      threadArduino.interrupt();
      gui.get(Toggle.class, "Run").setValue(false);
      return;
    }
    
    //Text to show that the experiment is running.
    time = "The experiment started at: "+ nf(day(),2)+"/"+nf(month(),2)+"/"+year()+
                    " at "+nf(hour(),2)+":"+nf(minute(),2)+":"+nf(second(),2);
      
    
//prepare fir period and set ZT0.
     Period PeriodZt0 = (Period) exp.get(1);
       zt0 = PeriodZt0.switchOnTime[0]+(PeriodZt0.switchOnTime[1]/60.); //zt0 in hours.
    
    //number of repetitions for period 0.
    Period Period0 = (Period) exp.get(0);
    int repetitions = Period0.repetitions;
    
    //first Period. ajustment to zt0
    while (alreadyRunning == true){
      Period firstPeriod = (Period) exp.get(0);
      startHour = firstPeriod.switchOnTime[0]+(firstPeriod.switchOnTime[1]/60.);
      endHour = firstPeriod.switchOffTime[0]+(firstPeriod.switchOffTime[1]/60.);
      //Duration of the period greater than a day?
      int firstPeriodDuration = firstPeriod.time * firstPeriod.repetitions;
      
      if(endHour == 0){
         endHour = 23.999;
      }
      if (firstPeriod.isIntervalHours ==false){
        messages = "No Adjustement";
        sendDataToArduino(off);
      }else{
        if (firstPeriod.isAlwaysOn == true){
          println("encendido");
          messages = "Switch ON in period 0, mode LL";
          sendDataToArduino(firstPeriod.ledColour);
        }else if (firstPeriod.isAlwaysOff == true){
          println("apagado");
          messages = "Switch OFF in period 0, mode DD";
          sendDataToArduino(off);
        }else if(firstPeriod.isAlwaysOn != true
                 && firstPeriod.isAlwaysOff != true
                 && startHour <= hour()+minute()/60. && endHour >= hour()+minute()/60.){
          println("encendido0");
          messages = "Switch ON in period 0";
          sendDataToArduino(firstPeriod.ledColour);
        }else if( startHour > endHour 
                && endHour <= hour()+minute()/60. 
                && startHour >= hour()+minute()/60.){
         println("apagado");
         messages = "Switch OFF in period "+numberPeriod+" mode LD";
         sendDataToArduino(off);
       }else if( startHour > endHour
                && firstPeriod.isAlwaysOn != true
                && firstPeriod.isAlwaysOff != true){
                if(endHour <= hour()+minute()/60. 
                   && startHour >= hour()+minute()/60.){
                    println("apagado");
                    messages = "Switch OFF in period "+numberPeriod+" mode LD";
                    sendDataToArduino(off);
                }else{
                    println("encendido");
                    messages = "Switch ON in period "+numberPeriod+" mode LD";
                    sendDataToArduino(firstPeriod.ledColour);
                }
                
        }else{
          println("apagado0");
          messages = "Switch OFF in period 0";
          sendDataToArduino(off);
        }
      }
       
       if (firstPeriod.isIntervalHours == true){
         if (firstPeriodDuration < 24 && hour()+minute()/60. >= zt0){
           numberPeriod +=1;
           break;
         }
         if (day()!= startTime[2] && hour()+minute()/60. >= zt0){
           repetitions = repetitions-1;
          // numberPeriod += 1;
           startTime[2] = day();
           if (numberPeriod > exp.size()-1){
             println("Experiment ended");
             messages = "Experiment Ended";
             sendDataToArduino(off);
             alreadyRunning = false;
             threadArduino.interrupt();
           }
           if(repetitions < 1){
             numberPeriod +=1;
             break;
           }  
         }
         
       }else if(firstPeriod.isIntervalHours == false){
         println("NO Adjustement");
         numberPeriod +=1;
          break;

       }
    delay(60000);  
    }
    
    //Experiment. While Periods available this while loop is running.
    boolean periodChanged = true;
    
    while (alreadyRunning == true){
       Period period = (Period) exp.get(numberPeriod); //object period from array periods.
       if (periodChanged == true){
         if (period.isIntervalHours==true){
           expHours = period.time * period.repetitions; //duration in days of the period.
           periodChanged = false;
         }else{
           expMinutes = period.time * period.repetitions; //duration in minutes.
           periodChanged = false;
         }
       }
       //Light control, switch on/off and colour parameters
      startHour = period.switchOnTime[0]+(period.switchOnTime[1]/60.);
      endHour = period.switchOffTime[0]+(period.switchOffTime[1]/60.);
      if(endHour == 0){
         endHour = 23.99999;
       }

      if(period.isAlwaysOn != true
         && period.isAlwaysOff != true
         && startHour <= hour()+minute()/60. && endHour >= hour()+minute()/60.){
         println("encendido");
         messages = "Switch ON in period "+numberPeriod+"mode LD";
         sendDataToArduino(period.ledColour);
       }else if(period.isAlwaysOn != true
                && period.isAlwaysOff != true
                && startHour < endHour
                && endHour <= hour()+minute()/60.){
         println("apagado");
          messages = "Switch OFF in period "+numberPeriod+" mode LD";
         sendDataToArduino(off);
       }else if(period.isAlwaysOn == true){
         println("encendido");
         messages = "Switch ON in period "+numberPeriod+" mode LL";
         sendDataToArduino(period.ledColour);
       }else if(period.isAlwaysOff == true){
         println("apagado");
         messages = "Switch OFF in period "+numberPeriod+" mode DD";
         sendDataToArduino(off);
       }else if( startHour > endHour 
                && endHour <= hour()+minute()/60. 
                && startHour >= hour()+minute()/60.){
         println("apagado");
         messages = "Switch OFF in period "+numberPeriod+" mode LD";
         sendDataToArduino(off);
       }else if( startHour > endHour
                && period.isAlwaysOn != true
                && period.isAlwaysOff != true){
                if(endHour <= hour()+minute()/60. 
                   && startHour >= hour()+minute()/60.){
                    println("apagado");
                    messages = "Switch OFF in period "+numberPeriod+" mode LD";
                    sendDataToArduino(off);
                }else{
                    println("encendido");
                    messages = "Switch ON in period "+numberPeriod+" mode LD";
                    sendDataToArduino(period.ledColour);
                }
                
        }       
                
       
       if (period.isIntervalHours == true){
       //Change period. It changes if the hours passed from zt0 are equal to duration of period.
       if (expHours >= 0){

           expHours = expHours - 1/60.; //rest one minute from expHours.
            println("Hours change");
            print(expHours);
           if (expHours < 0 ){
             numberPeriod += 1;
             //startTime[2] = day();
             //zt0 += period.time;
             periodChanged = true;
           }
           if (numberPeriod > exp.size()-1){
             println("Experiment ended");
             messages = "Experiment Ended";
             sendDataToArduino(off);
             alreadyRunning = false;
             threadArduino.interrupt();
           }
         }
       }else{
         if (expMinutes >= 0){
           expMinutes = expMinutes -1;
           println("Minutes change");
           println(expMinutes);
           if(expMinutes < 0){
             numberPeriod += 1;
             //startTime[2] = day();
             //zt0 +=period.time/60.;
             periodChanged = true;
           }
           if (numberPeriod > exp.size()-1){
             println("Experiment ended");
             messages = "Experiment Ended";
             sendDataToArduino(off);
             alreadyRunning = false;
             threadArduino.interrupt();
         }
       }  

     }
       //wait one minute to save resources.
        delay(60000);
    }
  }
}
