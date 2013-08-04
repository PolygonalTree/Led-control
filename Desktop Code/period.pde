class Period{
  int time;
  int[] ledColour = new int[4];
  int[] switchOnTime = new int[2];
  int[] switchOffTime = new int[2];
  int repetitions;
  boolean isIntervalHours = true;
  boolean isAlwaysOn=false;
  boolean isAlwaysOff =false;  
  
  Period(int t,boolean h, int r, int[] colour, int[] on, int[] off, boolean aON, boolean aOff){
    time = t;
    isIntervalHours = h;
    repetitions = r;
    switchOnTime = on;
    switchOffTime = off;
    ledColour = colour;
    isAlwaysOn = aON;
    isAlwaysOff = aOff;
  }
}


