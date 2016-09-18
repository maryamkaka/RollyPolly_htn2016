const int rightBumper = A0;  // Analog input pin that the potentiometer is attached to

int rightBumperValue = 1023;        // value read from the pot

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  delay(100);
  
  rightBumperValue = analogRead(rightBumper);
  
  if(rightBumperValue < 950){
    Serial.print("rightBumper \n");
  }
}
