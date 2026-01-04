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

**BThomeV2** is a comprehensive solution for developing BLE sensors following the
`BThome V2 <https://bthome.io/>`_ standard. The project consists of two tightly
integrated components:

1. **BThomeV2 Arduino Library** - PlatformIO/Arduino library for ESP32 and nRF52
2. **bthome-logger** - Python-based testing and monitoring tool

.. warning::
   **nRF52 Implementation Currently Broken**

   The nRF52 platform is currently non-functional due to runtime issues with
   Bluefruit initialization. ESP32 works fully.

   **Status:** ✅ ESP32 fully functional | ❌ nRF52 broken (runtime hang)

Overview
--------

The BThomeV2 library provides a unified interface for BLE advertising using the
BThome V2 format, designed for efficient transmission of sensor data over Bluetooth
Low Energy. The library abstracts platform-specific BLE implementations, making it
easy to develop BThome V2-compatible devices on different hardware platforms.

The **bthome-logger** tool complements the library perfectly by decoding received
BLE advertisements and displaying them in human-readable format. Both components are
versioned synchronously to ensure compatibility.

Main Features
-------------

Arduino Library
~~~~~~~~~~~~~~~

* ✅ BThome V2 protocol support
* ✅ Multiple sensor types (temperature, humidity, pressure, CO2, etc.)
* ✅ Binary sensor support (motion, door, window, etc.)
* ✅ Event support (button actions)
* ✅ Platform abstraction (ESP32 and nRF52)
* ✅ Easy-to-use API
* ✅ Encryption support (framework in place)
* ✅ Low-power BLE advertising

Python Testing Tool
~~~~~~~~~~~~~~~~~~~~

* ✅ BLE advertisement monitoring
* ✅ BThome V2 decoding
* ✅ Device filtering
* ✅ RSSI display
* ✅ Human-readable output
* ✅ Live monitoring

Supported Platforms
-------------------

* **ESP32** ✅ - Uses ArduinoBLE library (fully tested and functional)
* **nRF52** ❌ - Uses Adafruit Bluefruit library (currently broken - runtime hang)

Quick Start
-----------

**Library Installation:**

.. code-block:: ini

   [env:esp32]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps =
       the78mole/BThomeV2

**Testing Tool Installation:**

.. code-block:: bash

   uv tool install bthome-logger

**Simple Example:**

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

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Library Documentation

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
   :caption: Development

   development/workflow
   development/contributing
   development/release-process

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   changelog
   license

Indices and Tables
==================

* :ref:`genindex`
* :ref:`search`
