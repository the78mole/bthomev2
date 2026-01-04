Supported Sensors
=================

BThome V2 supports a wide variety of sensors and measurements. This page lists all supported sensor types with their object IDs, units, and resolutions.

Measurement Sensors
-------------------

These sensors report numerical values like temperature, humidity, etc.

Environmental Sensors
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Sensor
     - Object ID
     - Unit
     - Resolution
     - API Function
   * - Temperature
     - 0x02
     - °C
     - 0.01
     - ``addTemperature(float)``
   * - Humidity
     - 0x03
     - %
     - 0.01
     - ``addHumidity(float)``
   * - Pressure
     - 0x04
     - hPa
     - 0.01
     - ``addPressure(float)``
   * - Dew Point
     - 0x08
     - °C
     - 0.01
     - ``addMeasurement()``
   * - Moisture
     - 0x14
     - %
     - 0.01
     - ``addMeasurement()``

Light Sensors
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Sensor
     - Object ID
     - Unit
     - Resolution
     - API Function
   * - Illuminance
     - 0x05
     - lux
     - 0.01
     - ``addIlluminance(float)``

Air Quality Sensors
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Sensor
     - Object ID
     - Unit
     - Resolution
     - API Function
   * - CO2
     - 0x12
     - ppm
     - 1
     - ``addCO2(uint16_t)``
   * - TVOC
     - 0x13
     - ppb
     - 1
     - ``addMeasurement()``
   * - PM2.5
     - 0x0D
     - µg/m³
     - 1
     - ``addMeasurement()``
   * - PM10
     - 0x0E
     - µg/m³
     - 1
     - ``addMeasurement()``

Power Sensors
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Sensor
     - Object ID
     - Unit
     - Resolution
     - API Function
   * - Battery
     - 0x01
     - %
     - 1
     - ``addBattery(uint8_t)``
   * - Voltage
     - 0x0C
     - V
     - 0.001
     - ``addMeasurement()``
   * - Power
     - 0x0B
     - W
     - 0.01
     - ``addMeasurement()``
   * - Energy
     - 0x0A
     - kWh
     - 0.001
     - ``addMeasurement()``

Other Sensors
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Sensor
     - Object ID
     - Unit
     - Resolution
     - API Function
   * - Mass (kg)
     - 0x06
     - kg
     - 0.01
     - ``addMeasurement()``
   * - Mass (lb)
     - 0x07
     - lb
     - 0.01
     - ``addMeasurement()``
   * - Count
     - 0x09
     - -
     - 1
     - ``addMeasurement()``

Binary Sensors
--------------

Binary sensors report on/off or detected/not detected states.

Safety & Security
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Sensor
     - Object ID
     - States (false/true)
   * - Door
     - 0x1A
     - Closed / Open
   * - Garage Door
     - 0x1B
     - Closed / Open
   * - Window
     - 0x2F
     - Closed / Open
   * - Lock
     - 0x1F
     - Locked / Unlocked
   * - Opening
     - 0x24
     - Closed / Open
   * - Tamper
     - 0x2D
     - Off / On
   * - Safety
     - 0x2A
     - Unsafe / Safe

Detection Sensors
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Sensor
     - Object ID
     - States (false/true)
   * - Motion
     - 0x21
     - Clear / Detected
   * - Occupancy
     - 0x23
     - Clear / Detected
   * - Presence
     - 0x27
     - Away / Home
   * - Moving
     - 0x22
     - Not Moving / Moving
   * - Vibration
     - 0x2E
     - Clear / Detected
   * - Sound
     - 0x2C
     - Clear / Detected

Hazard Sensors
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Sensor
     - Object ID
     - States (false/true)
   * - Smoke
     - 0x2B
     - Clear / Detected
   * - CO (Carbon Monoxide)
     - 0x17
     - Clear / Detected
   * - Gas
     - 0x1C
     - Clear / Detected
   * - Problem
     - 0x28
     - OK / Problem
   * - Moisture (Binary)
     - 0x20
     - Dry / Wet

Power & Connectivity
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Sensor
     - Object ID
     - States (false/true)
   * - Battery Low
     - 0x15
     - Normal / Low
   * - Battery Charging
     - 0x16
     - Not Charging / Charging
   * - Plug
     - 0x25
     - Unplugged / Plugged
   * - Power
     - 0x26
     - Off / On
   * - Running
     - 0x29
     - Not Running / Running
   * - Connectivity
     - 0x19
     - Disconnected / Connected

Environment
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Sensor
     - Object ID
     - States (false/true)
   * - Cold
     - 0x18
     - Normal / Cold
   * - Heat
     - 0x1D
     - Normal / Hot
   * - Light
     - 0x1E
     - Off / On

Events
------

Events represent user interactions or state changes.

Button Events
~~~~~~~~~~~~~

Object ID: 0x3A

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Event
     - Value
     - Description
   * - None
     - 0x00
     - No event (used to clear previous event)
   * - Press
     - 0x01
     - Single button press
   * - Double Press
     - 0x02
     - Button pressed twice quickly
   * - Triple Press
     - 0x03
     - Button pressed three times quickly
   * - Long Press
     - 0x04
     - Button held for extended time

**API Function:** ``addButtonEvent(uint8_t event)``

**Example:**

.. code-block:: cpp

   // Single press
   bthome.addButtonEvent(0x01);

   // Long press
   bthome.addButtonEvent(0x04);

Dimmer Events
~~~~~~~~~~~~~

Object ID: 0x3C

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Event
     - Value
     - Description
   * - Rotate Left (1 step)
     - 0x01
     - Dimmer rotated counter-clockwise
   * - Rotate Right (1 step)
     - 0x02
     - Dimmer rotated clockwise

**Example:**

.. code-block:: cpp

   // Rotate right
   std::vector<uint8_t> data = {0x02};
   bthome.addMeasurement(DIMMER, data);

Usage Examples
--------------

Combining Multiple Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can combine multiple measurements in a single advertisement:

.. code-block:: cpp

   BThomeV2Device bthome;
   bthome.begin("Multi-Sensor");

   // Environmental monitoring
   bthome.addTemperature(22.5);
   bthome.addHumidity(65.0);
   bthome.addPressure(1013.25);
   bthome.addIlluminance(450.0);

   // Air quality
   bthome.addCO2(420);

   // Power
   bthome.addBattery(95);

   bthome.startAdvertising();

Binary Sensor Example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Door/window sensor
   bool doorOpen = digitalRead(DOOR_PIN);
   bthome.clearMeasurements();
   bthome.addBinarySensor(DOOR, doorOpen);
   bthome.addBattery(batteryLevel);
   bthome.updateAdvertising();

Motion Sensor Example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // PIR motion sensor
   bool motionDetected = digitalRead(PIR_PIN);
   bthome.clearMeasurements();
   bthome.addBinarySensor(MOTION, motionDetected);
   bthome.addBattery(batteryLevel);
   bthome.updateAdvertising();

Button Example
~~~~~~~~~~~~~~

.. code-block:: cpp

   // Detect button press type
   if (shortPress) {
     bthome.clearMeasurements();
     bthome.addButtonEvent(0x01);  // Single press
     bthome.updateAdvertising();
   } else if (longPress) {
     bthome.clearMeasurements();
     bthome.addButtonEvent(0x04);  // Long press
     bthome.updateAdvertising();
   }

Payload Size Considerations
----------------------------

BLE advertising packets have a maximum payload of 31 bytes. The BThome V2 format uses some bytes for headers and device information, leaving approximately 20-25 bytes for sensor data.

Typical Sensor Sizes
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Sensor Type
     - Bytes
     - Example Combination
   * - Temperature
     - 3 bytes
     - ~7 temperature sensors max
   * - Humidity
     - 3 bytes
     - Temp + Humidity + Pressure + Battery (12 bytes)
   * - Pressure
     - 4 bytes
     - Full climate station (15 bytes)
   * - Battery
     - 2 bytes
     - Most combinations include this
   * - CO2
     - 3 bytes
     - Air quality + climate (18 bytes)
   * - Binary Sensor
     - 2 bytes
     - Multiple binary sensors fit easily
   * - Button Event
     - 2 bytes
     - Event + battery

Recommendations
~~~~~~~~~~~~~~~

* **Keep it simple**: 3-5 measurements per advertisement
* **Essential first**: Always include battery level
* **Test payload size**: Use bthome-logger to verify all data transmits
* **Split if needed**: Create multiple devices for many sensors

Sensor Categories
-----------------

Quick Reference by Use Case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Climate Monitoring:**

* Temperature
* Humidity
* Pressure
* Dew Point

**Air Quality:**

* CO2
* TVOC
* PM2.5
* PM10

**Security:**

* Door
* Window
* Motion
* Tamper
* Smoke
* Gas

**Energy:**

* Battery
* Power
* Energy
* Voltage

**User Input:**

* Button (events)
* Dimmer (events)

Home Assistant Integration
---------------------------

All these sensors are automatically recognized by Home Assistant when using the BTHome integration. The sensors will appear with appropriate units and icons.

**Auto-discovered as:**

* Temperature → Temperature entity (°C)
* Humidity → Humidity entity (%)
* Motion → Binary sensor (motion)
* Door → Binary sensor (door)
* Button → Event entity
* Battery → Battery entity (%)

See Also
--------

* :doc:`api` - Complete API reference
* :doc:`examples` - Real-world examples
* :doc:`../tools/bthome-logger` - Testing tool
* `BThome V2 Specification <https://bthome.io/format/>`_ - Official specification
