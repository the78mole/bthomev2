API Referenz
=============

Die BThomeV2 Library bietet eine einfache und einheitliche API für das Erstellen
von BThome V2-kompatiblen BLE-Sensoren.

BThomeV2Device Klasse
----------------------

Die zentrale Klasse für die Arbeit mit BThome V2-Sensoren.

Initialisierung
~~~~~~~~~~~~~~~

.. cpp:function:: bool begin(const char* deviceName)

   Initialisiert den BLE-Stack mit einem Gerätenamen.

   :param deviceName: Name des BLE-Geräts (max. 29 Zeichen)
   :return: ``true`` bei Erfolg, ``false`` bei Fehler
   :rtype: bool

   **Beispiel:**

   .. code-block:: cpp

      BThomeV2Device bthome;
      if (bthome.begin("My-Sensor")) {
        Serial.println("BLE initialized");
      }

.. cpp:function:: void end()

   Stoppt BLE-Advertising und deinitialisiert den Stack.

   **Beispiel:**

   .. code-block:: cpp

      bthome.end();

Advertising-Kontrolle
~~~~~~~~~~~~~~~~~~~~~~

.. cpp:function:: bool startAdvertising()

   Startet BLE-Advertising mit den aktuellen Messwerten.

   :return: ``true`` bei Erfolg, ``false`` bei Fehler
   :rtype: bool

   **Beispiel:**

   .. code-block:: cpp

      bthome.addTemperature(22.5);
      bthome.startAdvertising();

.. cpp:function:: void stopAdvertising()

   Stoppt BLE-Advertising.

   **Beispiel:**

   .. code-block:: cpp

      bthome.stopAdvertising();

.. cpp:function:: bool updateAdvertising()

   Aktualisiert die Advertising-Daten mit neuen Messwerten.
   Stoppt und startet Advertising automatisch.

   :return: ``true`` bei Erfolg, ``false`` bei Fehler
   :rtype: bool

   **Beispiel:**

   .. code-block:: cpp

      bthome.clearMeasurements();
      bthome.addTemperature(23.0);
      bthome.updateAdvertising();

Messwerte verwalten
~~~~~~~~~~~~~~~~~~~

.. cpp:function:: void clearMeasurements()

   Löscht alle Messwerte vor dem Hinzufügen neuer Werte.

   **Beispiel:**

   .. code-block:: cpp

      bthome.clearMeasurements();
      bthome.addTemperature(22.5);

Sensoren hinzufügen
~~~~~~~~~~~~~~~~~~~

Temperatur
^^^^^^^^^^

.. cpp:function:: void addTemperature(float temperature)

   Fügt einen Temperaturwert hinzu.

   :param temperature: Temperatur in °C (Auflösung: 0.01°C)
   :type temperature: float

   **Beispiel:**

   .. code-block:: cpp

      bthome.addTemperature(22.5);  // 22.5°C

Luftfeuchtigkeit
^^^^^^^^^^^^^^^^

.. cpp:function:: void addHumidity(float humidity)

   Fügt einen Luftfeuchtigkeitswert hinzu.

   :param humidity: Luftfeuchtigkeit in % (Auflösung: 0.01%, Bereich: 0-100)
   :type humidity: float

   **Beispiel:**

   .. code-block:: cpp

      bthome.addHumidity(65.0);  // 65%

Batterie
^^^^^^^^

.. cpp:function:: void addBattery(uint8_t battery)

   Fügt einen Batteriestand hinzu.

   :param battery: Batteriestand in % (Bereich: 0-100)
   :type battery: uint8_t

   **Beispiel:**

   .. code-block:: cpp

      bthome.addBattery(95);  // 95%

Luftdruck
^^^^^^^^^

.. cpp:function:: void addPressure(float pressure)

   Fügt einen Luftdruckwert hinzu.

   :param pressure: Luftdruck in hPa (Auflösung: 0.01 hPa)
   :type pressure: float

   **Beispiel:**

   .. code-block:: cpp

      bthome.addPressure(1013.25);  // 1013.25 hPa

Beleuchtungsstärke
^^^^^^^^^^^^^^^^^^

.. cpp:function:: void addIlluminance(float illuminance)

   Fügt einen Beleuchtungsstärkewert hinzu.

   :param illuminance: Beleuchtungsstärke in lux (Auflösung: 0.01 lux)
   :type illuminance: float

   **Beispiel:**

   .. code-block:: cpp

      bthome.addIlluminance(500.0);  // 500 lux

CO2
^^^

.. cpp:function:: void addCO2(uint16_t co2)

   Fügt einen CO2-Wert hinzu.

   :param co2: CO2-Konzentration in ppm
   :type co2: uint16_t

   **Beispiel:**

   .. code-block:: cpp

      bthome.addCO2(450);  // 450 ppm

Binärsensoren
^^^^^^^^^^^^^

.. cpp:function:: void addBinarySensor(BThomeObjectID objectId, bool state)

   Fügt einen Binärsensor-Zustand hinzu.

   :param objectId: Object ID des Binärsensors (z.B. ``MOTION``, ``DOOR``, ``WINDOW``)
   :type objectId: BThomeObjectID
   :param state: Zustand (``true`` = aktiv/offen, ``false`` = inaktiv/geschlossen)
   :type state: bool

   **Beispiele:**

   .. code-block:: cpp

      bthome.addBinarySensor(MOTION, true);   // Bewegung erkannt
      bthome.addBinarySensor(DOOR, false);    // Tür geschlossen
      bthome.addBinarySensor(WINDOW, true);   // Fenster offen

   **Verfügbare Binärsensor-IDs:**

   * ``BATTERY_LOW`` - Batterie schwach
   * ``BATTERY_CHARGING`` - Batterie lädt
   * ``CO`` - Kohlenmonoxid
   * ``COLD`` - Kälte
   * ``CONNECTIVITY`` - Verbindung
   * ``DOOR`` - Tür
   * ``GARAGE_DOOR`` - Garagentor
   * ``GAS`` - Gas
   * ``HEAT`` - Hitze
   * ``LIGHT`` - Licht
   * ``LOCK`` - Schloss
   * ``MOISTURE_BINARY`` - Feuchtigkeit
   * ``MOTION`` - Bewegung
   * ``MOVING`` - Bewegung aktiv
   * ``OCCUPANCY`` - Belegung
   * ``OPENING`` - Öffnung
   * ``PLUG`` - Stecker
   * ``POWER_BINARY`` - Strom
   * ``PRESENCE`` - Anwesenheit
   * ``PROBLEM`` - Problem
   * ``RUNNING`` - Laufend
   * ``SAFETY`` - Sicherheit
   * ``SMOKE`` - Rauch
   * ``SOUND`` - Ton
   * ``TAMPER`` - Manipulation
   * ``VIBRATION`` - Vibration
   * ``WINDOW`` - Fenster

Button Events
^^^^^^^^^^^^^

.. cpp:function:: void addButtonEvent(uint8_t event)

   Fügt ein Button-Event hinzu.

   :param event: Event-Code
   :type event: uint8_t

   **Event-Codes:**

   * ``0x01`` - Einzelner Tastendruck
   * ``0x02`` - Doppelklick
   * ``0x03`` - Dreifachklick
   * ``0x04`` - Langer Druck

   **Beispiele:**

   .. code-block:: cpp

      bthome.addButtonEvent(0x01);  // Einzelner Tastendruck
      bthome.addButtonEvent(0x02);  // Doppelklick
      bthome.addButtonEvent(0x04);  // Langer Druck

Erweiterte Funktionen
~~~~~~~~~~~~~~~~~~~~~

.. cpp:function:: void addMeasurement(BThomeObjectID objectId, const std::vector<uint8_t>& data)

   Fügt einen benutzerdefinierten Messwert mit rohen Datenbytes hinzu.

   :param objectId: BThome Object ID
   :type objectId: BThomeObjectID
   :param data: Rohe Datenbytes
   :type data: const std::vector<uint8_t>&

   **Beispiel:**

   .. code-block:: cpp

      std::vector<uint8_t> customData = {0x12, 0x34};
      bthome.addMeasurement(CUSTOM_ID, customData);

BThomeObjectID Enum
-------------------

Alle unterstützten BThome V2 Object IDs:

.. code-block:: cpp

   enum BThomeObjectID {
       PACKET_ID = 0x00,
       BATTERY = 0x01,
       TEMPERATURE = 0x02,
       HUMIDITY = 0x03,
       PRESSURE = 0x04,
       ILLUMINANCE = 0x05,
       MASS_KG = 0x06,
       MASS_LB = 0x07,
       DEW_POINT = 0x08,
       COUNT = 0x09,
       ENERGY = 0x0A,
       POWER = 0x0B,
       VOLTAGE = 0x0C,
       PM2_5 = 0x0D,
       PM10 = 0x0E,
       CO2 = 0x12,
       TVOC = 0x13,
       MOISTURE = 0x14,
       // Binärsensoren (0x15 - 0x2D)
       BATTERY_LOW = 0x15,
       BATTERY_CHARGING = 0x16,
       // ... (siehe vollständige Liste in BThomeV2.h)
       BUTTON = 0x3A,
       DIMMER = 0x3C
   };

Plattformspezifische Details
-----------------------------

Die API ist auf beiden Plattformen identisch. Die plattformspezifischen
Implementierungen werden automatisch ausgewählt:

* **ESP32**: Nutzt ``BThomeV2_ESP32.cpp`` mit ArduinoBLE
* **nRF52**: Nutzt ``BThomeV2_nRF52.cpp`` mit Adafruit Bluefruit

.. note::
   nRF52 ist derzeit nicht funktionsfähig aufgrund von Problemen mit
   der Bluefruit-Bibliothek.

Thread-Sicherheit
-----------------

Die Library ist **nicht** thread-safe. Alle Aufrufe sollten aus dem gleichen
Thread erfolgen (typischerweise der Arduino ``loop()``).

Speicherverwaltung
------------------

Die Library verwendet ``std::vector`` für die Verwaltung von Messwerten.
Jeder Aufruf von ``clearMeasurements()`` gibt den Speicher frei.

**Empfehlung:** Rufe ``clearMeasurements()`` vor dem Hinzufügen neuer Werte auf.

Siehe auch
----------

* :doc:`sensors` - Alle unterstützten Sensortypen
* :doc:`examples` - Vollständige Beispiele
* :doc:`platforms` - Plattformspezifische Informationen
