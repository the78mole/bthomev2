Tool-Verwendung
===============

Erweiterte Verwendungsbeispiele für das bthome-logger Tool.

Live-Monitoring
---------------

Kontinuierliches Monitoring aller BThome V2-Geräte:

.. code-block:: bash

   bthome-logger

Die Ausgabe aktualisiert sich live bei jedem neuen Advertisement.

Gefiltertes Monitoring
-----------------------

Nur bestimmte Geräte überwachen:

.. code-block:: bash

   # Nach Präfix filtern
   bthome-logger -f "ESP32"

   # Nach vollständigem Namen
   bthome-logger -f "My-Exact-Sensor-Name"

Multi-Device Setup
------------------

Bei mehreren Geräten kannst du mehrere Terminal-Fenster verwenden:

.. code-block:: bash

   # Terminal 1: Sensor 1
   bthome-logger -f "Sensor-1"

   # Terminal 2: Sensor 2
   bthome-logger -f "Sensor-2"

   # Terminal 3: Alle Sensoren
   bthome-logger

Siehe auch
----------

* :doc:`bthome-logger` - Tool-Dokumentation
* :doc:`../quickstart` - Quick Start Guide
