Installation
============

Die BThomeV2-Lösung besteht aus zwei Komponenten, die je nach Anwendungsfall
installiert werden können.

Arduino/PlatformIO Library
---------------------------

PlatformIO (Empfohlen)
~~~~~~~~~~~~~~~~~~~~~~

Füge die Library zu deiner ``platformio.ini`` hinzu:

.. code-block:: ini

   [env:esp32]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2

Für spezifische Versionen:

.. code-block:: ini

   lib_deps =
       the78mole/BThomeV2@^0.1.0

Arduino IDE
~~~~~~~~~~~

1. Lade die Library von der `GitHub Releases Seite <https://github.com/the78mole/bthomev2/releases>`_ herunter
2. In Arduino IDE: **Sketch** → **Include Library** → **Add .ZIP Library**
3. Wähle die heruntergeladene ZIP-Datei aus

Arduino Library Manager
~~~~~~~~~~~~~~~~~~~~~~~

Die Library ist auch über den Arduino Library Manager verfügbar:

1. Öffne Arduino IDE
2. Gehe zu **Tools** → **Manage Libraries**
3. Suche nach "BThomeV2"
4. Klicke auf **Install**

Dependencies
~~~~~~~~~~~~

Die BThomeV2 Library hat folgende Abhängigkeiten, die automatisch installiert werden:

**ESP32:**

* ArduinoBLE (^1.5.0)

**nRF52:**

* Adafruit nRF52 Libraries (über PlatformIO)

Python Testing Tool (bthome-logger)
------------------------------------

uv (Empfohlen)
~~~~~~~~~~~~~~

Die Installation mit `uv <https://docs.astral.sh/uv/>`_ ist der empfohlene Weg:

.. code-block:: bash

   uv tool install bthome-logger

Das Tool ist dann global verfügbar:

.. code-block:: bash

   bthome-logger

pip
~~~

Alternativ kann die Installation mit pip erfolgen:

.. code-block:: bash

   pip install bthome-logger

pipx
~~~~

Für isolierte Installation:

.. code-block:: bash

   pipx install bthome-logger

Von GitHub
~~~~~~~~~~

Für Entwicklungsversionen:

.. code-block:: bash

   git clone https://github.com/the78mole/bthomev2.git
   cd bthomev2/tools
   uv tool install .

System-Anforderungen
--------------------

Hardware
~~~~~~~~

**Für Library-Entwicklung:**

* ESP32-basiertes Board (ESP32, ESP32-S3, ESP32-C3, etc.)
* nRF52-basiertes Board (Adafruit Feather nRF52840, Seeed XIAO nRF52840)

  .. warning::
     nRF52 ist derzeit nicht funktionsfähig!

**Für Testing mit bthome-logger:**

* Bluetooth LE-fähiger Computer (integriert oder USB-Adapter)
* Linux, macOS oder Windows

Software
~~~~~~~~

**Library-Entwicklung:**

* PlatformIO Core oder Arduino IDE
* ESP32 Board Support (via Arduino Board Manager oder PlatformIO)
* nRF52 Board Support (via Adafruit Board Manager oder PlatformIO)

**Testing Tool:**

* Python 3.8 oder höher
* Bluetooth-Treiber des Betriebssystems

Versionskompatibilität
----------------------

Die Library und das Testing Tool werden synchron versioniert. Es wird empfohlen,
passende Versionen zu verwenden:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Version
     - Library (PlatformIO)
     - Tool (PyPI)
   * - 0.1.x
     - ``the78mole/BThomeV2@^0.1.0``
     - ``bthome-logger==0.1.*``
   * - 0.0.x (dev)
     - Git Repository
     - Git Repository

Verifizierung der Installation
-------------------------------

Arduino Library
~~~~~~~~~~~~~~~

Erstelle ein neues Projekt und teste den Import:

.. code-block:: cpp

   #include <BThomeV2.h>

   BThomeV2Device bthome;

   void setup() {
     Serial.begin(115200);
     if (bthome.begin("Test-Device")) {
       Serial.println("BThomeV2 initialized successfully!");
     }
   }

   void loop() {}

Python Tool
~~~~~~~~~~~

Überprüfe die Installation:

.. code-block:: bash

   bthome-logger --version

Starte einen Test-Scan:

.. code-block:: bash

   bthome-logger

Nächste Schritte
----------------

Nach der Installation:

1. Lies den :doc:`quickstart` Guide für ein erstes Beispiel
2. Erkunde die :doc:`library/examples` für fortgeschrittene Anwendungsfälle
3. Lerne das :doc:`tools/bthome-logger` Tool kennen
4. Betrachte den :doc:`development/workflow` für Entwicklungsbeiträge
