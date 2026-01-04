bthome-logger Tool
==================

Das **bthome-logger** Tool ist ein Python-basiertes Kommandozeilenwerkzeug zum
Empfangen und Dekodieren von BThome V2 BLE-Advertisements. Es ist perfekt für
das Testing und Debugging von BThome V2-Geräten geeignet.

Installation
------------

Empfohlene Installation mit uv:

.. code-block:: bash

   uv tool install bthome-logger

Alternative mit pip:

.. code-block:: bash

   pip install bthome-logger

Verwendung
----------

Grundlegendes Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~

Starte das Tool ohne Argumente, um alle BThome V2-Advertisements zu empfangen:

.. code-block:: bash

   bthome-logger

Ausgabe:

.. code-block:: text

   My-BThome-Sensor (AA:BB:CC:DD:EE:FF) RSSI: -65 dBm
     Temperature (0x02): 22.50 °C
     Humidity (0x03): 65.00 %
     Battery (0x01): 95 %

   My-Other-Sensor (11:22:33:44:55:66) RSSI: -72 dBm
     CO2 (0x12): 450 ppm
     Temperature (0x02): 23.10 °C

Filterung nach Gerätename
~~~~~~~~~~~~~~~~~~~~~~~~~~

Filtere nach einem spezifischen Gerätenamen:

.. code-block:: bash

   bthome-logger -f "My-BThome-Sensor"

Nur Advertisements von "My-BThome-Sensor" werden angezeigt.

Kommandozeilenoptionen
----------------------

.. option:: -f NAME, --filter NAME

   Filtert nach Gerätenamen. Zeigt nur Advertisements von Geräten an,
   deren Name ``NAME`` enthält.

   **Beispiel:**

   .. code-block:: bash

      bthome-logger -f "Sensor"

.. option:: --version

   Zeigt die Version des Tools an.

   **Beispiel:**

   .. code-block:: bash

      bthome-logger --version

.. option:: -h, --help

   Zeigt die Hilfe an.

   **Beispiel:**

   .. code-block:: bash

      bthome-logger --help

Ausgabeformat
-------------

Das Tool zeigt für jedes empfangene Advertisement folgende Informationen:

1. **Gerätenamen** - Der Name des BLE-Geräts
2. **MAC-Adresse** - Die Bluetooth-MAC-Adresse
3. **RSSI** - Signalstärke in dBm
4. **Sensor-Daten** - Dekodierte Messwerte mit:

   * Sensorname
   * Object ID (hexadezimal)
   * Wert mit Einheit

Beispielausgabe:

.. code-block:: text

   ESP32-Temp-Sensor (AA:BB:CC:DD:EE:FF) RSSI: -65 dBm
     Temperature (0x02): 22.50 °C
     Humidity (0x03): 65.00 %
     Pressure (0x04): 1013.25 hPa
     Battery (0x01): 95 %
     Motion (0x21): True

Unterstützte Sensortypen
-------------------------

Das Tool kann alle BThome V2 Object IDs dekodieren:

Messwertsensoren
~~~~~~~~~~~~~~~~

* **Temperature** (0x02) - Temperatur in °C
* **Humidity** (0x03) - Luftfeuchtigkeit in %
* **Pressure** (0x04) - Luftdruck in hPa
* **Illuminance** (0x05) - Beleuchtungsstärke in lux
* **CO2** (0x12) - CO2-Konzentration in ppm
* **Battery** (0x01) - Batteriestand in %
* **TVOC** (0x13) - TVOC in µg/m³
* **PM2.5** (0x0D) - Feinstaub PM2.5 in µg/m³
* **PM10** (0x0E) - Feinstaub PM10 in µg/m³
* Und viele mehr...

Binärsensoren
~~~~~~~~~~~~~

* **Motion** (0x21) - Bewegung (True/False)
* **Door** (0x1A) - Türstatus (True/False)
* **Window** (0x2F) - Fensterstatus (True/False)
* **Smoke** (0x2B) - Rauchmelder (True/False)
* Und viele mehr...

Events
~~~~~~

* **Button** (0x3A) - Button-Events (0x01-0x04)
* **Dimmer** (0x3C) - Dimmer-Events

Unbekannte Object IDs werden als "Unbekannt (0xXX)" angezeigt.

Praktische Anwendungsfälle
---------------------------

Entwicklung und Testing
~~~~~~~~~~~~~~~~~~~~~~~

Während der Entwicklung eines BThome V2-Sensors:

.. code-block:: bash

   # Terminal 1: Upload und Monitor
   pio run --target upload
   pio device monitor

   # Terminal 2: BLE-Monitoring
   bthome-logger -f "My-Sensor"

So kannst du gleichzeitig die serielle Ausgabe und die BLE-Advertisements
überwachen.

Debugging von Sensordaten
~~~~~~~~~~~~~~~~~~~~~~~~~~

Überprüfe, ob die richtigen Werte übertragen werden:

.. code-block:: bash

   bthome-logger -f "Test"

Vergleiche die angezeigten Werte mit den erwarteten Werten aus deinem Code.

Signal-Qualität testen
~~~~~~~~~~~~~~~~~~~~~~~

Teste die BLE-Reichweite durch Beobachtung des RSSI-Werts:

.. code-block:: bash

   bthome-logger -f "My-Sensor"

* **RSSI > -60 dBm**: Ausgezeichnet
* **RSSI -60 bis -70 dBm**: Gut
* **RSSI -70 bis -80 dBm**: Mittel
* **RSSI < -80 dBm**: Schwach

Home Assistant Integration testen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bevor du das Gerät in Home Assistant einbindest, überprüfe mit bthome-logger,
ob alle Sensoren korrekt übertragen werden.

Technische Details
------------------

BLE-Scanner
~~~~~~~~~~~

Das Tool verwendet die ``bleak``-Library für plattformübergreifendes
BLE-Scanning (Linux, macOS, Windows).

BThome V2 Dekodierung
~~~~~~~~~~~~~~~~~~~~~

Das Tool dekodiert die Service Data des BThome V2 Service UUID (0xFCD2).
Die Dekodierung erfolgt gemäß der `BThome V2 Spezifikation <https://bthome.io/>`_.

System-Anforderungen
--------------------

* Python 3.8 oder höher
* Bluetooth LE-fähiger Adapter
* Betriebssystem: Linux, macOS oder Windows

Bekannte Limitierungen
----------------------

* **Verschlüsselte Advertisements** werden derzeit nicht unterstützt
* **Sehr kurze Advertisement-Intervalle** (<100ms) können zu verpassten Paketen führen
* **Multiple Advertisements** vom gleichen Gerät werden einzeln angezeigt (keine Aggregation)

Fehlerbehebung
--------------

Keine Geräte gefunden
~~~~~~~~~~~~~~~~~~~~~

**Problem:** Keine Advertisements werden angezeigt.

**Lösungen:**

1. Überprüfe, ob Bluetooth aktiviert ist
2. Stelle sicher, dass das BThome-Gerät sendet (Serial Monitor prüfen)
3. Reduziere die Distanz zwischen Computer und Gerät
4. Auf Linux: Stelle sicher, dass der Benutzer in der ``bluetooth``-Gruppe ist

Permission Denied (Linux)
~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** ``PermissionError`` beim Starten.

**Lösung:**

.. code-block:: bash

   # Benutzer zur bluetooth-Gruppe hinzufügen
   sudo usermod -a -G bluetooth $USER

   # Abmelden und neu anmelden (oder neu starten)

Falscher Gerätename
~~~~~~~~~~~~~~~~~~~

**Problem:** Filter funktioniert nicht.

**Lösung:**

* Überprüfe den Gerätenamen in deinem Code (``bthome.begin("Name")``)
* Der Filter ist case-sensitive
* Verwende Teilstrings: ``-f "Sensor"`` matched "My-Sensor" und "Sensor-1"

Version-Kompatibilität
----------------------

Das bthome-logger Tool und die BThomeV2 Library werden synchron versioniert:

.. code-block:: bash

   # Library Version
   pio pkg show the78mole/BThomeV2

   # Tool Version
   bthome-logger --version

   # Sollten identisch sein (z.B. beide 0.1.0)

Siehe auch
----------

* :doc:`usage` - Erweiterte Verwendungsbeispiele
* :doc:`../library/api` - Library API-Referenz
* :doc:`../development/workflow` - Entwicklungs-Workflow
