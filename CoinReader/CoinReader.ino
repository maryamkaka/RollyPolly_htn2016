const int rightBumper = A0;  // Analog input pin that the potentiometer is attached to
const int leftBumper = A1;
const int maxValue = 900;

int rightBumperValue = 1023;        // value read from the pot
int leftBumperValue = 1023;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  delay(100);
  
  rightBumperValue = analogRead(rightBumper);
  if(rightBumperValue < maxValue){
    Serial.print("rightBumper \n");
  }
  
  leftBumperValue = analogRead(leftBumper);
  if(leftBumperValue < maxValue){
    Serial.print("leftBumper \n");
  }
}
