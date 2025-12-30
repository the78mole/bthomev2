# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-30

### Added
- Initial release of BThomeV2 library
- Support for ESP32 platform using NimBLE-Arduino
- Support for nRF52 platform using Adafruit Bluefruit
- Base class with common BThome V2 protocol implementation
- Platform-specific implementations for ESP32 and nRF52
- Support for multiple sensor types:
  - Temperature (°C)
  - Humidity (%)
  - Battery (%)
  - Pressure (hPa)
  - Illuminance (lux)
  - CO2 (ppm)
  - And more according to BThome V2 specification
- Support for binary sensors (motion, door, window, etc.)
- Support for button events (single, double, triple press, long press)
- Four example sketches:
  - ESP32_Basic: Basic temperature/humidity sensor
  - nRF52_Basic: Basic temperature/humidity sensor for nRF52
  - ESP32_Button: Button event handling
  - ESP32_MultipleSensors: Multiple sensor types example
- Comprehensive README with API documentation
- Keywords file for Arduino IDE syntax highlighting
- Example PlatformIO configuration
- Contributing guidelines
- MIT License

### Platform Support
- ESP32 (all variants: ESP32, ESP32-S3, ESP32-C3, etc.)
- nRF52 (nRF52840, nRF52832 via Adafruit boards)

### Dependencies
- NimBLE-Arduino ^1.4.1 (for ESP32)
- Adafruit nRF52 (for nRF52)

[1.0.0]: https://github.com/the78mole/bthomev2/releases/tag/v1.0.0
