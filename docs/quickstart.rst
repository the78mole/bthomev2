Quick Start Guide
=================

This guide walks you through creating your first BThome V2 sensor and shows you how to test it with the bthome-logger tool.

Prerequisites
-------------

* ESP32 board (e.g., ESP32 DevKit)
* PlatformIO installed
* Python 3.8+ with uv or pip
* bthome-logger installed (see :doc:`installation`)

Step 1: Create Project
-----------------------

Create a new PlatformIO project:

.. code-block:: bash

   mkdir my-bthome-sensor
   cd my-bthome-sensor
   pio project init --board esp32dev

Step 2: Add Library
--------------------

Edit ``platformio.ini``:

.. code-block:: ini

   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2
   monitor_speed = 115200

Step 3: Write Your First Sensor Code
-------------------------------------

Create ``src/main.cpp``:

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   // Create BThome device
   BThomeV2Device bthome;

   void setup() {
     // Serial interface for debugging
     Serial.begin(115200);
     delay(1000);

     Serial.println("Starting BThome V2 Sensor...");

     // Initialize BLE with device name
     if (!bthome.begin("My-First-Sensor")) {
       Serial.println("Failed to initialize BLE!");
       while (1) delay(1000);
     }

     Serial.println("BLE initialized successfully");

     // Add initial measurements
     bthome.addTemperature(22.5);    // Temperature in °C
     bthome.addHumidity(65.0);       // Humidity in %
     bthome.addBattery(95);          // Battery in %

     // Start advertising
     if (bthome.startAdvertising()) {
       Serial.println("Advertising started!");
     } else {
       Serial.println("Failed to start advertising!");
     }
   }

   void loop() {
     // Wait 10 seconds
     delay(10000);

     // Simulate new measurements
     float temp = 20.0 + (random(0, 50) / 10.0);  // 20.0 - 25.0°C
     float humidity = 60.0 + (random(0, 100) / 10.0);  // 60.0 - 70.0%

     Serial.print("Updating values: Temp=");
     Serial.print(temp);
     Serial.print("°C, Humidity=");
     Serial.print(humidity);
     Serial.println("%");

     // Update measurements
     bthome.clearMeasurements();
     bthome.addTemperature(temp);
     bthome.addHumidity(humidity);
     bthome.addBattery(95);

     // Update advertising data
     bthome.updateAdvertising();
   }

Step 4: Compile and Upload
---------------------------

Compile the project:

.. code-block:: bash

   pio run

Upload to your ESP32:

.. code-block:: bash

   pio run --target upload

Monitor the serial output:

.. code-block:: bash

   pio device monitor

You should see:

.. code-block:: text

   Starting BThome V2 Sensor...
   BLE initialized successfully
   Advertising started!
   Updating values: Temp=22.3°C, Humidity=64.5%
   ...

Step 5: Test with bthome-logger
--------------------------------

Open a new terminal and start the logger:

.. code-block:: bash

   bthome-logger

You should see your sensor's data:

.. code-block:: text

   [2026-01-04 10:30:15] My-First-Sensor (E4:65:B8:XX:XX:XX) | RSSI: -45 dBm
     Temperature: 22.3 °C
     Humidity: 64.5 %
     Battery: 95 %

Filter for your specific device:

.. code-block:: bash

   bthome-logger -f "My-First-Sensor"

Understanding the Code
-----------------------

Basic Structure
~~~~~~~~~~~~~~~

Every BThome V2 sensor program follows this pattern:

1. **Include the library:** ``#include <BThomeV2.h>``
2. **Create device object:** ``BThomeV2Device bthome;``
3. **Initialize in setup():** ``bthome.begin("Device-Name")``
4. **Add measurements:** ``bthome.addTemperature(value)``
5. **Start advertising:** ``bthome.startAdvertising()``
6. **Update in loop():** Clear, add new values, update

Measurement Updates
~~~~~~~~~~~~~~~~~~~

To update measurements:

.. code-block:: cpp

   // Clear old measurements
   bthome.clearMeasurements();

   // Add new measurements
   bthome.addTemperature(newTemp);
   bthome.addHumidity(newHumidity);

   // Update advertising (restarts with new data)
   bthome.updateAdvertising();

Device Names
~~~~~~~~~~~~

The device name appears in:

* Bluetooth scan results
* bthome-logger output
* Home Assistant device list

Choose descriptive names like:

* ``Living-Room-Temp``
* ``Garden-Sensor``
* ``Basement-Climate``

Next Steps
----------

Now that you have a working sensor:

1. **Explore more sensors** - See :doc:`library/sensors` for all available sensor types
2. **Study examples** - Check out :doc:`library/examples` for more complex scenarios
3. **Read the API** - Review the full :doc:`library/api` reference
4. **Advanced testing** - Learn more about :doc:`tools/bthome-logger` features
5. **Add multiple sensors** - Combine temperature, humidity, pressure, and more

Example: Multiple Sensors
--------------------------

Here's a quick example with multiple sensors:

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   BThomeV2Device bthome;

   void setup() {
     Serial.begin(115200);
     bthome.begin("Multi-Sensor");

     // Environmental sensors
     bthome.addTemperature(22.5);
     bthome.addHumidity(65.0);
     bthome.addPressure(1013.25);
     bthome.addBattery(95);

     // Additional measurements
     bthome.addIlluminance(450);    // 450 lux
     bthome.addCO2(420);            // 420 ppm
     bthome.addVOC(50);             // 50 ppb

     bthome.startAdvertising();
   }

   void loop() {
     delay(60000);  // Update every minute

     // Read your real sensors here
     bthome.clearMeasurements();
     bthome.addTemperature(readTemperatureSensor());
     bthome.addHumidity(readHumiditySensor());
     bthome.addPressure(readPressureSensor());
     bthome.addBattery(readBatteryLevel());

     bthome.updateAdvertising();
   }

Troubleshooting
---------------

BLE initialization fails
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:** ``begin()`` returns ``false``

**Solutions:**

* Check that your board supports Bluetooth LE
* Ensure no other BLE code is running
* Verify device name is not too long (max 29 characters)
* Try a simple device name without special characters

Sensor not visible in bthome-logger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:** Logger runs but doesn't show your device

**Solutions:**

* Verify advertising started: check serial output for "Advertising started!"
* Check Bluetooth is enabled on your computer
* Move the ESP32 closer to your computer
* Run logger with ``-v`` for verbose output: ``bthome-logger -v``
* Verify the device name: ``bthome-logger -f "Your-Device-Name"``

Values not updating
~~~~~~~~~~~~~~~~~~~

**Symptoms:** Old values keep appearing

**Solutions:**

* Ensure you call ``clearMeasurements()`` before adding new values
* Verify ``updateAdvertising()`` is called after adding measurements
* Check for errors in serial monitor
* Increase update interval if updates happen too fast

Further Reading
---------------

* :doc:`library/api` - Complete API reference
* :doc:`library/sensors` - All supported sensor types
* :doc:`library/examples` - Real-world examples
* :doc:`library/platforms` - Platform-specific details
* :doc:`tools/bthome-logger` - Testing tool documentation
