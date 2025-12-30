# ESP32 Basic Example

A basic example demonstrating temperature, humidity, and battery monitoring with BThome V2 on ESP32.

## Description

This example simulates sensor readings and broadcasts them via BLE using the BThome V2 protocol. The data updates every 30 seconds.

## Hardware Requirements

- ESP32 (any variant: ESP32, ESP32-S3, ESP32-C3, etc.)
- USB cable for power and serial monitoring

## Building and Uploading

### Using PlatformIO CLI

```bash
# Navigate to this example directory
cd examples/ESP32_Basic

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

```
BThome V2 ESP32 Example
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
- nRF Connect app (Android/iOS)
- LightBlue app (iOS)
- Home Assistant with BThome V2 integration

Look for a device named "BThome-ESP32" broadcasting on service UUID 0x181C.
