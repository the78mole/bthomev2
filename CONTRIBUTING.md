# Contributing to BThomeV2

Thank you for your interest in contributing to the BThomeV2 library! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your platform (ESP32 variant, nRF52 board, etc.)
- Library version

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear description of the enhancement
- Use cases for the enhancement
- Any relevant examples or references

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test your changes on both ESP32 and nRF52 if possible
5. Commit your changes (`git commit -am 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Create a Pull Request

## Development Guidelines

### Code Style

- Follow the existing code style
- Use descriptive variable and function names
- Add comments for complex logic
- Include Doxygen-style comments for public APIs

### Platform Support

When adding new features:
- Ensure compatibility with both ESP32 and nRF52 platforms
- Use platform-specific implementations in the respective files
- Keep the base class platform-agnostic
- Test on actual hardware when possible

### Testing

- Test new features on real hardware
- Verify BLE advertising with a scanner app (nRF Connect, LightBlue, etc.)
- Check compatibility with Home Assistant or other BThome V2 consumers
- Include example sketches for new features

### Documentation

- Update README.md for new features
- Add inline documentation for new public methods
- Update examples if the API changes
- Include usage examples in your PR description

## BThome V2 Protocol

When implementing new sensor types or features:
- Follow the [BThome V2 specification](https://bthome.io/)
- Use correct data types and byte ordering (little-endian)
- Verify object IDs match the specification
- Test with Home Assistant or other BThome V2 receivers

## Project Structure

```
bthomev2/
├── src/                      # Library source files
│   ├── BThomeV2.h           # Base class header
│   ├── BThomeV2.cpp         # Base class implementation
│   ├── BThomeV2_ESP32.h     # ESP32-specific header
│   ├── BThomeV2_ESP32.cpp   # ESP32-specific implementation
│   ├── BThomeV2_nRF52.h     # nRF52-specific header
│   └── BThomeV2_nRF52.cpp   # nRF52-specific implementation
├── examples/                 # Example sketches
├── library.json             # PlatformIO library manifest
├── library.properties       # Arduino library manifest
└── README.md               # Main documentation
```

## Adding New Sensor Types

To add a new sensor type:

1. Add the object ID to the `BThomeObjectID` enum in `BThomeV2.h`
2. Add a public method in the `BThomeV2` class (e.g., `addMySensor()`)
3. Implement the method in `BThomeV2.cpp` using existing encoding functions
4. Update the README.md with the new sensor type
5. Add an example if appropriate

Example:
```cpp
// In BThomeV2.h
void addVolume(float volume);  // Volume in m³

// In BThomeV2.cpp
void BThomeV2::addVolume(float volume) {
    uint32_t vol = (uint32_t)(volume * 1000.0f);  // Convert to liters
    std::vector<uint8_t> data;
    encodeUInt32(vol, data);
    measurements.push_back(BThomeMeasurement(VOLUME, data));
}
```

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Check existing issues and pull requests
- Review the [BThome V2 specification](https://bthome.io/)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
