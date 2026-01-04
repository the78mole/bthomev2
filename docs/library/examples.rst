Examples
========

This page documents the example projects included with the BThomeV2 library.

Available Examples
------------------

The library includes several working examples for different use cases:

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Example
     - Platform
     - Description
   * - ESP32_Basic
     - ESP32
     - ✅ Basic temperature and humidity sensor
   * - ESP32_Button
     - ESP32
     - ✅ Button event handling
   * - ESP32_MultipleSensors
     - ESP32
     - ✅ Multiple sensors combined
   * - nRF52_Basic
     - nRF52
     - ❌ **Not functional** - Basic example (currently broken)

.. warning::
   The nRF52 platform is currently not functional. Examples will not work. Only ESP32 examples are operational.

ESP32_Basic
-----------

**Location:** ``examples/ESP32_Basic/``

A minimal example showing temperature and humidity monitoring.

Features
~~~~~~~~

* Temperature sensor simulation
* Humidity sensor simulation
* Battery level reporting
* Regular updates every 10 seconds

Code Overview
~~~~~~~~~~~~~

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   BThomeV2Device bthome;

   void setup() {
     Serial.begin(115200);
     bthome.begin("ESP32-Basic");

     // Initial measurements
     bthome.addTemperature(22.5);
     bthome.addHumidity(65.0);
     bthome.addBattery(100);

     bthome.startAdvertising();
   }

   void loop() {
     delay(10000);

     // Simulated readings
     float temp = 20.0 + random(0, 50) / 10.0;
     float humidity = 60.0 + random(0, 100) / 10.0;

     // Update
     bthome.clearMeasurements();
     bthome.addTemperature(temp);
     bthome.addHumidity(humidity);
     bthome.addBattery(100);
     bthome.updateAdvertising();
   }

Testing
~~~~~~~

.. code-block:: bash

   # Compile and upload
   cd examples/ESP32_Basic
   pio run --target upload

   # Monitor serial output
   pio device monitor

   # Test with bthome-logger
   bthome-logger -f "ESP32-Basic"

Expected Output
~~~~~~~~~~~~~~~

**Serial Monitor:**

.. code-block:: text

   Starting BThome V2 Basic Example...
   BLE initialized successfully
   Advertising started!
   Updating values: Temp=22.3°C, Humidity=64.5%
   Updating values: Temp=23.1°C, Humidity=62.8%

**bthome-logger:**

.. code-block:: text

   [2026-01-04 10:30:15] ESP32-Basic (E4:65:B8:XX:XX:XX) | RSSI: -45 dBm
     Temperature: 22.3 °C
     Humidity: 64.5 %
     Battery: 100 %

ESP32_Button
------------

**Location:** ``examples/ESP32_Button/``

Demonstrates button event handling with BThome V2.

Features
~~~~~~~~

* Button press detection
* Long press detection (>1 second)
* Event-based advertising updates
* Battery level reporting

Hardware Setup
~~~~~~~~~~~~~~

* ESP32 board
* Push button connected to GPIO 0
* Internal pull-up resistor used

Code Overview
~~~~~~~~~~~~~

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   #define BUTTON_PIN 0
   #define LONG_PRESS_TIME 1000

   BThomeV2Device bthome;
   unsigned long buttonPressStart = 0;
   bool buttonPressed = false;

   void setup() {
     Serial.begin(115200);
     pinMode(BUTTON_PIN, INPUT_PULLUP);

     bthome.begin("ESP32-Button");
     bthome.addBattery(100);
     bthome.startAdvertising();
   }

   void loop() {
     bool currentState = digitalRead(BUTTON_PIN) == LOW;

     if (currentState && !buttonPressed) {
       // Button just pressed
       buttonPressed = true;
       buttonPressStart = millis();
     } else if (!currentState && buttonPressed) {
       // Button released
       buttonPressed = false;
       unsigned long pressDuration = millis() - buttonPressStart;

       // Send appropriate event
       bthome.clearMeasurements();
       if (pressDuration >= LONG_PRESS_TIME) {
         bthome.addButtonEvent(0x04);  // Long press
       } else {
         bthome.addButtonEvent(0x01);  // Short press
       }
       bthome.addBattery(100);
       bthome.updateAdvertising();
     }

     delay(50);
   }

Testing
~~~~~~~

.. code-block:: bash

   # Upload
   cd examples/ESP32_Button
   pio run --target upload

   # Watch for button events
   bthome-logger -f "ESP32-Button"

Expected Output
~~~~~~~~~~~~~~~

**Short Press:**

.. code-block:: text

   [2026-01-04 10:31:22] ESP32-Button (E4:65:B8:XX:XX:XX) | RSSI: -42 dBm
     Button: Press
     Battery: 100 %

**Long Press:**

.. code-block:: text

   [2026-01-04 10:31:30] ESP32-Button (E4:65:B8:XX:XX:XX) | RSSI: -42 dBm
     Button: Long Press
     Battery: 100 %

ESP32_MultipleSensors
---------------------

**Location:** ``examples/ESP32_MultipleSensors/``

Advanced example showing multiple sensor types in one device.

Features
~~~~~~~~

* Temperature
* Humidity
* Pressure
* Illuminance
* CO2
* Battery level
* Updates every 60 seconds

Code Overview
~~~~~~~~~~~~~

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   BThomeV2Device bthome;
   unsigned long lastUpdate = 0;
   const unsigned long UPDATE_INTERVAL = 60000;

   void setup() {
     Serial.begin(115200);
     bthome.begin("Multi-Sensor");

     // Initial values
     bthome.addTemperature(22.5);
     bthome.addHumidity(65.0);
     bthome.addPressure(1013.25);
     bthome.addIlluminance(450.0);
     bthome.addCO2(420);
     bthome.addBattery(100);

     bthome.startAdvertising();
   }

   void loop() {
     if (millis() - lastUpdate >= UPDATE_INTERVAL) {
       lastUpdate = millis();

       // Simulated sensor readings
       float temp = 20.0 + random(0, 100) / 10.0;
       float humidity = 50.0 + random(0, 300) / 10.0;
       float pressure = 1000.0 + random(0, 500) / 10.0;
       float lux = 300.0 + random(0, 3000) / 10.0;
       uint16_t co2 = 400 + random(0, 200);

       // Update all measurements
       bthome.clearMeasurements();
       bthome.addTemperature(temp);
       bthome.addHumidity(humidity);
       bthome.addPressure(pressure);
       bthome.addIlluminance(lux);
       bthome.addCO2(co2);
       bthome.addBattery(100);

       bthome.updateAdvertising();
     }

     delay(1000);
   }

Testing
~~~~~~~

.. code-block:: bash

   cd examples/ESP32_MultipleSensors
   pio run --target upload
   bthome-logger -f "Multi-Sensor"

Expected Output
~~~~~~~~~~~~~~~

.. code-block:: text

   [2026-01-04 10:32:45] Multi-Sensor (E4:65:B8:XX:XX:XX) | RSSI: -48 dBm
     Temperature: 24.2 °C
     Humidity: 58.3 %
     Pressure: 1015.3 hPa
     Illuminance: 623.5 lux
     CO2: 456 ppm
     Battery: 100 %

nRF52_Basic (Not Functional)
-----------------------------

**Location:** ``examples/nRF52_Basic/``

.. warning::
   **This example is currently not functional!**

   The nRF52 platform has runtime issues that cause the device to hang during advertising. Do not use this example until the platform support is fixed.

Known Issues
~~~~~~~~~~~~

* Device hangs during ``startAdvertising()``
* BLE stack does not initialize properly on nRF52
* Platform marked as broken in documentation

See :doc:`platforms` for more information about nRF52 status.

Creating Your Own Example
--------------------------

Template
~~~~~~~~

Use this template to create your own sensor:

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   // Configuration
   #define DEVICE_NAME "My-Sensor"
   #define UPDATE_INTERVAL 60000  // 60 seconds

   BThomeV2Device bthome;
   unsigned long lastUpdate = 0;

   void setup() {
     Serial.begin(115200);

     // Initialize your sensors here
     // ...

     // Initialize BLE
     if (!bthome.begin(DEVICE_NAME)) {
       Serial.println("BLE initialization failed!");
       while (1) delay(1000);
     }

     // Add initial measurements
     bthome.addTemperature(22.5);
     bthome.addBattery(100);

     // Start advertising
     if (bthome.startAdvertising()) {
       Serial.println("Sensor started successfully");
     }
   }

   void loop() {
     if (millis() - lastUpdate >= UPDATE_INTERVAL) {
       lastUpdate = millis();

       // Read your sensors
       float temperature = readYourSensor();

       // Update measurements
       bthome.clearMeasurements();
       bthome.addTemperature(temperature);
       bthome.addBattery(readBatteryLevel());

       // Update advertising
       bthome.updateAdvertising();

       Serial.println("Measurements updated");
     }

     delay(1000);
   }

   // Implement your sensor reading functions
   float readYourSensor() {
     // Replace with actual sensor code
     return 22.5;
   }

   uint8_t readBatteryLevel() {
     // Replace with actual battery reading
     return 100;
   }

Best Practices
~~~~~~~~~~~~~~

1. **Always check initialization:**

   .. code-block:: cpp

      if (!bthome.begin("Device")) {
        // Handle error
      }

2. **Clear before updating:**

   .. code-block:: cpp

      bthome.clearMeasurements();
      bthome.addTemperature(newValue);
      bthome.updateAdvertising();

3. **Include battery level:**

   .. code-block:: cpp

      bthome.addBattery(batteryPercent);

4. **Use appropriate intervals:**

   .. code-block:: cpp

      // 30-300 seconds typical
      const unsigned long UPDATE_INTERVAL = 60000;

5. **Add serial debugging:**

   .. code-block:: cpp

      Serial.print("Temperature: ");
      Serial.println(temperature);

Testing Your Example
---------------------

Local Testing
~~~~~~~~~~~~~

.. code-block:: bash

   # Build
   pio run

   # Upload
   pio run --target upload

   # Monitor
   pio device monitor

With bthome-logger
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Install tool
   uv tool install bthome-logger

   # Watch for your device
   bthome-logger -f "My-Sensor"

   # Verbose output
   bthome-logger -v -f "My-Sensor"

See Also
--------

* :doc:`api` - Complete API reference
* :doc:`sensors` - All available sensor types
* :doc:`platforms` - Platform-specific information
* :doc:`../tools/bthome-logger` - Testing tool documentation
* :doc:`../quickstart` - Getting started guide
