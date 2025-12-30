# nRF52 Basic Example

A basic example demonstrating temperature, humidity, and battery monitoring
with BThome V2 on nRF52.

## Description

This example simulates sensor readings and broadcasts them via BLE using the
BThome V2 protocol. The data updates every 30 seconds. This is identical to
the ESP32_Basic example but configured for nRF52 boards.

## Hardware Requirements

- Adafruit Feather nRF52840 or similar nRF52-based board
- USB cable for power and serial monitoring

## Building and Uploading

### Using PlatformIO CLI

```bash
# Navigate to this example directory
cd examples/nRF52_Basic

# Build the project
pio run

# Upload to board
pio run --target upload

# Monitor serial output
pio device monitor
```

### Using PlatformIO IDE

1. Open this folder in VS Code with PlatformIO extension
2. Click "Build" in the PlatformIO toolbar
3. Click "Upload" to flash to your board
4. Click "Monitor" to view serial output

## Expected Output

```text
BThome V2 nRF52 Example
========================
BThome initialized successfully
Started advertising BThome V2 data

Advertising sensor data:
  Temperature: 21.5 °C
  Humidity: 65.0 %
  Battery: 100 %

Updating sensor data:
  Temperature: 21.6 °C
  Humidity: 65.1 %
  Battery: 99 %
Advertising updated
```

## Testing

You can verify the BLE advertisements using:

- nRF Connect app (Android/iOS) - recommended for Nordic boards
- LightBlue app (iOS)
- Home Assistant with BThome V2 integration
- bthome-logger command-line tool (in this repository or on PyPi)

Look for a device named "BThome-nRF52" broadcasting on service UUID 0xFCD2.

## Platform Notes

The nRF52 implementation uses the Adafruit Bluefruit library, which provides
excellent power efficiency and BLE performance on Nordic hardware.
