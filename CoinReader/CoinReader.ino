const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to

int sensorValue = 1023;        // value read from the pot

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  delay(100);
  
  sensorValue = analogRead(analogInPin);

  if(sensorValue < 950){
    Serial.print("1 \n");
  }
}
