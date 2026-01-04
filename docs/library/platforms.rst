Plattform-Support
=================

Die BThomeV2 Library unterstützt mehrere Plattformen durch plattformspezifische
Implementierungen.

ESP32 ✅
--------

**Status:** Vollständig funktionsfähig und getestet

Die ESP32-Implementierung nutzt die ArduinoBLE Library für zuverlässige
BLE-Operationen.

Unterstützte Boards
~~~~~~~~~~~~~~~~~~~

* ESP32 (alle Varianten)
* ESP32-S2
* ESP32-S3
* ESP32-C3
* ESP32-C6

Dependencies
~~~~~~~~~~~~

* ArduinoBLE ^1.5.0 (automatisch installiert)

Besonderheiten
~~~~~~~~~~~~~~

* Stabiles BLE-Advertising
* Niedriger Stromverbrauch
* Unterstützt alle BThome V2 Features

Beispiel platformio.ini
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2

nRF52 ❌
--------

**Status:** Nicht funktionsfähig

.. warning::
   Die nRF52-Implementierung ist derzeit defekt aufgrund von Runtime-Problemen
   mit der Bluefruit-Initialisierung auf Seeed XIAO nRF52840-Boards.

Bekannte Probleme
~~~~~~~~~~~~~~~~~

* **Runtime Hang:** Code hängt bei ``Bluefruit.begin()``
* **Kompilierung:** Erfolgreich
* **Hardware:** Seeed XIAO nRF52840

Getestete Boards
~~~~~~~~~~~~~~~~

* ❌ Seeed XIAO nRF52840 - Hang bei Bluefruit.begin()
* ⚠️ Adafruit Feather nRF52840 - Nicht getestet

Dependencies
~~~~~~~~~~~~

* Adafruit nRF52 Libraries (via PlatformIO)

Hilfe benötigt
~~~~~~~~~~~~~~

Wenn du Erfahrung mit Adafruit Bluefruit auf Seeed XIAO Boards hast, schau dir
bitte die `Issues <https://github.com/the78mole/bthomev2/issues>`_ an oder
erstelle einen Pull Request.

Zukünftige Plattformen
----------------------

Potentielle zukünftige Unterstützung:

* **nRF53** - Wenn nRF52 gelöst ist
* **RP2040 mit BLE-Modul** - Möglicherweise
* **STM32 mit BLE** - Möglicherweise

Plattform-Abstraktion
----------------------

Die Library verwendet eine Basis-Klasse (``BThomeV2``) mit plattformspezifischen
Implementierungen:

.. code-block:: text

   BThomeV2                    (Basis-Klasse, BThomeV2.h)
   ├── BThomeV2_ESP32          (ESP32-Implementation)
   └── BThomeV2_nRF52          (nRF52-Implementation)

Die korrekte Implementation wird automatisch zur Compile-Zeit ausgewählt:

.. code-block:: cpp

   // In BThomeV2.h
   #if defined(ESP32)
     #include "BThomeV2_ESP32.h"
     typedef BThomeV2_ESP32 BThomeV2Device;
   #elif defined(NRF52)
     #include "BThomeV2_nRF52.h"
     typedef BThomeV2_nRF52 BThomeV2Device;
   #endif

Dadurch ist die API auf allen Plattformen identisch.

Siehe auch
----------

* :doc:`api` - Plattformunabhängige API
* :doc:`examples` - Plattformspezifische Beispiele
