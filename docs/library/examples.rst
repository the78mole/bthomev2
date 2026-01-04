Beispiele
=========

Die BThomeV2 Library enthält mehrere vollständige Beispiel-Projekte im
``examples/`` Verzeichnis.

Verfügbare Beispiele
--------------------

ESP32_Basic
~~~~~~~~~~~

**Pfad:** ``examples/ESP32_Basic/``

**Beschreibung:** Grundlegendes Beispiel mit Temperatur-, Luftfeuchtigkeits-
und Batteriesensoren.

**Features:**

* Einfache Sensor-Integration
* Periodisches Update (alle 60 Sekunden)
* Serial Monitor Ausgabe

**Verwendung:**

.. code-block:: bash

   cd examples/ESP32_Basic
   pio run --target upload
   pio device monitor

**Code-Highlights:**

.. code-block:: cpp

   BThomeV2Device bthome;

   void setup() {
     bthome.begin("ESP32-Sensor");
     bthome.addTemperature(22.5);
     bthome.addHumidity(65.0);
     bthome.addBattery(95);
     bthome.startAdvertising();
   }

ESP32_Button
~~~~~~~~~~~~

**Pfad:** ``examples/ESP32_Button/``

**Beschreibung:** Demonstriert Button-Event-Handling mit verschiedenen
Drucktypen.

**Features:**

* Button-Event-Erkennung
* Single, Double, Triple, Long Press
* Echtzeit-Event-Übertragung

**Verwendung:**

.. code-block:: bash

   cd examples/ESP32_Button
   pio run --target upload
   pio device monitor

   # In anderem Terminal
   bthome-logger -f "ESP32-Button"

**Code-Highlights:**

.. code-block:: cpp

   // Single press
   bthome.addButtonEvent(0x01);

   // Double press
   bthome.addButtonEvent(0x02);

   // Long press
   bthome.addButtonEvent(0x04);

ESP32_MultipleSensors
~~~~~~~~~~~~~~~~~~~~~

**Pfad:** ``examples/ESP32_MultipleSensors/``

**Beschreibung:** Zeigt die Verwendung mehrerer Sensortypen gleichzeitig.

**Features:**

* Mehrere Mess-Sensoren
* Binärsensoren (Motion, Door)
* Kombinierte Advertisement-Daten

**Verwendung:**

.. code-block:: bash

   cd examples/ESP32_MultipleSensors
   pio run --target upload
   pio device monitor

   # In anderem Terminal
   bthome-logger -f "ESP32-Multi"

**Code-Highlights:**

.. code-block:: cpp

   bthome.clearMeasurements();

   // Mess-Sensoren
   bthome.addTemperature(22.5);
   bthome.addHumidity(65.0);
   bthome.addPressure(1013.25);
   bthome.addCO2(450);

   // Binärsensoren
   bthome.addBinarySensor(MOTION, false);
   bthome.addBinarySensor(DOOR, true);

   // Status
   bthome.addBattery(95);

   bthome.updateAdvertising();

nRF52_Basic
~~~~~~~~~~~

**Pfad:** ``examples/nRF52_Basic/``

.. warning::
   Dieses Beispiel kompiliert, funktioniert aber **nicht zur Laufzeit**
   aufgrund von Problemen mit der Bluefruit-Bibliothek.

**Beschreibung:** Grundlegendes Beispiel für nRF52-Boards (nicht funktionsfähig).

Eigene Beispiele erstellen
---------------------------

Struktur
~~~~~~~~

Jedes Beispiel sollte folgende Struktur haben:

.. code-block:: text

   examples/MyExample/
   ├── platformio.ini       # PlatformIO-Konfiguration
   ├── README.md            # Beispiel-Dokumentation
   └── src/
       └── main.cpp         # Hauptcode

platformio.ini Template
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2
   monitor_speed = 115200

main.cpp Template
~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   BThomeV2Device bthome;

   void setup() {
     Serial.begin(115200);

     if (!bthome.begin("My-Device")) {
       Serial.println("BLE init failed!");
       while (1) delay(1000);
     }

     // Add your sensors
     bthome.addTemperature(22.5);

     bthome.startAdvertising();
     Serial.println("Started advertising");
   }

   void loop() {
     delay(10000);

     // Update values
     bthome.clearMeasurements();
     bthome.addTemperature(random(200, 250) / 10.0);
     bthome.updateAdvertising();
   }

Testing mit bthome-logger
--------------------------

Alle Beispiele können mit dem bthome-logger Tool getestet werden:

.. code-block:: bash

   # Terminal 1: Device
   cd examples/ESP32_Basic
   pio run --target upload
   pio device monitor

   # Terminal 2: Logger
   bthome-logger -f "ESP32"

Erwartete Ausgabe im Logger:

.. code-block:: text

   ESP32-Sensor (AA:BB:CC:DD:EE:FF) RSSI: -65 dBm
     Temperature (0x02): 22.50 °C
     Humidity (0x03): 65.00 %
     Battery (0x01): 95 %

Siehe auch
----------

* :doc:`api` - API-Referenz
* :doc:`sensors` - Sensor-Typen
* :doc:`../quickstart` - Quick Start Guide
* :doc:`../tools/bthome-logger` - Logger-Tool
