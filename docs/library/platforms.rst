Supported Platforms
===================

The BThomeV2 library is designed to support multiple microcontroller platforms through a unified API. However, platform support varies.

Platform Status Overview
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Platform
     - Status
     - Tested
     - Notes
   * - ESP32
     - ✅ Working
     - Yes
     - Fully functional, recommended
   * - nRF52
     - ❌ Broken
     - Yes
     - Runtime issues, not functional

ESP32 Platform
--------------

Status: ✅ **Fully Functional**

The ESP32 platform is fully supported and recommended for production use.

Supported Boards
~~~~~~~~~~~~~~~~

* ESP32 (original)
* ESP32-S2
* ESP32-S3
* ESP32-C3
* ESP32-C6
* Any ESP32-based board with Bluetooth LE support

Requirements
~~~~~~~~~~~~

**PlatformIO:**

.. code-block:: ini

   [env:esp32]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2

**Arduino IDE:**

* ESP32 Board Support via Board Manager
* Install "BThomeV2" library from Library Manager

Dependencies
~~~~~~~~~~~~

* ArduinoBLE (^1.5.0) - automatically installed

Features
~~~~~~~~

* ✅ BLE advertising
* ✅ All sensor types supported
* ✅ Custom MAC address support
* ✅ Stable BLE stack (ArduinoBLE)
* ✅ Low power modes (with additional configuration)
* ✅ OTA updates supported
* ✅ Serial debugging

Tested Boards
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Board
     - Status
     - Notes
   * - ESP32 DevKit V1
     - ✅ Working
     - Reference board, fully tested
   * - ESP32-S3
     - ✅ Working
     - Good performance
   * - ESP32-C3
     - ✅ Working
     - Compact, BLE only (no classic BT)
   * - NodeMCU-32S
     - ✅ Working
     - Popular development board

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

**platformio.ini:**

.. code-block:: ini

   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2
   monitor_speed = 115200
   upload_speed = 921600

Performance
~~~~~~~~~~~

* **Advertising interval:** Configurable, default ~100ms
* **Power consumption:** ~80mA active, <1mA deep sleep
* **Range:** 10-50 meters (depending on environment)
* **Update rate:** Limited by BLE, recommend 30-300 second intervals

Best Practices
~~~~~~~~~~~~~~

1. **Use deep sleep for battery operation:**

   .. code-block:: cpp

      // After advertising update
      bthome.updateAdvertising();
      delay(100);  // Allow advertising
      esp_deep_sleep_start();

2. **Monitor RSSI for range testing:**

   Use ``bthome-logger`` to check signal strength

3. **Use unique device names:**

   .. code-block:: cpp

      // Include MAC or ID in name
      char deviceName[32];
      sprintf(deviceName, "Sensor-%02X", ESP.getEfuseMac() & 0xFF);
      bthome.begin(deviceName);

Known Issues
~~~~~~~~~~~~

* None currently

nRF52 Platform
--------------

Status: ❌ **Not Functional**

.. danger::
   **Do not use nRF52 platform in production!**

   The nRF52 implementation has critical runtime issues and is not functional. Examples will not work. Use ESP32 instead.

Affected Boards
~~~~~~~~~~~~~~~

* Adafruit Feather nRF52840
* Seeed XIAO nRF52840
* Nordic nRF52832/nRF52840 based boards
* Any nRF52-based development board

Issues
~~~~~~

1. **Runtime hang during advertising:**

   Device freezes when calling ``startAdvertising()``

2. **BLE stack initialization problems:**

   Bluefruit library integration issues

3. **Memory corruption:**

   Possible memory issues with service data

Current Status
~~~~~~~~~~~~~~

* ❌ BLE advertising not working
* ❌ Examples fail to run
* ❌ Platform disabled in build
* ❌ Not recommended for any use

What Doesn't Work
~~~~~~~~~~~~~~~~~

* Everything - the entire platform is broken

Workaround
~~~~~~~~~~

**Use ESP32 instead.** The ESP32 platform is fully functional and recommended.

If you need nRF52 specifically, consider:

1. Wait for platform fixes (check GitHub issues)
2. Use native Bluefruit library directly (without BThomeV2)
3. Contribute fixes to the project

Future Plans
~~~~~~~~~~~~

The nRF52 platform may be fixed in future releases, but there is no timeline currently.

Platform Comparison
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Feature
     - ESP32
     - ESP32-S2
     - nRF52
   * - BLE Advertising
     - ✅ Yes
     - ✅ Yes
     - ❌ Broken
   * - BLE + WiFi
     - ✅ Yes
     - ✅ Yes
     - ❌ N/A
   * - Deep Sleep
     - ✅ Yes
     - ✅ Yes
     - ⚠️ Not tested
   * - OTA Updates
     - ✅ Yes
     - ✅ Yes
     - ⚠️ Not tested
   * - Cost
     - Low
     - Low
     - Medium
   * - Power (active)
     - ~80mA
     - ~70mA
     - ~15mA
   * - **Recommendation**
     - ✅ **Use**
     - ✅ **Use**
     - ❌ **Avoid**

Platform Abstraction
--------------------

The library uses platform abstraction to provide a unified API:

Architecture
~~~~~~~~~~~~

.. code-block:: text

   ┌─────────────────────────────┐
   │  Your Application Code      │
   └──────────────┬──────────────┘
                  │
   ┌──────────────▼──────────────┐
   │  BThomeV2 Unified API       │
   │  (BThomeV2Device class)     │
   └──────────────┬──────────────┘
                  │
         ┌────────┴─────────┐
         │                  │
   ┌─────▼──────┐   ┌──────▼─────┐
   │ ESP32      │   │ nRF52      │
   │ Implementation  │ Implementation
   │ (ArduinoBLE)│   │ (Bluefruit)│
   └────────────┘   └────────────┘

Platform-Specific Code
~~~~~~~~~~~~~~~~~~~~~~

**ESP32 (src/BThomeV2_ESP32.cpp):**

* Uses ArduinoBLE library
* NimBLE stack underneath
* Stable and well-tested

**nRF52 (src/BThomeV2_nRF52.cpp):**

* Uses Adafruit Bluefruit library
* SoftDevice BLE stack
* Currently broken

Compile-Time Selection
~~~~~~~~~~~~~~~~~~~~~~

Platform is selected automatically based on ``#define``:

.. code-block:: cpp

   #if defined(ESP32)
     // ESP32 implementation
   #elif defined(NRF52)
     // nRF52 implementation
   #else
     #error "Unsupported platform"
   #endif

Adding New Platforms
--------------------

To add support for a new platform:

Requirements
~~~~~~~~~~~~

1. Bluetooth LE stack
2. BLE advertising support
3. Service data capability
4. Arduino framework compatibility

Steps
~~~~~

1. **Create platform file:**

   ``src/BThomeV2_NEWPLATFORM.cpp``

2. **Implement abstract interface:**

   .. code-block:: cpp

      class BThomeV2Device : public BThomeV2 {
        bool begin(const char* deviceName) override;
        void end() override;
        bool startAdvertising() override;
        void stopAdvertising() override;
        bool setMAC(const uint8_t mac[6]) override;
      };

3. **Add platform detection:**

   In ``BThomeV2.h``:

   .. code-block:: cpp

      #elif defined(NEWPLATFORM)
        #include "BThomeV2_NEWPLATFORM.h"
      #endif

4. **Test thoroughly:**

   * Basic advertising
   * All sensor types
   * Memory usage
   * Stability

5. **Submit pull request:**

   See :doc:`../development/contributing`

Recommendations
---------------

For New Projects
~~~~~~~~~~~~~~~~

**Use ESP32.** It's the only fully functional platform.

Recommended boards:

1. **ESP32 DevKit V1** - Cheap, reliable
2. **ESP32-S3** - More powerful, newer
3. **ESP32-C3** - Compact, cost-effective

For Existing nRF52 Projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Migrate to ESP32** or wait for fixes.

For Battery-Powered Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**ESP32 with deep sleep:**

* Long battery life achievable
* Wake up, measure, advertise, sleep
* Can run months on coin cell

For Production
~~~~~~~~~~~~~~

**ESP32 only.** Do not use nRF52 in production until platform is fixed.

See Also
--------

* :doc:`api` - Complete API reference
* :doc:`examples` - Platform-specific examples
* :doc:`../installation` - Platform installation guides
* :doc:`../development/workflow` - Contributing platform fixes
