
#define sensorPin A2

void setup() {
   // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  //analogReference(INTERNAL);
 
}

void loop() {
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  // get the temperature and convert it to celsius


float reading = analogRead(sensorPin);  
float voltage = reading * 5.0 / 1024.0;
float temp = voltage * 100 ;
  
 // print out the value you read:
 Serial.print(temp); 
 
 Serial.print(" \xC2\xB0");
 // print out the value you read, and skip next line
 Serial.println("C");
 delay(1000); 
}
