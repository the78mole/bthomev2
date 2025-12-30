/**
 * @file main.cpp
 * @brief Button event example for ESP32 with BThome V2
 *
 * This example demonstrates how to send button events using BThome V2.
 * It uses a physical button connected to GPIO and advertises button
 * press events (single, double, triple, long press).
 *
 * Hardware:
 * - ESP32 (any variant)
 * - Button connected to GPIO 0 (BOOT button) or any GPIO pin
 * - Button pulls GPIO to GND when pressed (with internal pull-up)
 */

#include <Arduino.h>
#include <BThomeV2.h>

// Pin configuration
const int BUTTON_PIN = 0;  // GPIO0 (BOOT button on most ESP32 dev boards)

// Create BThome V2 device instance
BThomeV2Device bthome;

// Button state tracking
bool lastButtonState = HIGH;
unsigned long buttonPressTime = 0;
unsigned long lastReleaseTime = 0;
int pressCount = 0;
const unsigned long LONG_PRESS_TIME = 1000;  // 1 second for long press
const unsigned long MULTI_CLICK_TIME = 500;  // 500ms window for multi-click

void sendButtonEvent(uint8_t event);

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("BThome V2 Button Example");
  Serial.println("========================");

  // Configure button pin
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Initialize BThome V2
  if (!bthome.begin("BThome-Button")) {
    Serial.println("Failed to initialize BThome!");
    while (1) delay(100);
  }

  Serial.println("BThome initialized successfully");

  // Add initial state with motion sensor as false (no button press yet)
  bthome.addButtonEvent(0x00);  // No event

  // Start advertising
  if (bthome.startAdvertising()) {
    Serial.println("Started advertising");
    Serial.println("\nWaiting for button press...");
    Serial.println("  Single press = 0x01");
    Serial.println("  Double press = 0x02");
    Serial.println("  Triple press = 0x03");
    Serial.println("  Long press   = 0x04");
  } else {
    Serial.println("Failed to start advertising");
  }
}

void loop() {
  bool currentButtonState = digitalRead(BUTTON_PIN);

  // Button pressed (LOW because of pull-up)
  if (currentButtonState == LOW && lastButtonState == HIGH) {
    buttonPressTime = millis();

    // Check if this is part of a multi-click sequence
    if (millis() - lastReleaseTime < MULTI_CLICK_TIME) {
      pressCount++;
    } else {
      pressCount = 1;
    }

    Serial.println("Button pressed");
  }

  // Button released
  if (currentButtonState == HIGH && lastButtonState == LOW) {
    unsigned long pressDuration = millis() - buttonPressTime;
    lastReleaseTime = millis();

    // Determine if it was a long press
    if (pressDuration >= LONG_PRESS_TIME) {
      Serial.println("Long press detected!");
      sendButtonEvent(0x04);  // Long press
      pressCount = 0;         // Reset count after long press
    } else {
      Serial.printf("Short press #%d\n", pressCount);
    }
  }

  // Check for multi-click timeout
  if (pressCount > 0 && currentButtonState == HIGH &&
      millis() - lastReleaseTime > MULTI_CLICK_TIME) {
    // Send the appropriate event based on press count
    if (pressCount == 1) {
      Serial.println("Single press event");
      sendButtonEvent(0x01);
    } else if (pressCount == 2) {
      Serial.println("Double press event");
      sendButtonEvent(0x02);
    } else if (pressCount >= 3) {
      Serial.println("Triple press event");
      sendButtonEvent(0x03);
    }

    pressCount = 0;
  }

  lastButtonState = currentButtonState;
  delay(10);  // Small debounce delay
}

void sendButtonEvent(uint8_t event) {
  // Clear old measurements
  bthome.clearMeasurements();

  // Add button event
  bthome.addButtonEvent(event);

  // Update advertising
  bthome.updateAdvertising();

  Serial.println("Button event sent via BLE");
}
