# ESP32 Multiple Sensors Example

A comprehensive example showing how to use multiple sensor types and binary
sensors together.

## Description

This example demonstrates a complete sensor station with:

- Temperature sensor
- Humidity sensor
- Pressure sensor
- CO2 sensor
- Battery level
- Motion sensor (binary)
- Door sensor (binary)

All values are simulated and update every 60 seconds, with random events for
motion and door states.

## Hardware Requirements

- ESP32 (any variant)

## Features

- Multiple sensor types in one advertisement
- Binary sensor support (motion, door)
- Automatic updates every 60 seconds
- Random event simulation for motion and door
- Comprehensive sensor value ranges

## Building and Uploading

```bash
cd examples/ESP32_MultipleSensors
pio run --target upload
pio device monitor
```

## Expected Output

```text
BThome V2 Multiple Sensors Example
===================================
BThome initialized successfully
Started advertising BThome V2 data

--- Updating Sensors ---
Temperature:  21.50 °C
Humidity:     65.0 %
Pressure:     1013.25 hPa
CO2:          450 ppm
Battery:      100 %
Motion:       NO
Door:         CLOSED
✓ Advertising updated

Motion DETECTED
--- Updating Sensors ---
Temperature:  21.51 °C
Humidity:     65.1 %
Pressure:     1013.30 hPa
CO2:          448 ppm
Battery:      100 %
Motion:       YES
Door:         CLOSED
✓ Advertising updated
```

## Testing

In Home Assistant, this will create multiple entities:

- `sensor.bthome_temperature`
- `sensor.bthome_humidity`
- `sensor.bthome_pressure`
- `sensor.bthome_co2`
- `sensor.bthome_battery`
- `binary_sensor.bthome_motion`
- `binary_sensor.bthome_door`
