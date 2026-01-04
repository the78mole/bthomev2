Installation
============

The BThomeV2 solution consists of two components that can be installed depending on your use case.

Arduino/PlatformIO Library
---------------------------

PlatformIO (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~

Add the library to your ``platformio.ini``:

.. code-block:: ini

   [env:esp32]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2

For specific versions:

.. code-block:: ini

   lib_deps =
       the78mole/BThomeV2@^0.1.0

Arduino IDE
~~~~~~~~~~~

1. Download the library from the `GitHub Releases page <https://github.com/the78mole/bthomev2/releases>`_
2. In Arduino IDE: **Sketch** → **Include Library** → **Add .ZIP Library**
3. Select the downloaded ZIP file

Arduino Library Manager
~~~~~~~~~~~~~~~~~~~~~~~

The library is also available through the Arduino Library Manager:

1. Open Arduino IDE
2. Go to **Tools** → **Manage Libraries**
3. Search for "BThomeV2"
4. Click **Install**

Dependencies
~~~~~~~~~~~~

The BThomeV2 library has the following dependencies that are automatically installed:

**ESP32:**

* ArduinoBLE (^1.5.0)

**nRF52:**

* Adafruit nRF52 Libraries (via PlatformIO)

Python Testing Tool (bthome-logger)
------------------------------------

uv (Recommended)
~~~~~~~~~~~~~~~~

Installation with `uv <https://docs.astral.sh/uv/>`_ is the recommended method:

.. code-block:: bash

   uv tool install bthome-logger

The tool is then globally available:

.. code-block:: bash

   bthome-logger

pip
~~~

Alternatively, you can install with pip:

.. code-block:: bash

   pip install bthome-logger

pipx
~~~~

For isolated installation:

.. code-block:: bash

   pipx install bthome-logger

From GitHub
~~~~~~~~~~~

For development versions:

.. code-block:: bash

   git clone https://github.com/the78mole/bthomev2.git
   cd bthomev2/tools
   uv tool install .

System Requirements
-------------------

Hardware
~~~~~~~~

**For Library Development:**

* ESP32-based boards (ESP32, ESP32-S3, ESP32-C3, etc.)
* nRF52-based boards (Adafruit Feather nRF52840, Seeed XIAO nRF52840)

  .. warning::
     nRF52 is currently not functional!

**For Testing with bthome-logger:**

* Bluetooth LE capable computer (built-in or USB adapter)
* Linux, macOS or Windows

Software
~~~~~~~~

**Library Development:**

* PlatformIO Core or Arduino IDE
* ESP32 Board Support (via Arduino Board Manager or PlatformIO)
* nRF52 Board Support (via Adafruit Board Manager or PlatformIO)

**Testing Tool:**

* Python 3.8 or higher
* Operating system Bluetooth drivers

Version Compatibility
---------------------

The library and testing tool are versioned synchronously. It is recommended to use matching versions:

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

Installation Verification
-------------------------

Arduino Library
~~~~~~~~~~~~~~~

Create a new project and test the import:

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

Verify the installation:

.. code-block:: bash

   bthome-logger --version

Start a test scan:

.. code-block:: bash

   bthome-logger

Next Steps
----------

After installation:

1. Read the :doc:`quickstart` guide for a first example
2. Explore :doc:`library/examples` for advanced use cases
3. Learn about the :doc:`tools/bthome-logger` tool
4. Review the :doc:`development/workflow` for development contributions
