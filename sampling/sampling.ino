// This is used for getting data to pc/python 

unsigned long Oldmicros;
int ptime, mode;


void setup() {
  Serial.begin(500000); 
  Oldmicros = micros();
  mode = 1 ; // 0 for emg only , 1 for all
}

void loop() {

  ptime = micros() - Oldmicros ;
   
  if (ptime > 996) { // around 1000Hz
    //Serial.println(1000000.0/ptime); 
    Oldmicros = micros();     
        
    Serial.println();

    if ( mode == 1) { //all 
      for (int i = 0; i <= 5 ; i++) {
        int value = map(analogRead(i),0,1024.0,0,255);
        Serial.write(value);
      
      } 
    
    }
    
    else { //emg only  
      for (int i = 2; i <= 5 ; i++) {
        int value = map(analogRead(i),0,1024.0,0,255);
        Serial.write(value);
    
      }
    
    }
      
  }
  
}