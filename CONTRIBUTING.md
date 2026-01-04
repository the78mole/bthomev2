# Contributing to BThomeV2

Thank you for your interest in contributing to the BThomeV2 library! This
document provides guidelines for contributing to the project.

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

> **Note:** The nRF52 implementation is currently broken (runtime hang at
> `Bluefruit.begin()`). Focus development efforts on ESP32 until the nRF52
> issue is resolved.

When adding new features:

- Ensure compatibility with ESP32 platform (nRF52 currently non-functional)
- Use platform-specific implementations in the respective files
- Keep the base class platform-agnostic
- Test on actual hardware when possible
- Help with nRF52 debugging is especially welcome!

### Testing

- Test new features on real hardware
- Use **bthome-logger** to verify BLE advertisements:

  ```bash
  uv tool install bthome-logger
  bthome-logger -f "Your-Device-Name"
  ```

- Verify BLE advertising with a scanner app (nRF Connect, LightBlue, etc.)
- Check compatibility with Home Assistant or other BThome V2 consumers
- Include example sketches for new features

### Documentation

- Update README.md for new features
- Add inline documentation for new public methods
- Update examples if the API changes
- Include usage examples in your PR description
- **Update Sphinx documentation** when changing API or adding features

#### Sphinx Documentation

The project uses Sphinx for comprehensive documentation in `docs/`:

**Building Documentation Locally:**

```bash
cd docs

# Build English version (default)
./build.sh

# Build German version
./build.sh --language de

# Build both languages
./build-all.sh

# Clean build
./build.sh --clean
```

**When to Update Documentation:**

- **API Changes**: Update [docs/library/api.rst](docs/library/api.rst)
- **New Sensors**: Update [docs/library/sensors.rst](docs/library/sensors.rst)
- **New Examples**: Update [docs/library/examples.rst](docs/library/examples.rst)
- **Tool Changes**: Update [docs/tools/bthome-logger.rst](docs/tools/bthome-logger.rst)
- **Workflow Changes**: Update [docs/development/workflow.rst](docs/development/workflow.rst)

**Contributing Translations:**

German translations are managed via `.po` files:

```bash
cd docs

# Update translation templates
uv run --with sphinx --with sphinx-intl sphinx-build -b gettext . _build/gettext
uv run --with sphinx --with sphinx-intl sphinx-intl update -l de

# Edit translation files
# locale/de/LC_MESSAGES/*.po

# Build and test
./build.sh --language de
```

See [docs/I18N.md](docs/I18N.md) for detailed translation guidelines.

**Documentation is automatically built on ReadTheDocs** for each push to `main`.

## BThome V2 Protocol

When implementing new sensor types or features:

- Follow the [BThome V2 specification](https://bthome.io/)
- Use correct data types and byte ordering (little-endian)
- Verify object IDs match the specification
- Test with Home Assistant or other BThome V2 receivers

## Project Structure

```text
bthomev2/
├── .github/workflows/        # CI/CD workflows
│   ├── release.yml          # Main release orchestration
│   ├── pypi-publish.yml     # bthome-logger publishing
│   └── pio-publish.yml      # PlatformIO library publishing
├── docs/                     # Sphinx documentation
│   ├── conf.py              # Sphinx configuration
│   ├── index.rst            # Documentation entry point
│   ├── library/             # Library API documentation
│   ├── tools/               # bthome-logger documentation
│   ├── development/         # Development workflow docs
│   ├── locale/              # Translation files (i18n)
│   ├── build.sh             # Build script (uses uv)
│   └── build-all.sh         # Build all language versions
├── src/                      # Library source files
│   ├── BThomeV2.h           # Base class header and unified device interface
│   ├── BThomeV2.cpp         # Base class implementation
│   ├── BThomeV2_ESP32.cpp   # ESP32-specific implementation
│   └── BThomeV2_nRF52.cpp   # nRF52-specific implementation
├── tools/                    # Supporting tools
│   └── bthome_logger.py     # Python tool for testing BLE advertisements
├── examples/                 # Example sketches
├── library.json.j2          # PlatformIO library manifest template (Jinja2)
├── library.properties.j2    # Arduino library manifest template (Jinja2)
├── library.json             # Generated manifest (version 0.0.0-dev)
├── library.properties       # Generated manifest (version 0.0.0-dev)
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

## Release Process

Releases are automated via GitHub Actions:

1. **Semantic Versioning**: Commit messages determine version bumps
   - `feat:` → minor version bump (0.x.0)
   - `fix:` → patch version bump (0.0.x)
   - `BREAKING CHANGE:` → major version bump (x.0.0)

2. **Automatic Publishing**: On push to `main` (with changes in relevant paths):
   - Version is calculated from commit history
   - GitHub Release is created with tag
   - bthome-logger is published to PyPI
   - BThomeV2 library is published to PlatformIO Registry
   - Both packages receive the same version number

3. **Template System**:
   - `library.json` and `library.properties` are generated from `.j2` templates
   - Repository contains `0.0.0-dev` versions
   - Workflows generate actual versions during release (not committed)

4. **Manual Testing**: Before merging to `main`:
   - Test changes on ESP32 hardware
   - Verify with bthome-logger
   - Update examples if API changes

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Check existing issues and pull requests
- Review the [BThome V2 specification](https://bthome.io/)

## License

By contributing, you agree that your contributions will be licensed under the
MIT License.
