# ESP32 Button Example

Demonstrates button event handling with BThome V2, including single, double, triple, and long press detection.

## Description

This example shows how to send button events via BThome V2. It uses the built-in BOOT button (GPIO 0) on most ESP32 development boards.

## Hardware Requirements

- ESP32 (any variant)
- Uses built-in BOOT button (GPIO 0) or connect your own button to GPIO 0

## Button Events

- **Single Press**: Short press and release
- **Double Press**: Two quick presses within 500ms
- **Triple Press**: Three quick presses within 500ms
- **Long Press**: Hold for 1 second or longer

## Building and Uploading

```bash
cd examples/ESP32_Button
pio run --target upload
pio device monitor
```

## Expected Output

```
BThome V2 Button Example
========================
BThome initialized successfully
Started advertising

Waiting for button press...
  Single press = 0x01
  Double press = 0x02
  Triple press = 0x03
  Long press   = 0x80

Button pressed
Short press #1
Single press event
Button event sent via BLE
```

## Testing

Monitor button events in:
- Serial output (as shown above)
- Home Assistant (button entity)
- BLE scanner apps (nRF Connect, LightBlue)
