#include <LiquidCrystal_I2C.h>
#include <DHT.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
const int soilMoisturePin = A0;
const int buttonPin = 2; // Pin for the button to toggle the display
const int lcdControlButtonPin = 3; // Pin for the button to turn the LCD off/on
const int dhtPin = 5; // Pin for the DHT11 sensor
const int relayPin = 8; // Pin for the relay

DHT dht(dhtPin, DHT11);

int sensorValue = 0;
int moisturePercent = 0;
bool showMoisture = true; // Start with soil moisture display
bool lcdOn = true; // Flag to track LCD on/off state

// Thresholds
const int moistureThreshold = 40; // Soil moisture threshold (%)
const float tempThreshold = 25.0; // Temperature threshold (°C)
const float humidityThreshold = 70.0; // Humidity threshold (%)

// Flag to control the interrupt state
volatile bool toggleLCD = false;

void setup() {
    lcd.init();
    lcd.backlight();
    pinMode(buttonPin, INPUT_PULLUP); // Use internal pull-up resistor for button
    pinMode(relayPin, OUTPUT); // Set relay pin as output
    pinMode(lcdControlButtonPin, INPUT_PULLUP); // Button to control LCD power
    
    dht.begin();

    // Start serial communication
    Serial.begin(9600);  // Initialize the serial monitor at 9600 baud rate

    // Attach interrupt to the button that controls LCD on/off (now on falling edge)
    attachInterrupt(digitalPinToInterrupt(lcdControlButtonPin), toggleLCDState, FALLING);
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Soil Moisture:");
}

void loop() {
    if (toggleLCD) {
        // Toggle LCD on/off
        lcdOn = !lcdOn;
        if (lcdOn) {
            lcd.backlight();
        } else {
            lcd.noBacklight();
        }
        toggleLCD = false; // Reset the flag
        delay(200); // Debounce delay
    }

    if (lcdOn) {
        if (digitalRead(buttonPin) == LOW) {
            // Button pressed, switch display
            showMoisture = !showMoisture;
            delay(200); // Debounce delay
        }

        // Read soil moisture and print to Serial Monitor
        sensorValue = analogRead(soilMoisturePin);
        moisturePercent = map(sensorValue, 0, 1020, 100, 0);

        // Read temperature and humidity from DHT11
        float humidity = dht.readHumidity();
        float temperature = dht.readTemperature();

        // Show soil moisture or DHT11 readings on LCD
        if (showMoisture) {
            lcd.setCursor(0, 1);
            lcd.print("Moisture: ");
            lcd.print(moisturePercent);
            lcd.print(" %  "); 
        } else {
            lcd.setCursor(0, 1);
            lcd.print("Temp: ");
            lcd.print(temperature);
            lcd.print("C ");
            lcd.setCursor(0, 0);
            lcd.print("Humidity: ");
            lcd.print(humidity);
            lcd.print("% ");
        }

        // Print both sets of readings to Serial Monitor
        Serial.print("Soil Moisture: ");
        Serial.print(moisturePercent);
        Serial.println(" %");

        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.println(" C");
        
        Serial.print("Humidity: ");
        Serial.print(humidity);
        Serial.println(" %");

        // Relay control logic based on thresholds
        if (moisturePercent < moistureThreshold || temperature > tempThreshold || humidity < humidityThreshold) {
            digitalWrite(relayPin, HIGH); // Activate relay
        } else {
            digitalWrite(relayPin, LOW); // Deactivate relay
        }
    }

    delay(1000); // Update every second
}

// Interrupt service routine to toggle LCD state
void toggleLCDState() {
    toggleLCD = true; // Set the flag to toggle LCD on/off
}
