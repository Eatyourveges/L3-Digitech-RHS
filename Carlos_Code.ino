
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT11.h>
LiquidCrystal_I2C lcd(0x27, 20, 4);
DHT11 dht11(5);

void setup() {
  lcd.init();                    
  lcd.backlight();
  lcd.setCursor(3, 0);
  lcd.print("Hello, world!");
  lcd.setCursor(2, 1);
  lcd.print("Ywrobot Arduino!");
  lcd.setCursor(0, 2);
  lcd.print("Arduino LCM IIC 2004");
  lcd.setCursor(2, 3);
  lcd.print("Power By Ec-yuan!");
  Serial.begin(9600);
}

void loop() {
  int temperature = 0;
  int humidity = 0;
  int result = dht11.readTemperatureHumidity(temperature, humidity);
 
  if (result == 0) {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C\tHumidity: ");
    Serial.print(humidity);
    Serial.println(" %");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(temperature);
    lcd.print(" C");
    lcd.setCursor(0, 1);
    lcd.print("Humidity: ");
    lcd.print(humidity);
    lcd.print(" %");
  } else {
    
    Serial.println(DHT11::getErrorString(result));
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Error reading");
    lcd.setCursor(0, 1);
    lcd.print("from sensor!");
  }
  delay(2000);
}
