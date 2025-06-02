int PulseSensorPin = 0;        // Pulse Sensor wire connected to ANALOG PIN 0
int LED = LED_BUILTIN;   // The on-board Arduion LED
int Signal;                // Signal value can range from 0-1024
int Threshold = 580;       // Signal amplitude threshold to "count as a beat"

void setup() {
  pinMode(LED,OUTPUT);
   Serial.begin(115200); 
}

void loop() {
  Signal = analogRead(PulseSensorPin); 
  Serial.println(Signal);

  if(Signal > Threshold){                          
    digitalWrite(LED,HIGH);
  } else {
    digitalWrite(LED,LOW);
  }

  delay(20);
}