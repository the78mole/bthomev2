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

// Board-specific LED mapping – both boards use active-LOW LEDs (LOW = ON).
#if defined(BOARD_NRF52DK)
// nRF52840-DK (pca10056): PIN_LED1=P0.13, PIN_LED2=P0.14, PIN_LED3=P0.15,
// PIN_LED4=P0.16 LED_RED=PIN_LED1, LED_BLUE=PIN_LED2 (defined in variant.h),
// LED_STATE_ON=0
#define MY_LED_RED LED_RED     // LED1
#define MY_LED_GREEN PIN_LED3  // no LED_GREEN on DK → use LED3
#define MY_LED_BLUE LED_BLUE   // LED2
// J-Link VCOM (P0.06=TX / P0.08=RX) → Serial2 in Adafruit BSP (NRF_UARTE1)
// Cannot use -DSerial=Serial2 build flag (conflicts with USB CDC declaration).
#define DBG_SERIAL Serial2
#define MY_BOARD_NAME "nRF52840-DK (pca10056)"
#elif defined(BOARD_XIAO_NRF52840)
// Seeed XIAO nRF52840: RGB LED, active LOW
// LED_RED=P0.26, LED_GREEN=P0.30, LED_BLUE=P0.06
#define MY_LED_RED LED_RED
#define MY_LED_GREEN LED_GREEN
#define MY_LED_BLUE LED_BLUE
#define DBG_SERIAL Serial
#define MY_BOARD_NAME "Seeed XIAO nRF52840"
#else
#define MY_LED_RED LED_RED
#define MY_LED_GREEN LED_GREEN
#define MY_LED_BLUE LED_BLUE
#define DBG_SERIAL Serial
#define MY_BOARD_NAME "Unknown Board"
#endif
#define MY_LED_ON LOW
#define MY_LED_OFF HIGH

// Create BThome V2 device instance
BThomeV2Device bthome;

// Simulated sensor values
float temperature = 21.5;
float humidity = 65.0;
uint8_t battery = 100;

void setup() {
  // Initialize LEDs first
  pinMode(MY_LED_RED, OUTPUT);
  pinMode(MY_LED_GREEN, OUTPUT);
  pinMode(MY_LED_BLUE, OUTPUT);
  digitalWrite(MY_LED_RED, MY_LED_OFF);
  digitalWrite(MY_LED_GREEN, MY_LED_OFF);
  digitalWrite(MY_LED_BLUE, MY_LED_OFF);

// *** BOOT INDICATOR: rapid red blink before ANY init ***
// Uses direct GPIO + busy-wait to avoid any dependency on delay()/FreeRTOS.
#define GPIO0_OUTSET (*(volatile uint32_t*)0x50000508UL)
#define GPIO0_OUTCLR (*(volatile uint32_t*)0x5000050CUL)
#define GPIO0_DIRSET (*(volatile uint32_t*)0x50000518UL)
#define LED1_BIT (1u << 13)
  GPIO0_DIRSET = LED1_BIT;
  for (int i = 0; i < 20; i++) {
    GPIO0_OUTCLR = LED1_BIT;  // ON  (active-LOW)
    for (volatile uint32_t d = 0; d < 100000; d++) {
    }
    GPIO0_OUTSET = LED1_BIT;  // OFF
    for (volatile uint32_t d = 0; d < 100000; d++) {
    }
  }
  // LED_RED ON for the entire duration of setup()
  digitalWrite(MY_LED_RED, MY_LED_ON);

  // Initialize Serial
  DBG_SERIAL.begin(115200);

  // Wait up to 8s for USB CDC – blink blue LED so we know the board is alive.
  // Serial2 (UART/J-Link) is always ready; this loop only blocks on USB CDC.
  unsigned long startTime = millis();
  while (!DBG_SERIAL && (millis() - startTime < 8000)) {
    digitalWrite(MY_LED_BLUE, MY_LED_ON);
    delay(200);
    digitalWrite(MY_LED_BLUE, MY_LED_OFF);
    delay(200);
  }
  delay(100);

  // Checkpoint 1: Serial works BEFORE anything else
  DBG_SERIAL.println("\n\n[CP1] Serial OK – before BLE init");
  DBG_SERIAL.flush();

  DBG_SERIAL.println("========================================");
  DBG_SERIAL.println("  BThome V2 nRF52 Example");
  DBG_SERIAL.println("  Hardware: " MY_BOARD_NAME);
  DBG_SERIAL.println("========================================");
  DBG_SERIAL.println();

  // Initialize BThome V2

  if (!bthome.begin("MAKE-nRF52")) {
    while (1) {
      digitalWrite(MY_LED_GREEN, MY_LED_ON);
      delay(100);
      digitalWrite(MY_LED_GREEN, MY_LED_OFF);
      delay(100);
    }
  }

  // Add initial sensor readings
  DBG_SERIAL.println("\nAdding initial measurements:");
  DBG_SERIAL.printf("  • Temperature: %.1f °C\n", temperature);
  DBG_SERIAL.printf("  • Humidity: %.1f %%\n", humidity);
  DBG_SERIAL.printf("  • Battery: %d %%\n", battery);

  bthome.addTemperature(temperature);
  bthome.addHumidity(humidity);
  bthome.addBattery(battery);

  // Start advertising
  DBG_SERIAL.print("\nStarting BLE advertising... ");
  if (bthome.startAdvertising()) {
    DBG_SERIAL.println("OK");
    DBG_SERIAL.println("✓ BThome V2 advertising started successfully");

    // LED_BLUE: brief flash = first BThome packet queued
    digitalWrite(MY_LED_BLUE, MY_LED_ON);
    delay(50);
    digitalWrite(MY_LED_BLUE, MY_LED_OFF);
  } else {
    DBG_SERIAL.println("FAILED!");
  }

  DBG_SERIAL.println("\n----------------------------------------");
  DBG_SERIAL.println("Ready. Updating every 30 seconds...");
  DBG_SERIAL.println("----------------------------------------\n");

  // LED_RED OFF – setup complete
  digitalWrite(MY_LED_RED, MY_LED_OFF);
}

void loop() {
  // Wait 30 s – LED_GREEN heartbeat: 1 s period, 10 % duty cycle (100 ms ON /
  // 900 ms OFF)
  unsigned long loopStart = millis();
  while (millis() - loopStart < 30000UL) {
    unsigned long t = (millis() - loopStart) % 1000UL;
    digitalWrite(MY_LED_GREEN, t < 100 ? MY_LED_ON : MY_LED_OFF);
    delay(10);
  }
  digitalWrite(MY_LED_GREEN, MY_LED_OFF);

  // Simulate sensor value changes
  float tempChange = (random(-100, 100) / 100.0);
  float humChange = (random(-200, 200) / 100.0);

  temperature += tempChange;
  humidity += humChange;
  battery = max(0, battery - 1);

  // Keep values in reasonable ranges
  temperature = constrain(temperature, -20.0, 40.0);
  humidity = constrain(humidity, 0.0, 100.0);

  DBG_SERIAL.println();
  DBG_SERIAL.println("┌─────────────────────────────────────┐");
  DBG_SERIAL.println("│  Updating Sensor Data               │");
  DBG_SERIAL.println("└─────────────────────────────────────┘");
  DBG_SERIAL.printf("  Temperature: %.2f °C (Δ%+.2f)\n", temperature,
                    tempChange);
  DBG_SERIAL.printf("  Humidity:    %.1f %% (Δ%+.1f)\n", humidity, humChange);
  DBG_SERIAL.printf("  Battery:     %d %%\n", battery);

  // Clear old measurements
  DBG_SERIAL.print("\n  Clearing old measurements... ");
  bthome.clearMeasurements();
  DBG_SERIAL.println("done");

  // Add new measurements
  DBG_SERIAL.print("  Adding new measurements... ");
  bthome.addTemperature(temperature);
  bthome.addHumidity(humidity);
  bthome.addBattery(battery);
  DBG_SERIAL.println("done");

  // Update advertising with new data
  DBG_SERIAL.print("  Updating BLE advertisement... ");
  if (bthome.updateAdvertising()) {
    DBG_SERIAL.println("OK");

    // Blink blue LED to indicate packet sent
    digitalWrite(MY_LED_BLUE, MY_LED_ON);
    delay(100);
    digitalWrite(MY_LED_BLUE, MY_LED_OFF);

    DBG_SERIAL.println("  ✓ BThome packet sent successfully");
  } else {
    DBG_SERIAL.println("FAILED!");
  }

  DBG_SERIAL.println();
}
