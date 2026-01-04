bthome-logger Tool
==================

The **bthome-logger** is a Python command-line tool for testing and debugging BThome V2 devices. It scans for BLE advertisements and displays decoded sensor data in real-time.

Overview
--------

The tool helps you:

* Verify your BThome V2 sensor is advertising correctly
* Debug sensor data and advertisements
* Monitor multiple sensors simultaneously
* Check signal strength (RSSI)
* View raw advertisement data

Installation
------------

Recommended: uv
~~~~~~~~~~~~~~~

The fastest and most reliable installation method:

.. code-block:: bash

   uv tool install bthome-logger

The tool is then globally available:

.. code-block:: bash

   bthome-logger

Alternative: pipx
~~~~~~~~~~~~~~~~~

For isolated tool installation:

.. code-block:: bash

   pipx install bthome-logger

Alternative: pip
~~~~~~~~~~~~~~~~

System-wide installation:

.. code-block:: bash

   pip install bthome-logger

From Source
~~~~~~~~~~~

For development or latest changes:

.. code-block:: bash

   git clone https://github.com/the78mole/bthomev2.git
   cd bthomev2/tools
   pip install -e .

Usage
-----

Basic Usage
~~~~~~~~~~~

Start scanning with default filter:

.. code-block:: bash

   bthome-logger

This filters for devices with "MAKE" in their name (default).

Filter by Device Name
~~~~~~~~~~~~~~~~~~~~~

Show only specific devices:

.. code-block:: bash

   # Filter by partial name
   bthome-logger -f "ESP32"

   # Filter for your sensor
   bthome-logger -f "My-Sensor"

   # Filter for multiple devices (any match)
   bthome-logger -f "Living-Room"

Verbose Mode
~~~~~~~~~~~~

Show all BLE advertisements, not just BThome devices:

.. code-block:: bash

   bthome-logger -v

   # Or
   bthome-logger --verbose

Version Information
~~~~~~~~~~~~~~~~~~~

Check installed version:

.. code-block:: bash

   bthome-logger --version

Help
~~~~

Show all options:

.. code-block:: bash

   bthome-logger --help

Command-Line Options
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Option
     - Short
     - Description
   * - ``--filter <name>``
     - ``-f``
     - Filter devices by name (partial match)
   * - ``--verbose``
     - ``-v``
     - Show all BLE advertisements
   * - ``--version``
     -
     - Show version and exit
   * - ``--help``
     - ``-h``
     - Show help message and exit

Output Format
-------------

The tool displays advertisements in this format:

Header
~~~~~~

.. code-block:: text

   ======================================================================
   🔵 BThome Logger - Python Edition
   Scans for BLE devices with BThome v2 protocol
   ======================================================================

   Filter: Devices with 'ESP32' in name
   Press Ctrl+C to exit

   ✓ Scanner started...

Advertisement Display
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ----------------------------------------------------------------------
   [14:32:45.123] 📱 ESP32-Climate (E4:65:B8:12:34:56)
     RSSI: -45 dBm
     Temperature: 22.5 °C
     Humidity: 65.0 %
     Battery: 95 %

RSSI Color Coding
~~~~~~~~~~~~~~~~~

Signal strength is color-coded:

* **Green** (> -60 dBm): Excellent signal
* **Yellow** (-60 to -75 dBm): Good signal
* **Red** (< -75 dBm): Weak signal

Supported Sensor Types
----------------------

The tool automatically decodes all BThome V2 sensor types:

Environmental Sensors
~~~~~~~~~~~~~~~~~~~~~

* Temperature (°C)
* Humidity (%)
* Pressure (hPa)
* Dew Point (°C)
* Moisture (%)

Air Quality
~~~~~~~~~~~

* CO2 (ppm)
* TVOC (ppb)
* PM2.5 (µg/m³)
* PM10 (µg/m³)

Light & Power
~~~~~~~~~~~~~

* Illuminance (lux)
* Battery (%)
* Voltage (V)
* Power (W)
* Energy (kWh)

Binary Sensors
~~~~~~~~~~~~~~

All binary sensors are decoded with appropriate labels:

* Motion, Occupancy, Presence
* Door, Window, Opening
* Smoke, Gas, CO
* And many more (see :doc:`../library/sensors`)

Events
~~~~~~

* Button events (press, double press, triple press, long press)
* Dimmer events (rotate left/right)

Practical Use Cases
-------------------

Development Testing
~~~~~~~~~~~~~~~~~~~

Test your sensor during development:

.. code-block:: bash

   # Terminal 1: Monitor serial output
   pio device monitor

   # Terminal 2: Watch BLE advertisements
   bthome-logger -f "My-Sensor"

Verify Sensor Updates
~~~~~~~~~~~~~~~~~~~~~~

Check that measurements update correctly:

.. code-block:: bash

   bthome-logger -f "Climate-Sensor"

   # Watch for value changes every 60 seconds
   # Temperature: 22.5 °C → 22.7 °C → 23.0 °C

Signal Strength Testing
~~~~~~~~~~~~~~~~~~~~~~~

Test range and signal quality:

.. code-block:: bash

   bthome-logger -f "Test-Sensor"

   # Move device away and watch RSSI:
   # RSSI: -45 dBm (1m)
   # RSSI: -60 dBm (5m)
   # RSSI: -75 dBm (10m)

Multiple Sensor Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor several sensors at once:

.. code-block:: bash

   # Show all your sensors
   bthome-logger -f "Home-"

   # Will show:
   # Home-Living-Room
   # Home-Bedroom
   # Home-Kitchen

Debugging
~~~~~~~~~

Find issues with advertisements:

.. code-block:: bash

   # Use verbose mode to see raw data
   bthome-logger -v -f "Problem-Sensor"

   # Check:
   # - Is device advertising?
   # - Is BThome company ID present (0xFCD2)?
   # - Are sensor values reasonable?

Examples
--------

Example 1: Basic Temperature Sensor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ bthome-logger -f "ESP32-Basic"

Output:

.. code-block:: text

   [10:30:15] ESP32-Basic (E4:65:B8:XX:XX:XX) | RSSI: -45 dBm
     Temperature: 22.3 °C
     Humidity: 64.5 %
     Battery: 100 %

   [10:30:25] ESP32-Basic (E4:65:B8:XX:XX:XX) | RSSI: -46 dBm
     Temperature: 22.4 °C
     Humidity: 64.3 %
     Battery: 100 %

Example 2: Button Events
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ bthome-logger -f "Button"

Output:

.. code-block:: text

   [10:31:22] ESP32-Button (E4:65:B8:XX:XX:XX) | RSSI: -42 dBm
     Button: Press
     Battery: 100 %

   [10:31:30] ESP32-Button (E4:65:B8:XX:XX:XX) | RSSI: -42 dBm
     Button: Long Press
     Battery: 100 %

Example 3: Multiple Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ bthome-logger -f "Multi-Sensor"

Output:

.. code-block:: text

   [10:32:45] Multi-Sensor (E4:65:B8:XX:XX:XX) | RSSI: -48 dBm
     Temperature: 24.2 °C
     Humidity: 58.3 %
     Pressure: 1015.3 hPa
     Illuminance: 623.5 lux
     CO2: 456 ppm
     Battery: 100 %

Example 4: Verbose Mode
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ bthome-logger -v

Output shows ALL BLE advertisements:

.. code-block:: text

   [10:33:10] Random-Device (AA:BB:CC:DD:EE:FF) | RSSI: -55 dBm
     (No BThome data)

   [10:33:11] ESP32-Basic (E4:65:B8:XX:XX:XX) | RSSI: -45 dBm
     Temperature: 22.5 °C
     Battery: 100 %

   [10:33:12] iPhone (11:22:33:44:55:66) | RSSI: -60 dBm
     (No BThome data)

Troubleshooting
---------------

Tool doesn't start
~~~~~~~~~~~~~~~~~~

**Problem:** Command not found

**Solution:**

.. code-block:: bash

   # Reinstall
   uv tool install bthome-logger --force

   # Or check installation
   uv tool list

No devices found
~~~~~~~~~~~~~~~~

**Problem:** Scanner starts but no devices appear

**Check:**

1. Is Bluetooth enabled?

   .. code-block:: bash

      # Linux
      bluetoothctl power on

      # macOS
      # Check System Settings > Bluetooth

2. Is device actually advertising?

   Check serial monitor for "Advertising started!"

3. Is device in range?

   Move device closer (<5m for testing)

4. Try verbose mode:

   .. code-block:: bash

      bthome-logger -v

Wrong device name filter
~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Your device doesn't appear but others do

**Solution:**

.. code-block:: bash

   # Check exact device name in your code
   # Then use matching filter
   bthome-logger -f "Exact-Name"

Permission errors (Linux)
~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Permission denied when scanning

**Solution:**

.. code-block:: bash

   # Add user to bluetooth group
   sudo usermod -a -G bluetooth $USER

   # Restart session or reboot

Values not updating
~~~~~~~~~~~~~~~~~~~

**Problem:** Same values shown repeatedly

**Check:**

1. Device is calling ``updateAdvertising()``
2. Update interval is reasonable (30+ seconds)
3. Device hasn't crashed (check serial monitor)

Incorrect values displayed
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Values don't match expected

**Check:**

1. Units in your code match sensor documentation
2. Resolution is correct (e.g., temperature in °C not °F)
3. Data type is correct (float vs int)

Version Compatibility
---------------------

The tool and library share version numbers:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Tool Version
     - Library Version
     - Notes
   * - 0.2.x
     - 0.2.x
     - Current, fully compatible
   * - 0.1.x
     - 0.1.x
     - Initial release

**Recommendation:** Always use matching versions.

.. code-block:: bash

   # Check versions
   bthome-logger --version
   # Compare with library version in platformio.ini

System Requirements
-------------------

Operating Systems
~~~~~~~~~~~~~~~~~

* **Linux:** Ubuntu 20.04+, Debian 11+, other distributions with BlueZ
* **macOS:** 10.15+ (Catalina or newer)
* **Windows:** 10+ with Bluetooth LE support

Python
~~~~~~

* Python 3.8 or higher
* pip or uv package manager

Hardware
~~~~~~~~

* Bluetooth LE 4.0+ adapter (built-in or USB)
* For USB adapters: Must support Bluetooth LE

Dependencies
~~~~~~~~~~~~

Automatically installed:

* ``bleak`` - Bluetooth LE library
* ``colorama`` - Terminal colors (Windows)

Advanced Usage
--------------

Integration with Scripts
~~~~~~~~~~~~~~~~~~~~~~~~

Use in shell scripts:

.. code-block:: bash

   #!/bin/bash
   # Check if sensor is alive
   timeout 30 bthome-logger -f "My-Sensor" | grep -q "Temperature"
   if [ $? -eq 0 ]; then
     echo "Sensor is alive"
   else
     echo "Sensor not responding"
   fi

Continuous Monitoring
~~~~~~~~~~~~~~~~~~~~~

Run as a service or in background:

.. code-block:: bash

   # With logging
   bthome-logger -f "Production-Sensor" >> sensor.log 2>&1

   # In screen session
   screen -S bthome
   bthome-logger -f "My-Sensor"
   # Ctrl+A, D to detach

See Also
--------

* :doc:`usage` - Extended usage examples
* :doc:`../library/api` - Library API reference
* :doc:`../library/sensors` - Supported sensor types
* :doc:`../quickstart` - Getting started guide
* :doc:`../development/workflow` - Development workflow
