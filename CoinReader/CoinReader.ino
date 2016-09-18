const int startButton = A0;
const int rightBumper = A1;  // Analog input pin that the potentiometer is attached to
const int leftBumper = A2;
const int maxValue = 900;
const int minValue = 100;

int rightBumperValue = 1023;        // value read from the pot
int leftBumperValue = 1023;
int startSig = 0;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  delay(100);
  
  rightBumperValue = analogRead(rightBumper);
  leftBumperValue = analogRead(leftBumper);
  startSig = analogRead(startButton);
  
  if(rightBumperValue < maxValue || leftBumperValue < maxValue){
    Serial.print("bumper \n");
  }
  
  if(startSig == 0){
    Serial.print("1 \n");
  }
}
