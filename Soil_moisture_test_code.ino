// Library to Run I2C LCD
#include <LiquidCrystal_I2C.h>    
LiquidCrystal_I2C lcd(0x27, 16, 2);
const int soilMoisturePin = A0;
int sensorValue = 0;
int moisturePercent = 0;

void setup()
 {
 lcd.init();
 lcd.backlight();
 lcd.clear();
 lcd.setCursor(0, 0);
 lcd.print("Soil Moisture:");
}

void loop()
 {
 sensorValue = analogRead(soilMoisturePin);
 moisturePercent = map(sensorValue, 0, 1020, 100, 0);
 lcd.setCursor(0, 1);
 lcd.print(moisturePercent);
 lcd.print(" %  "); 
 delay(1000);
}
