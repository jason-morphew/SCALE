// test for seeed match UP project
// JY.W @ 2016-01-04

#include <Wire.h>
#include "Seeed_QTouchSensor.h"
QTouch qTouch;
void setup()
{
	Serial.begin(115200);
	Serial.println("Test for Seeed match UP project");
	Serial.println("Q Touch Sensor");
	qTouch.Init();  
}

void loop()
{
    int key = qTouch.QTouchRead();
    if(key >= 0)
    {
        Serial.print("KEY");
        Serial.print(key);
        Serial.println(" touched");
    }
    delay(10);
}
