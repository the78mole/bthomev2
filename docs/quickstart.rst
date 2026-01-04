Quick Start Guide
=================

Dieser Guide führt dich durch die Erstellung deines ersten BThome V2-Sensors und
zeigt, wie du ihn mit dem bthome-logger Tool testest.

Voraussetzungen
---------------

* ESP32-Board (z.B. ESP32 DevKit)
* PlatformIO installiert
* Python 3.8+ mit uv oder pip
* bthome-logger installiert (siehe :doc:`installation`)

Schritt 1: Projekt erstellen
-----------------------------

Erstelle ein neues PlatformIO-Projekt:

.. code-block:: bash

   mkdir my-bthome-sensor
   cd my-bthome-sensor
   pio project init --board esp32dev

Schritt 2: Library hinzufügen
------------------------------

Bearbeite ``platformio.ini``:

.. code-block:: ini

   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2
   monitor_speed = 115200

Schritt 3: Ersten Sensor-Code schreiben
----------------------------------------

Erstelle ``src/main.cpp``:

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   // BThome-Device erstellen
   BThomeV2Device bthome;

   void setup() {
     // Serielle Schnittstelle für Debugging
     Serial.begin(115200);
     delay(1000);

     Serial.println("Starting BThome V2 Sensor...");

     // BLE mit Gerätenamen initialisieren
     if (!bthome.begin("My-First-Sensor")) {
       Serial.println("Failed to initialize BLE!");
       while (1) delay(1000);
     }

     Serial.println("BLE initialized successfully");

     // Initiale Messwerte hinzufügen
     bthome.addTemperature(22.5);    // Temperatur in °C
     bthome.addHumidity(65.0);       // Luftfeuchtigkeit in %
     bthome.addBattery(95);          // Batterie in %

     // Advertising starten
     if (bthome.startAdvertising()) {
       Serial.println("Advertising started!");
     } else {
       Serial.println("Failed to start advertising!");
     }
   }

   void loop() {
     // Warte 10 Sekunden
     delay(10000);

     // Simuliere neue Messwerte
     float temp = 20.0 + (random(0, 50) / 10.0);  // 20.0 - 25.0°C
     float humidity = 60.0 + (random(0, 100) / 10.0);  // 60.0 - 70.0%

     Serial.print("Updating values: Temp=");
     Serial.print(temp);
     Serial.print("°C, Humidity=");
     Serial.print(humidity);
     Serial.println("%");

     // Messwerte aktualisieren
     bthome.clearMeasurements();
     bthome.addTemperature(temp);
     bthome.addHumidity(humidity);
     bthome.addBattery(95);

     // Advertising mit neuen Werten aktualisieren
     bthome.updateAdvertising();
   }

Schritt 4: Kompilieren und hochladen
-------------------------------------

.. code-block:: bash

   # Kompilieren
   pio run

   # Hochladen
   pio run --target upload

   # Serial Monitor öffnen
   pio device monitor

Du solltest folgende Ausgabe sehen:

.. code-block:: text

   Starting BThome V2 Sensor...
   BLE initialized successfully
   Advertising started!
   Updating values: Temp=22.3°C, Humidity=65.4%
   Updating values: Temp=23.1°C, Humidity=64.8%
   ...

Schritt 5: Mit bthome-logger testen
------------------------------------

Öffne ein neues Terminal und starte den Logger:

.. code-block:: bash

   bthome-logger -f "My-First-Sensor"

Du solltest die BLE-Advertisements sehen:

.. code-block:: text

   My-First-Sensor (AA:BB:CC:DD:EE:FF) RSSI: -65 dBm
     Temperature (0x02): 22.30 °C
     Humidity (0x03): 65.40 %
     Battery (0x01): 95 %

   My-First-Sensor (AA:BB:CC:DD:EE:FF) RSSI: -64 dBm
     Temperature (0x02): 23.10 °C
     Humidity (0x03): 64.80 %
     Battery (0x01): 95 %

Gratulation! 🎉
---------------

Du hast erfolgreich:

* ✅ Einen BThome V2-Sensor erstellt
* ✅ BLE-Advertising implementiert
* ✅ Die Advertisements mit bthome-logger empfangen und dekodiert

Nächste Schritte
----------------

Weitere Sensortypen hinzufügen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Druck-Sensor
   bthome.addPressure(1013.25);  // hPa

   // CO2-Sensor
   bthome.addCO2(450);  // ppm

   // Lichtsensor
   bthome.addIlluminance(500.0);  // lux

Binärsensoren verwenden
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Bewegungsmelder
   bthome.addBinarySensor(MOTION, true);  // Bewegung erkannt

   // Tür-Sensor
   bthome.addBinarySensor(DOOR, false);  // Tür geschlossen

   // Fenster-Sensor
   bthome.addBinarySensor(WINDOW, true);  // Fenster offen

Button-Events senden
~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Einzelner Tastendruck
   bthome.addButtonEvent(0x01);

   // Doppelklick
   bthome.addButtonEvent(0x02);

   // Langer Druck
   bthome.addButtonEvent(0x04);

Weitere Ressourcen
------------------

* :doc:`library/api` - Vollständige API-Referenz
* :doc:`library/examples` - Weitere Beispiele
* :doc:`library/sensors` - Alle unterstützten Sensoren
* :doc:`tools/bthome-logger` - Logger-Tool Dokumentation
* :doc:`development/workflow` - Entwicklungs-Workflow

Probleme?
---------

* Überprüfe die :doc:`library/platforms` für plattformspezifische Hinweise
* Stelle Fragen in den `GitHub Issues <https://github.com/the78mole/bthomev2/issues>`_
* Lies den :doc:`development/contributing` Guide
