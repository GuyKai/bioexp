// This is only used for observe and confirm the data  

unsigned long begt, runt, Oldmicros;
int ch;

void setup(){
  Serial.begin(500000);
  Oldmicros = micros();
  ch = 6;   //0 for one channel, 1 for all channel 
}

void loop(){
  //runt = micros() - begt;
  //begt = micros();
  //Serial.print(runt);
  //Serial.println(1000000.0/runt);
  
  if ( ch != 6){
    //======for only one channel======//
  
    int value = analogRead(ch);
    Serial.print(value);
    Serial.print(" ");

  }
  else {
    //======for all channel======//
    for (int i = 0; i <= 5 ; i++){
      Serial.print(analogRead(i));
      Serial.print(" ");
    }
  }

  Serial.print(1024);
  Serial.print(" ");
  Serial.print(512);
  Serial.print(" ");
  Serial.println(0);

  

}
