/**
 * @file ESP32_MultipleSensors.ino
 * @brief Complete sensor station example with multiple sensor types
 * 
 * This example demonstrates how to use multiple sensor types together
 * including temperature, humidity, pressure, CO2, battery, and binary sensors.
 * 
 * Hardware: ESP32 with various sensors (or simulated values)
 */

#include <BThomeV2.h>

// Create BThome V2 device instance
BThomeV2Device bthome;

// Simulated sensor values
float temperature = 21.5;
float humidity = 65.0;
float pressure = 1013.25;
uint16_t co2 = 450;
uint8_t battery = 100;
bool motionDetected = false;
bool doorOpen = false;

// Update interval
const unsigned long UPDATE_INTERVAL = 60000;  // 60 seconds
unsigned long lastUpdate = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("BThome V2 Multiple Sensors Example");
  Serial.println("===================================");
  
  // Initialize BThome V2
  if (!bthome.begin("BThome-Station")) {
    Serial.println("Failed to initialize BThome!");
    while (1) delay(100);
  }
  
  Serial.println("BThome initialized successfully");
  
  // Send initial sensor readings
  updateSensors();
  
  // Start advertising
  if (bthome.startAdvertising()) {
    Serial.println("Started advertising BThome V2 data");
  } else {
    Serial.println("Failed to start advertising");
  }
}

void loop() {
  // Check if it's time to update
  if (millis() - lastUpdate >= UPDATE_INTERVAL) {
    updateSensors();
    lastUpdate = millis();
  }
  
  // Simulate motion detection (random event)
  if (random(0, 1000) > 995) {  // 0.5% chance per loop
    motionDetected = !motionDetected;
    Serial.printf("Motion %s\n", motionDetected ? "DETECTED" : "cleared");
    updateSensors();
  }
  
  // Simulate door state change (random event)
  if (random(0, 1000) > 998) {  // 0.2% chance per loop
    doorOpen = !doorOpen;
    Serial.printf("Door %s\n", doorOpen ? "OPENED" : "closed");
    updateSensors();
  }
  
  delay(100);
}

void updateSensors() {
  Serial.println("\n--- Updating Sensors ---");
  
  // Simulate sensor value changes
  temperature += (random(-50, 50) / 100.0);
  humidity += (random(-100, 100) / 100.0);
  pressure += (random(-50, 50) / 100.0);
  co2 += random(-10, 10);
  battery = max(0, battery - (random(0, 2)));  // Slow battery drain
  
  // Keep values in reasonable ranges
  temperature = constrain(temperature, -20.0, 40.0);
  humidity = constrain(humidity, 0.0, 100.0);
  pressure = constrain(pressure, 950.0, 1050.0);
  co2 = constrain(co2, 400, 2000);
  
  // Print all sensor values
  Serial.printf("Temperature:  %.2f °C\n", temperature);
  Serial.printf("Humidity:     %.1f %%\n", humidity);
  Serial.printf("Pressure:     %.2f hPa\n", pressure);
  Serial.printf("CO2:          %d ppm\n", co2);
  Serial.printf("Battery:      %d %%\n", battery);
  Serial.printf("Motion:       %s\n", motionDetected ? "YES" : "NO");
  Serial.printf("Door:         %s\n", doorOpen ? "OPEN" : "CLOSED");
  
  // Clear old measurements
  bthome.clearMeasurements();
  
  // Add all measurements
  bthome.addTemperature(temperature);
  bthome.addHumidity(humidity);
  bthome.addPressure(pressure);
  bthome.addCO2(co2);
  bthome.addBattery(battery);
  
  // Add binary sensors
  bthome.addBinarySensor(MOTION, motionDetected);
  bthome.addBinarySensor(DOOR, doorOpen);
  
  // Update advertising with new data
  if (bthome.updateAdvertising()) {
    Serial.println("✓ Advertising updated");
  } else {
    Serial.println("✗ Failed to update advertising");
  }
}
