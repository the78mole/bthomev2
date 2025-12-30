# BThome V2 Library

A PlatformIO/Arduino library for implementing the BThome V2 protocol on ESP32
and nRF52 platforms.

## Overview

This library provides a unified interface for BLE advertising using the
[BThome V2 format](https://bthome.io/), which is designed for efficient
transmission of sensor data over Bluetooth Low Energy. The library abstracts
platform-specific BLE implementations, making it easy to create BThome V2
compatible devices on different hardware platforms.

### Supported Platforms

- **ESP32** - Uses ArduinoBLE library for reliable BLE operations
- **nRF52** - Uses Adafruit Bluefruit library (Adafruit nRF52)

## Features

- ✅ BThome V2 protocol support
- ✅ Multiple sensor types (temperature, humidity, pressure, CO2, etc.)
- ✅ Binary sensor support (motion, door, window, etc.)
- ✅ Event support (button presses)
- ✅ Platform abstraction (ESP32 and nRF52)
- ✅ Easy-to-use API
- ✅ Encryption support (framework in place)
- ✅ Low power BLE advertising

## Installation

### PlatformIO

Add the library to your `platformio.ini`:

```ini
[env:esp32]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps =
    the78mole/BThomeV2

[env:nrf52]
platform = nordicnrf52
board = adafruit_feather_nrf52840
framework = arduino
lib_deps =
    the78mole/BThomeV2
```

### Arduino IDE

1. Download the library from the GitHub releases page
2. In Arduino IDE, go to Sketch → Include Library → Add .ZIP Library
3. Select the downloaded ZIP file

## Quick Start

### PlatformIO Example (Recommended)

All examples are provided as complete PlatformIO projects with `platformio.ini`
and `src/main.cpp` files.

```bash
# Navigate to an example
cd examples/ESP32_Basic

# Build and upload
pio run --target upload

# Monitor serial output
pio device monitor
```

### Code Example

```cpp
#include <Arduino.h>
#include <BThomeV2.h>

BThomeV2Device bthome;

void setup() {
  // Initialize BThome
  bthome.begin("My-BThome-Device");

  // Add sensor data
  bthome.addTemperature(22.5);    // °C
  bthome.addHumidity(65.0);       // %
  bthome.addBattery(95);          // %

  // Start advertising
  bthome.startAdvertising();
}

void loop() {
  delay(60000); // Wait 1 minute

  // Update sensor readings
  bthome.clearMeasurements();
  bthome.addTemperature(23.0);
  bthome.addHumidity(64.5);
  bthome.addBattery(94);

  // Update advertisement
  bthome.updateAdvertising();
}
```

### Platform Compatibility

The code is identical for ESP32 and nRF52! The library automatically uses the
appropriate BLE stack for your platform (ArduinoBLE for ESP32, Bluefruit for
nRF52).

## API Reference

### Initialization

#### `bool begin(const char* deviceName)`

Initialize the BLE stack with a device name.

```cpp
bthome.begin("My-Sensor");
```

#### `void end()`

Stop BLE advertising and deinitialize the stack.

### Advertising Control

#### `bool startAdvertising()`

Start BLE advertising with current measurements.

#### `void stopAdvertising()`

Stop BLE advertising.

#### `bool updateAdvertising()`

Update the advertising data with new measurements (stops and restarts advertising).

### Adding Measurements

#### `void clearMeasurements()`

Clear all measurements before adding new ones.

#### `void addTemperature(float temperature)`

Add temperature in Celsius (resolution: 0.01°C).

```cpp
bthome.addTemperature(22.5);  // 22.5°C
```

#### `void addHumidity(float humidity)`

Add humidity in percent (resolution: 0.01%).

```cpp
bthome.addHumidity(65.0);  // 65%
```

#### `void addBattery(uint8_t battery)`

Add battery level in percent (0-100).

```cpp
bthome.addBattery(85);  // 85%
```

#### `void addPressure(float pressure)`

Add atmospheric pressure in hPa (resolution: 0.01 hPa).

```cpp
bthome.addPressure(1013.25);  // 1013.25 hPa
```

#### `void addIlluminance(float illuminance)`

Add illuminance in lux (resolution: 0.01 lux).

```cpp
bthome.addIlluminance(500.0);  // 500 lux
```

#### `void addCO2(uint16_t co2)`

Add CO2 level in ppm.

```cpp
bthome.addCO2(450);  // 450 ppm
```

#### `void addBinarySensor(BThomeObjectID objectId, bool state)`

Add a binary sensor state (on/off, open/closed, etc.).

```cpp
bthome.addBinarySensor(MOTION, true);      // Motion detected
bthome.addBinarySensor(DOOR, false);       // Door closed
bthome.addBinarySensor(WINDOW, true);      // Window open
```

#### `void addButtonEvent(uint8_t event)`

Add a button event.

```cpp
bthome.addButtonEvent(0x01);  // Single press
bthome.addButtonEvent(0x02);  // Double press
bthome.addButtonEvent(0x03);  // Triple press
bthome.addButtonEvent(0x80);  // Long press
```

#### `void addMeasurement(BThomeObjectID objectId, const std::vector<uint8_t>& data)`

Add a custom measurement with raw data bytes.

### Supported Sensor Types

The library supports the following BThome V2 object IDs:

**Sensors:**

- `PACKET_ID` - Packet ID
- `BATTERY` - Battery (%)
- `TEMPERATURE` - Temperature (°C)
- `HUMIDITY` - Humidity (%)
- `PRESSURE` - Pressure (hPa)
- `ILLUMINANCE` - Illuminance (lux)
- `MASS_KG` - Mass (kg)
- `MASS_LB` - Mass (lb)
- `DEW_POINT` - Dew point (°C)
- `COUNT` - Count
- `ENERGY` - Energy (kWh)
- `POWER` - Power (W)
- `VOLTAGE` - Voltage (V)
- `PM2_5` - PM2.5 (µg/m³)
- `PM10` - PM10 (µg/m³)
- `CO2` - CO2 (ppm)
- `TVOC` - TVOC (µg/m³)
- `MOISTURE` - Moisture (%)

**Binary Sensors:**

- `BATTERY_LOW`, `BATTERY_CHARGING`
- `CO`, `COLD`, `CONNECTIVITY`
- `DOOR`, `GARAGE_DOOR`, `GAS`
- `HEAT`, `LIGHT`, `LOCK`
- `MOISTURE_BINARY`, `MOTION`, `MOVING`
- `OCCUPANCY`, `OPENING`, `PLUG`
- `POWER_BINARY`, `PRESENCE`, `PROBLEM`
- `RUNNING`, `SAFETY`, `SMOKE`
- `SOUND`, `TAMPER`, `VIBRATION`, `WINDOW`

**Events:**

- `BUTTON` - Button press events
- `DIMMER` - Dimmer events

## Platform-Specific Notes

### ESP32

- Uses ArduinoBLE for BLE operations
- Supports all ESP32 variants (ESP32, ESP32-S3, ESP32-C3, etc.)
- Integrates BTHomeV2-Arduino library for complete BThome V2 encoding
- Reliable BLE advertising with ArduinoBLE stack

### nRF52

**NOTE**
The nRF52 implementation is not working yet due to library issues with the
Seeed nRF52840 board.

- Uses Adafruit Bluefruit library
- Tested on Adafruit Feather nRF52840
- Supports custom MAC address
- Excellent power efficiency

## BThome V2 Protocol

BThome V2 is a format for broadcasting sensor data over Bluetooth Low Energy.
It's designed to be:

- **Efficient**: Compact binary format minimizes power consumption
- **Standardized**: Compatible with Home Assistant and other home automation systems
- **Flexible**: Supports many sensor types and custom data
- **Secure**: Optional encryption support

The library uses the official BThome V2 service UUID **0xFCD2** for BLE advertising.

For more information, visit [bthome.io](https://bthome.io/).

## Examples

See the `examples/` directory for complete working PlatformIO examples:

- **ESP32_Basic** - Basic temperature/humidity sensor for ESP32
- **ESP32_Button** - Button event handling with single/double/triple/long press
- **ESP32_MultipleSensors** - Multiple sensor types and binary sensors
- **nRF52_Basic** - Basic temperature/humidity sensor for nRF52

Each example includes:

- Complete PlatformIO project structure
- `platformio.ini` configuration file
- `src/main.cpp` with fully documented code
- Individual README with build instructions

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Credits

- BThome V2 protocol: [bthome.io](https://bthome.io/)
- ArduinoBLE: [arduino-libraries/ArduinoBLE](https://github.com/arduino-libraries/ArduinoBLE)
- Adafruit nRF52: [adafruit/Adafruit_nRF52_Arduino](https://github.com/adafruit/Adafruit_nRF52_Arduino)
