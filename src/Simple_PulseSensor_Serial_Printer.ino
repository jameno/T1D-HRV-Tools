
/*  
 *   Simple Serial Printer (100 samples/sec)
 *   Modified from PulseSensor.com's Starter Project Code
*/


//  Variables
int PulseSensorPurplePin = 0;        // Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0
int Signal;                // holds the incoming raw data. Signal value can range from 0-1024

// The SetUp Function:
void setup() {
   Serial.begin(9600);         // Set's up Serial Communication at certain speed.
}

// The Main Loop Function
void loop() {

  Serial.println(Signal);                    // Send the Signal value to Serial Plotter.
  delay(10); //delay 10 ms (100 samples/sec)
}
