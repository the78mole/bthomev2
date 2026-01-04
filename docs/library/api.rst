API Reference
=============

The BThomeV2 library provides a simple and unified API for creating BThome V2-compatible BLE sensors.

BThomeV2Device Class
--------------------

The central class for working with BThome V2 sensors.

Initialization
~~~~~~~~~~~~~~

.. cpp:function:: bool begin(const char* deviceName)

   Initializes the BLE stack with a device name.

   :param deviceName: Name of the BLE device (max 29 characters)
   :return: ``true`` on success, ``false`` on error
   :rtype: bool

   **Example:**

   .. code-block:: cpp

      BThomeV2Device bthome;
      if (bthome.begin("My-Sensor")) {
        Serial.println("BLE initialized");
      }

.. cpp:function:: void end()

   Stops BLE advertising and deinitializes the stack.

   **Example:**

   .. code-block:: cpp

      bthome.end();

Advertising Control
~~~~~~~~~~~~~~~~~~~

.. cpp:function:: bool startAdvertising()

   Starts BLE advertising with current measurements.

   :return: ``true`` on success, ``false`` on error
   :rtype: bool

   **Example:**

   .. code-block:: cpp

      bthome.addTemperature(22.5);
      bthome.startAdvertising();

.. cpp:function:: void stopAdvertising()

   Stops BLE advertising.

   **Example:**

   .. code-block:: cpp

      bthome.stopAdvertising();

.. cpp:function:: bool updateAdvertising()

   Updates advertising data with new measurements. Automatically stops and restarts advertising.

   :return: ``true`` on success, ``false`` on error
   :rtype: bool

   **Example:**

   .. code-block:: cpp

      bthome.clearMeasurements();
      bthome.addTemperature(23.0);
      bthome.updateAdvertising();

Measurement Management
~~~~~~~~~~~~~~~~~~~~~~

.. cpp:function:: void clearMeasurements()

   Clears all measurements before adding new values.

   **Example:**

   .. code-block:: cpp

      bthome.clearMeasurements();
      bthome.addTemperature(22.5);

Adding Sensors
~~~~~~~~~~~~~~

Temperature
^^^^^^^^^^^

.. cpp:function:: void addTemperature(float temperature)

   Adds a temperature measurement.

   :param temperature: Temperature in °C (resolution: 0.01°C)
   :type temperature: float

   **Example:**

   .. code-block:: cpp

      bthome.addTemperature(22.5);  // 22.5°C

Humidity
^^^^^^^^

.. cpp:function:: void addHumidity(float humidity)

   Adds a humidity measurement.

   :param humidity: Humidity in % (resolution: 0.01%, range: 0-100)
   :type humidity: float

   **Example:**

   .. code-block:: cpp

      bthome.addHumidity(65.0);  // 65%

Battery
^^^^^^^

.. cpp:function:: void addBattery(uint8_t battery)

   Adds a battery level measurement.

   :param battery: Battery level in % (range: 0-100)
   :type battery: uint8_t

   **Example:**

   .. code-block:: cpp

      bthome.addBattery(95);  // 95%

Pressure
^^^^^^^^

.. cpp:function:: void addPressure(float pressure)

   Adds an air pressure measurement.

   :param pressure: Pressure in hPa (resolution: 0.01 hPa)
   :type pressure: float

   **Example:**

   .. code-block:: cpp

      bthome.addPressure(1013.25);  // 1013.25 hPa

Illuminance
^^^^^^^^^^^

.. cpp:function:: void addIlluminance(float illuminance)

   Adds an illuminance measurement.

   :param illuminance: Illuminance in lux (resolution: 0.01 lux)
   :type illuminance: float

   **Example:**

   .. code-block:: cpp

      bthome.addIlluminance(450.0);  // 450 lux

CO2
^^^

.. cpp:function:: void addCO2(uint16_t co2)

   Adds a CO2 concentration measurement.

   :param co2: CO2 concentration in ppm (parts per million)
   :type co2: uint16_t

   **Example:**

   .. code-block:: cpp

      bthome.addCO2(420);  // 420 ppm

Binary Sensors
~~~~~~~~~~~~~~

.. cpp:function:: void addBinarySensor(BThomeObjectID objectId, bool state)

   Adds a binary sensor state.

   :param objectId: Binary sensor object ID (see :doc:`sensors`)
   :param state: Sensor state (true = on/detected, false = off/not detected)
   :type objectId: BThomeObjectID
   :type state: bool

   **Example:**

   .. code-block:: cpp

      // Door sensor
      bthome.addBinarySensor(DOOR, true);  // Door open

      // Motion sensor
      bthome.addBinarySensor(MOTION, true);  // Motion detected

      // Window sensor
      bthome.addBinarySensor(WINDOW, false);  // Window closed

Available Binary Sensors
^^^^^^^^^^^^^^^^^^^^^^^^^

* ``BATTERY_LOW`` - Low battery indicator
* ``BATTERY_CHARGING`` - Charging indicator
* ``CO`` - Carbon monoxide detected
* ``COLD`` - Cold temperature detected
* ``CONNECTIVITY`` - Network connectivity
* ``DOOR`` - Door open/closed
* ``GARAGE_DOOR`` - Garage door open/closed
* ``GAS`` - Gas detected
* ``HEAT`` - Heat detected
* ``LIGHT`` - Light on/off
* ``LOCK`` - Lock locked/unlocked
* ``MOISTURE_BINARY`` - Moisture detected
* ``MOTION`` - Motion detected
* ``MOVING`` - Movement detected
* ``OCCUPANCY`` - Room occupied
* ``OPENING`` - Opening detected
* ``PLUG`` - Plug on/off
* ``POWER_BINARY`` - Power on/off
* ``PRESENCE`` - Presence detected
* ``PROBLEM`` - Problem detected
* ``RUNNING`` - Running state
* ``SAFETY`` - Safety state
* ``SMOKE`` - Smoke detected
* ``SOUND`` - Sound detected
* ``TAMPER`` - Tamper detected
* ``VIBRATION`` - Vibration detected
* ``WINDOW`` - Window open/closed

Events
~~~~~~

Button Events
^^^^^^^^^^^^^

.. cpp:function:: void addButtonEvent(uint8_t event)

   Adds a button press event.

   :param event: Event type
   :type event: uint8_t

   **Event Types:**

   * ``0x00`` - None (no event)
   * ``0x01`` - Press (single press)
   * ``0x02`` - Double press
   * ``0x03`` - Triple press
   * ``0x04`` - Long press

   **Example:**

   .. code-block:: cpp

      // Single press
      bthome.addButtonEvent(0x01);

      // Long press
      bthome.addButtonEvent(0x04);

Advanced Functions
~~~~~~~~~~~~~~~~~~

Custom Measurements
^^^^^^^^^^^^^^^^^^^

.. cpp:function:: void addMeasurement(BThomeObjectID objectId, const std::vector<uint8_t>& data)

   Adds a custom measurement with raw data.

   :param objectId: Object ID from BThome specification
   :param data: Raw data bytes for the measurement
   :type objectId: BThomeObjectID
   :type data: const std::vector<uint8_t>&

   **Example:**

   .. code-block:: cpp

      // Custom sensor with 2-byte data
      std::vector<uint8_t> customData = {0x12, 0x34};
      bthome.addMeasurement(CUSTOM_ID, customData);

Encryption (Optional)
^^^^^^^^^^^^^^^^^^^^^

.. cpp:function:: bool setEncryptionKey(const uint8_t key[16])

   Sets the encryption key for encrypted advertising.

   :param key: 16-byte encryption key
   :return: ``true`` if key was set, ``false`` otherwise
   :rtype: bool

.. cpp:function:: void setEncryption(bool enabled)

   Enables or disables encryption.

   :param enabled: true to enable, false to disable
   :type enabled: bool

.. cpp:function:: bool isEncryptionEnabled() const

   Checks if encryption is enabled.

   :return: ``true`` if encryption is enabled
   :rtype: bool

   **Example:**

   .. code-block:: cpp

      uint8_t key[16] = {0x01, 0x02, /* ... */};
      bthome.setEncryptionKey(key);
      bthome.setEncryption(true);

MAC Address (Platform-Specific)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. cpp:function:: bool setMAC(const uint8_t mac[6])

   Sets a custom MAC address for the device (if supported by platform).

   :param mac: 6-byte MAC address
   :return: ``true`` if MAC was set, ``false`` if not supported
   :rtype: bool

   **Example:**

   .. code-block:: cpp

      uint8_t mac[6] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF};
      bthome.setMAC(mac);

Complete Example
----------------

Here's a complete example using multiple API functions:

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   BThomeV2Device bthome;
   unsigned long lastUpdate = 0;
   const unsigned long UPDATE_INTERVAL = 60000;  // 60 seconds

   void setup() {
     Serial.begin(115200);

     // Initialize BLE
     if (!bthome.begin("Climate-Sensor")) {
       Serial.println("BLE init failed!");
       while (1) delay(1000);
     }

     // Add initial measurements
     bthome.addTemperature(22.5);
     bthome.addHumidity(65.0);
     bthome.addPressure(1013.25);
     bthome.addBattery(100);

     // Start advertising
     bthome.startAdvertising();
     Serial.println("Sensor started");
   }

   void loop() {
     // Update every minute
     if (millis() - lastUpdate >= UPDATE_INTERVAL) {
       lastUpdate = millis();

       // Read sensors (simulated here)
       float temp = readTemperature();
       float humidity = readHumidity();
       float pressure = readPressure();
       uint8_t battery = readBatteryLevel();

       // Update measurements
       bthome.clearMeasurements();
       bthome.addTemperature(temp);
       bthome.addHumidity(humidity);
       bthome.addPressure(pressure);
       bthome.addBattery(battery);

       // Update advertising
       bthome.updateAdvertising();

       Serial.println("Measurements updated");
     }

     delay(1000);
   }

   // Simulated sensor reading functions
   float readTemperature() { return 20.0 + random(0, 100) / 10.0; }
   float readHumidity() { return 50.0 + random(0, 200) / 10.0; }
   float readPressure() { return 1000.0 + random(0, 500) / 10.0; }
   uint8_t readBatteryLevel() { return 80 + random(0, 21); }

Best Practices
--------------

Update Frequency
~~~~~~~~~~~~~~~~

* **Don't update too frequently**: BLE advertising can drain battery
* **Recommended intervals**: 30-300 seconds for most sensors
* **Consider battery impact**: Longer intervals save power

Memory Management
~~~~~~~~~~~~~~~~~

* **Clear before updating**: Always call ``clearMeasurements()`` before adding new values
* **Limit measurements**: BLE payload is limited to 31 bytes
* **Combine wisely**: Too many sensors in one advertisement may not fit

Error Handling
~~~~~~~~~~~~~~

.. code-block:: cpp

   // Always check initialization
   if (!bthome.begin("Device")) {
     Serial.println("Failed to initialize!");
     // Handle error appropriately
   }

   // Check advertising status
   if (!bthome.startAdvertising()) {
     Serial.println("Failed to start advertising!");
   }

Device Naming
~~~~~~~~~~~~~

* **Use descriptive names**: "Living-Room-Temp" not "Sensor1"
* **Keep it short**: Max 29 characters
* **Avoid special characters**: Stick to alphanumeric and hyphens
* **Be consistent**: Use same naming scheme across devices

Platform Differences
--------------------

The API is unified across platforms, but there are some differences:

ESP32
~~~~~

* ✅ Fully functional
* ✅ All features supported
* ✅ Stable BLE stack (ArduinoBLE)
* ✅ Custom MAC address supported

nRF52
~~~~~

* ⚠️ Currently not functional
* ❌ Runtime issues with advertising
* ❌ Not recommended for production

See :doc:`platforms` for detailed platform information.

See Also
--------

* :doc:`sensors` - Complete list of all supported sensors
* :doc:`examples` - Real-world code examples
* :doc:`platforms` - Platform-specific information
* :doc:`../tools/bthome-logger` - Testing tool documentation
