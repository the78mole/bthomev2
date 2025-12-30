/**
 * @file main.cpp
 * @brief Basic example of BThome V2 library for nRF52
 *
 * This example demonstrates how to use the BThome V2 library on nRF52
 * to advertise sensor data (temperature, humidity, battery) using BLE.
 *
 * Hardware: nRF52 boards (Adafruit Feather nRF52840, XIAO nRF52840)
 *
 * The example simulates sensor readings and updates the BLE advertisement
 * every 30 seconds.
 *
 * LEDs (XIAO nRF52840):
 * - LED_GREEN (Pin 30): Lights up after successful boot
 * - LED_BLUE (Pin 6): Blinks briefly when sending BThome packet
 */

#include <Arduino.h>
#include <BThomeV2.h>

// LEDs are already defined in variant.h:
// LED_RED = 26, LED_GREEN = 30, LED_BLUE = 6

// Create BThome V2 device instance
BThomeV2Device bthome;

// Simulated sensor values
float temperature = 21.5;
float humidity = 65.0;
uint8_t battery = 100;

void setup() {
  // Initialize LEDs first
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  digitalWrite(LED_GREEN, HIGH);  // OFF (active LOW)
  digitalWrite(LED_BLUE, HIGH);   // OFF

  // Initialize Serial
  Serial.begin(115200);

  // Wait for USB CDC connection (with timeout)
  unsigned long startTime = millis();
  while (!Serial && (millis() - startTime < 2000)) {
    delay(10);
  }
  delay(100);

  Serial.println("\n\n");
  Serial.println("========================================");
  Serial.println("  BThome V2 nRF52 Example");
  Serial.println("  Hardware: XIAO nRF52840");
  Serial.println("========================================");
  Serial.println();

  // Initialize BThome V2
  Serial.print("Initializing BThome V2... ");
  Serial.flush();

  if (!bthome.begin("BThome-nRF52")) {
    Serial.println("FAILED!");
    while (1) {
      digitalWrite(LED_GREEN, LOW);
      delay(100);
      digitalWrite(LED_GREEN, HIGH);
      delay(100);
    }
  }
  Serial.println("OK");

  // Add initial sensor readings
  Serial.println("\nAdding initial measurements:");
  Serial.printf("  • Temperature: %.1f °C\n", temperature);
  Serial.printf("  • Humidity: %.1f %%\n", humidity);
  Serial.printf("  • Battery: %d %%\n", battery);

  bthome.addTemperature(temperature);
  bthome.addHumidity(humidity);
  bthome.addBattery(battery);

  // Start advertising
  Serial.print("\nStarting BLE advertising... ");
  if (bthome.startAdvertising()) {
    Serial.println("OK");
    Serial.println("✓ BThome V2 advertising started successfully");

    // Turn on green LED to indicate successful boot
    digitalWrite(LED_GREEN, LOW);  // Active LOW = ON

    // Brief blue LED blink to confirm packet sent
    digitalWrite(LED_BLUE, LOW);
    delay(50);
    digitalWrite(LED_BLUE, HIGH);
  } else {
    Serial.println("FAILED!");
  }

  Serial.println("\n----------------------------------------");
  Serial.println("Ready. Updating every 30 seconds...");
  Serial.println("----------------------------------------\n");
}

void loop() {
  // Wait 30 seconds
  delay(30000);

  // Simulate sensor value changes
  float tempChange = (random(-100, 100) / 100.0);
  float humChange = (random(-200, 200) / 100.0);

  temperature += tempChange;
  humidity += humChange;
  battery = max(0, battery - 1);

  // Keep values in reasonable ranges
  temperature = constrain(temperature, -20.0, 40.0);
  humidity = constrain(humidity, 0.0, 100.0);

  Serial.println();
  Serial.println("┌─────────────────────────────────────┐");
  Serial.println("│  Updating Sensor Data               │");
  Serial.println("└─────────────────────────────────────┘");
  Serial.printf("  Temperature: %.2f °C (Δ%+.2f)\n", temperature, tempChange);
  Serial.printf("  Humidity:    %.1f %% (Δ%+.1f)\n", humidity, humChange);
  Serial.printf("  Battery:     %d %%\n", battery);

  // Clear old measurements
  Serial.print("\n  Clearing old measurements... ");
  bthome.clearMeasurements();
  Serial.println("done");

  // Add new measurements
  Serial.print("  Adding new measurements... ");
  bthome.addTemperature(temperature);
  bthome.addHumidity(humidity);
  bthome.addBattery(battery);
  Serial.println("done");

  // Update advertising with new data
  Serial.print("  Updating BLE advertisement... ");
  if (bthome.updateAdvertising()) {
    Serial.println("OK");

    // Blink blue LED to indicate packet sent
    digitalWrite(LED_BLUE, LOW);  // ON
    delay(100);
    digitalWrite(LED_BLUE, HIGH);  // OFF

    Serial.println("  ✓ BThome packet sent successfully");
  } else {
    Serial.println("FAILED!");
  }

  Serial.println();
}
