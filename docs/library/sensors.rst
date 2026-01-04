Unterstützte Sensoren
=====================

BThome V2 unterstützt eine Vielzahl von Sensortypen. Diese Seite bietet eine
vollständige Übersicht über alle verfügbaren Sensoren und deren Verwendung.

Messwertsensoren
----------------

Temperatur (0x02)
~~~~~~~~~~~~~~~~~

**Object ID:** ``TEMPERATURE`` (0x02)

**Einheit:** °C (Celsius)

**Auflösung:** 0.01°C

**Datentyp:** Signed 16-bit Integer (little-endian)

**Beispiel:**

.. code-block:: cpp

   bthome.addTemperature(22.5);  // 22.5°C
   bthome.addTemperature(-5.3);  // -5.3°C

Luftfeuchtigkeit (0x03)
~~~~~~~~~~~~~~~~~~~~~~~~

**Object ID:** ``HUMIDITY`` (0x03)

**Einheit:** % (Prozent)

**Auflösung:** 0.01%

**Bereich:** 0-100%

**Datentyp:** Unsigned 16-bit Integer (little-endian)

**Beispiel:**

.. code-block:: cpp

   bthome.addHumidity(65.0);  // 65%
   bthome.addHumidity(45.5);  // 45.5%

Luftdruck (0x04)
~~~~~~~~~~~~~~~~

**Object ID:** ``PRESSURE`` (0x04)

**Einheit:** hPa (Hektopascal)

**Auflösung:** 0.01 hPa

**Datentyp:** Unsigned 24-bit Integer (little-endian)

**Beispiel:**

.. code-block:: cpp

   bthome.addPressure(1013.25);  // 1013.25 hPa
   bthome.addPressure(950.0);    // 950.0 hPa

Beleuchtungsstärke (0x05)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Object ID:** ``ILLUMINANCE`` (0x05)

**Einheit:** lux

**Auflösung:** 0.01 lux

**Datentyp:** Unsigned 24-bit Integer (little-endian)

**Beispiel:**

.. code-block:: cpp

   bthome.addIlluminance(500.0);   // 500 lux
   bthome.addIlluminance(1200.5);  // 1200.5 lux

CO2 (0x12)
~~~~~~~~~~

**Object ID:** ``CO2`` (0x12)

**Einheit:** ppm (parts per million)

**Auflösung:** 1 ppm

**Datentyp:** Unsigned 16-bit Integer (little-endian)

**Beispiel:**

.. code-block:: cpp

   bthome.addCO2(450);   // 450 ppm
   bthome.addCO2(1200);  // 1200 ppm

Batterie (0x01)
~~~~~~~~~~~~~~~

**Object ID:** ``BATTERY`` (0x01)

**Einheit:** % (Prozent)

**Auflösung:** 1%

**Bereich:** 0-100%

**Datentyp:** Unsigned 8-bit Integer

**Beispiel:**

.. code-block:: cpp

   bthome.addBattery(95);  // 95%
   bthome.addBattery(50);  // 50%

Taupunkt (0x08)
~~~~~~~~~~~~~~~

**Object ID:** ``DEW_POINT`` (0x08)

**Einheit:** °C

**Auflösung:** 0.01°C

**Datentyp:** Signed 16-bit Integer (little-endian)

**Beispiel:**

.. code-block:: cpp

   std::vector<uint8_t> dewData = encodeSInt16(1250);  // 12.50°C
   bthome.addMeasurement(DEW_POINT, dewData);

Zähler (0x09)
~~~~~~~~~~~~~

**Object ID:** ``COUNT`` (0x09)

**Einheit:** dimensionslos

**Datentyp:** Unsigned 32-bit Integer (little-endian)

**Beispiel:**

.. code-block:: cpp

   std::vector<uint8_t> countData = encodeUInt32(12345);
   bthome.addMeasurement(COUNT, countData);

Energie (0x0A)
~~~~~~~~~~~~~~

**Object ID:** ``ENERGY`` (0x0A)

**Einheit:** kWh

**Auflösung:** 0.001 kWh

**Datentyp:** Unsigned 24-bit Integer (little-endian)

Leistung (0x0B)
~~~~~~~~~~~~~~~

**Object ID:** ``POWER`` (0x0B)

**Einheit:** W (Watt)

**Auflösung:** 0.01 W

**Datentyp:** Unsigned 24-bit Integer (little-endian)

Spannung (0x0C)
~~~~~~~~~~~~~~~

**Object ID:** ``VOLTAGE`` (0x0C)

**Einheit:** V (Volt)

**Auflösung:** 0.001 V

**Datentyp:** Unsigned 16-bit Integer (little-endian)

Feinstaub PM2.5 (0x0D)
~~~~~~~~~~~~~~~~~~~~~~

**Object ID:** ``PM2_5`` (0x0D)

**Einheit:** µg/m³

**Auflösung:** 1 µg/m³

**Datentyp:** Unsigned 16-bit Integer (little-endian)

Feinstaub PM10 (0x0E)
~~~~~~~~~~~~~~~~~~~~~

**Object ID:** ``PM10`` (0x0E)

**Einheit:** µg/m³

**Auflösung:** 1 µg/m³

**Datentyp:** Unsigned 16-bit Integer (little-endian)

TVOC (0x13)
~~~~~~~~~~~

**Object ID:** ``TVOC`` (0x13)

**Einheit:** µg/m³

**Auflösung:** 1 µg/m³

**Datentyp:** Unsigned 16-bit Integer (little-endian)

Feuchtigkeit (0x14)
~~~~~~~~~~~~~~~~~~~

**Object ID:** ``MOISTURE`` (0x14)

**Einheit:** % (Prozent)

**Auflösung:** 0.01%

**Datentyp:** Unsigned 16-bit Integer (little-endian)

Binärsensoren
-------------

Alle Binärsensoren verwenden die gleiche API:

.. code-block:: cpp

   bthome.addBinarySensor(SENSOR_ID, state);

``state`` ist ``true`` (aktiv/offen) oder ``false`` (inaktiv/geschlossen).

Verfügbare Binärsensoren
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Sensor
     - Object ID
     - Beschreibung
   * - ``BATTERY_LOW``
     - 0x15
     - Batterie niedrig
   * - ``BATTERY_CHARGING``
     - 0x16
     - Batterie lädt
   * - ``CO``
     - 0x17
     - Kohlenmonoxid erkannt
   * - ``COLD``
     - 0x18
     - Kälte erkannt
   * - ``CONNECTIVITY``
     - 0x19
     - Verbindungsstatus
   * - ``DOOR``
     - 0x1A
     - Türstatus (offen/geschlossen)
   * - ``GARAGE_DOOR``
     - 0x1B
     - Garagentorstatus
   * - ``GAS``
     - 0x1C
     - Gas erkannt
   * - ``HEAT``
     - 0x1D
     - Hitze erkannt
   * - ``LIGHT``
     - 0x1E
     - Lichtstatus
   * - ``LOCK``
     - 0x1F
     - Schlossstatus
   * - ``MOISTURE_BINARY``
     - 0x20
     - Feuchtigkeit erkannt
   * - ``MOTION``
     - 0x21
     - Bewegung erkannt
   * - ``MOVING``
     - 0x22
     - Gerät bewegt sich
   * - ``OCCUPANCY``
     - 0x23
     - Raum belegt
   * - ``OPENING``
     - 0x24
     - Öffnung erkannt
   * - ``PLUG``
     - 0x25
     - Steckerstatus
   * - ``POWER_BINARY``
     - 0x26
     - Stromstatus
   * - ``PRESENCE``
     - 0x27
     - Anwesenheit erkannt
   * - ``PROBLEM``
     - 0x28
     - Problem erkannt
   * - ``RUNNING``
     - 0x29
     - Gerät läuft
   * - ``SAFETY``
     - 0x2A
     - Sicherheitsstatus
   * - ``SMOKE``
     - 0x2B
     - Rauch erkannt
   * - ``SOUND``
     - 0x2C
     - Ton erkannt
   * - ``TAMPER``
     - 0x2D
     - Manipulation erkannt
   * - ``VIBRATION``
     - 0x2E
     - Vibration erkannt
   * - ``WINDOW``
     - 0x2F
     - Fensterstatus

Beispiele für Binärsensoren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Bewegungsmelder
   bthome.addBinarySensor(MOTION, true);   // Bewegung erkannt
   bthome.addBinarySensor(MOTION, false);  // Keine Bewegung

   // Türsensor
   bthome.addBinarySensor(DOOR, true);   // Tür offen
   bthome.addBinarySensor(DOOR, false);  // Tür geschlossen

   // Fenstersensor
   bthome.addBinarySensor(WINDOW, true);   // Fenster offen
   bthome.addBinarySensor(WINDOW, false);  // Fenster geschlossen

   // Rauchmelder
   bthome.addBinarySensor(SMOKE, true);   // Rauch erkannt
   bthome.addBinarySensor(SMOKE, false);  // Kein Rauch

   // Batterie-Status
   bthome.addBinarySensor(BATTERY_LOW, true);  // Batterie niedrig

Events
------

Button Events (0x3A)
~~~~~~~~~~~~~~~~~~~~

**Object ID:** ``BUTTON`` (0x3A)

**Datentyp:** Unsigned 8-bit Integer

Button-Events werden verwendet, um Tastenbetätigungen zu übertragen.

**Event-Codes:**

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Code
     - Beschreibung
   * - 0x01
     - Einzelner Tastendruck
   * - 0x02
     - Doppelklick
   * - 0x03
     - Dreifachklick
   * - 0x04
     - Langer Druck

**Beispiel:**

.. code-block:: cpp

   // Einzelner Tastendruck
   bthome.addButtonEvent(0x01);

   // Doppelklick
   bthome.addButtonEvent(0x02);

   // Langer Druck
   bthome.addButtonEvent(0x04);

Dimmer Events (0x3C)
~~~~~~~~~~~~~~~~~~~~

**Object ID:** ``DIMMER`` (0x3C)

**Datentyp:** Unsigned 16-bit Integer (little-endian)

Dimmer-Events übertragen Rotations- oder Dimmer-Informationen.

Mehrere Sensoren kombinieren
-----------------------------

Du kannst mehrere Sensoren in einem Advertisement kombinieren:

.. code-block:: cpp

   bthome.clearMeasurements();

   // Umweltsensoren
   bthome.addTemperature(22.5);
   bthome.addHumidity(65.0);
   bthome.addPressure(1013.25);
   bthome.addCO2(450);

   // Status-Informationen
   bthome.addBattery(95);
   bthome.addBinarySensor(MOTION, false);

   bthome.updateAdvertising();

.. note::
   Die maximale Größe eines BLE-Advertisements ist begrenzt (ca. 31 Bytes Payload).
   Bei zu vielen Sensoren kann das Advertisement nicht vollständig übertragen werden.

Siehe auch
----------

* :doc:`api` - API-Referenz
* :doc:`examples` - Vollständige Beispiele
* `BThome V2 Spezifikation <https://bthome.io/>`_ - Offizielle Dokumentation
