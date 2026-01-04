BThomeV2 - BLE Sensor Library & Testing Tool
=============================================

.. image:: https://badges.registry.platformio.org/packages/the78mole/library/BThomeV2.svg
   :target: https://registry.platformio.org/libraries/the78mole/BThomeV2
   :alt: PlatformIO Registry

.. image:: https://badge.fury.io/py/bthome-logger.svg
   :target: https://badge.fury.io/py/bthome-logger
   :alt: PyPI version

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. image:: https://readthedocs.org/projects/bthomev2/badge/?version=latest
   :target: https://bthomev2.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

**BThomeV2** ist eine umfassende Lösung für die Entwicklung von BLE-Sensoren nach dem
`BThome V2 <https://bthome.io/>`_ Standard. Das Projekt besteht aus zwei eng verzahnten
Komponenten:

1. **BThomeV2 Arduino Library** - PlatformIO/Arduino Library für ESP32 und nRF52
2. **bthome-logger** - Python-basiertes Testing- und Monitoring-Tool

.. warning::
   **nRF52 Implementation Currently Broken**

   Die nRF52-Plattform ist derzeit nicht funktionsfähig aufgrund von Runtime-Problemen
   mit der Bluefruit-Initialisierung. ESP32 funktioniert vollständig.

   **Status:** ✅ ESP32 voll funktionsfähig | ❌ nRF52 defekt (Runtime-Hang)

Überblick
---------

Die BThomeV2 Library bietet eine einheitliche Schnittstelle für BLE-Advertising im
BThome V2-Format, das für effiziente Übertragung von Sensordaten über Bluetooth Low
Energy konzipiert ist. Die Library abstrahiert plattformspezifische BLE-Implementierungen
und erleichtert die Entwicklung von BThome V2-kompatiblen Geräten auf verschiedenen
Hardware-Plattformen.

Das **bthome-logger** Tool ergänzt die Library perfekt, indem es die empfangenen
BLE-Advertisements dekodiert und in menschenlesbarer Form anzeigt. Beide Komponenten
werden synchron versioniert, um Kompatibilität zu gewährleisten.

Hauptmerkmale
-------------

Arduino Library
~~~~~~~~~~~~~~~

* ✅ BThome V2 Protokoll-Unterstützung
* ✅ Mehrere Sensortypen (Temperatur, Luftfeuchtigkeit, Druck, CO2, etc.)
* ✅ Binärsensor-Unterstützung (Bewegung, Tür, Fenster, etc.)
* ✅ Event-Unterstützung (Button-Aktionen)
* ✅ Plattform-Abstraktion (ESP32 und nRF52)
* ✅ Einfach zu verwendende API
* ✅ Verschlüsselungs-Unterstützung (Framework vorhanden)
* ✅ Stromsparendes BLE-Advertising

Python Testing Tool
~~~~~~~~~~~~~~~~~~~~

* ✅ BLE-Advertisement Monitoring
* ✅ BThome V2 Dekodierung
* ✅ Gerätefilterung
* ✅ RSSI-Anzeige
* ✅ Menschenlesbare Ausgabe
* ✅ Live-Monitoring

Unterstützte Plattformen
------------------------

* **ESP32** ✅ - Nutzt ArduinoBLE Library (vollständig getestet und funktionsfähig)
* **nRF52** ❌ - Nutzt Adafruit Bluefruit Library (derzeit defekt - Runtime-Hang)

Quick Start
-----------

**Installation der Library:**

.. code-block:: ini

   [env:esp32]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2

**Installation des Testing Tools:**

.. code-block:: bash

   uv tool install bthome-logger

**Einfaches Beispiel:**

.. code-block:: cpp

   #include <Arduino.h>
   #include <BThomeV2.h>

   BThomeV2Device bthome;

   void setup() {
     bthome.begin("My-BThome-Device");
     bthome.addTemperature(22.5);
     bthome.addHumidity(65.0);
     bthome.startAdvertising();
   }

   void loop() {
     delay(60000);
     bthome.clearMeasurements();
     bthome.addTemperature(23.0);
     bthome.updateAdvertising();
   }

**Testing:**

.. code-block:: bash

   bthome-logger -f "My-BThome-Device"

Dokumentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Erste Schritte

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Library Dokumentation

   library/api
   library/sensors
   library/examples
   library/platforms

.. toctree::
   :maxdepth: 2
   :caption: Testing Tool

   tools/bthome-logger
   tools/usage

.. toctree::
   :maxdepth: 2
   :caption: Entwicklung

   development/workflow
   development/contributing
   development/release-process

.. toctree::
   :maxdepth: 1
   :caption: Zusätzliche Informationen

   changelog
   license

Indices und Tabellen
====================

* :ref:`genindex`
* :ref:`search`
