/**
 * @file ESP32_Basic.ino
 * @brief Basic example of BThome V2 library for ESP32
 * 
 * This example demonstrates how to use the BThome V2 library on ESP32
 * to advertise sensor data (temperature, humidity, battery) using BLE.
 * 
 * Hardware: ESP32 (any variant)
 * 
 * The example simulates sensor readings and updates the BLE advertisement
 * every 30 seconds.
 */

#include <BThomeV2.h>

// Create BThome V2 device instance
BThomeV2Device bthome;

// Simulated sensor values
float temperature = 21.5;
float humidity = 65.0;
uint8_t battery = 100;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("BThome V2 ESP32 Example");
  Serial.println("========================");
  
  // Initialize BThome V2
  if (!bthome.begin("BThome-ESP32")) {
    Serial.println("Failed to initialize BThome!");
    while (1) delay(100);
  }
  
  Serial.println("BThome initialized successfully");
  
  // Add initial sensor readings
  bthome.addTemperature(temperature);
  bthome.addHumidity(humidity);
  bthome.addBattery(battery);
  
  // Start advertising
  if (bthome.startAdvertising()) {
    Serial.println("Started advertising BThome V2 data");
  } else {
    Serial.println("Failed to start advertising");
  }
  
  Serial.println("\nAdvertising sensor data:");
  Serial.printf("  Temperature: %.1f °C\n", temperature);
  Serial.printf("  Humidity: %.1f %%\n", humidity);
  Serial.printf("  Battery: %d %%\n", battery);
}

void loop() {
  // Wait 30 seconds
  delay(30000);
  
  // Simulate sensor value changes
  temperature += (random(-100, 100) / 100.0);
  humidity += (random(-200, 200) / 100.0);
  battery = max(0, battery - 1);
  
  // Keep values in reasonable ranges
  temperature = constrain(temperature, -20.0, 40.0);
  humidity = constrain(humidity, 0.0, 100.0);
  
  Serial.println("\nUpdating sensor data:");
  Serial.printf("  Temperature: %.1f °C\n", temperature);
  Serial.printf("  Humidity: %.1f %%\n", humidity);
  Serial.printf("  Battery: %d %%\n", battery);
  
  // Clear old measurements
  bthome.clearMeasurements();
  
  // Add new measurements
  bthome.addTemperature(temperature);
  bthome.addHumidity(humidity);
  bthome.addBattery(battery);
  
  // Update advertising with new data
  bthome.updateAdvertising();
  Serial.println("Advertising updated");
}
