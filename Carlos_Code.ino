
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
const int soilMoisturePin = A0;
const int buttonPin = 2; // Pin for the button
const int dhtPin = 5; // Pin for the DHT11 sensor

DHT dht(dhtPin, DHT11);

int sensorValue = 0;
int moisturePercent = 0;
bool showMoisture = true; // Start with soil moisture display

void setup() {
    lcd.init();
    lcd.backlight();
    pinMode(buttonPin, INPUT_PULLUP); // Use internal pull-up resistor
    dht.begin();
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Soil Moisture:");
}

void loop() {
    if (digitalRead(buttonPin) == LOW) {
        // Button pressed, switch display
        showMoisture = !showMoisture;
        delay(200); // Debounce delay
    }

    if (showMoisture) {
        // Display soil moisture
        sensorValue = analogRead(soilMoisturePin);
        moisturePercent = map(sensorValue, 0, 1020, 100, 0);
        
        lcd.setCursor(0, 1);
        lcd.print("Moisture: ");
        lcd.print(moisturePercent);
        lcd.print(" %  "); 
    } else {
        // Display DHT11 readings
        float humidity = dht.readHumidity();
        float temperature = dht.readTemperature();

        lcd.setCursor(0, 1);
        lcd.print("Temp: ");
        lcd.print(temperature);
        lcd.print("C ");
        lcd.setCursor(0, 0);
        lcd.print("Humidity: ");
        lcd.print(humidity);
        lcd.print("% ");
    }
    
    delay(1000); // Update every second
}
