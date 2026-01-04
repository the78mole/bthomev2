Advanced Usage Examples
=======================

This page provides advanced usage examples for the bthome-logger tool beyond basic scanning.

Production Monitoring
---------------------

Long-Running Monitoring
~~~~~~~~~~~~~~~~~~~~~~~

Monitor sensors continuously:

.. code-block:: bash

   # Basic continuous monitoring
   bthome-logger -f "Production-Sensor"

   # With timestamp logging
   bthome-logger -f "Sensor" | while read line; do
     echo "$(date +%Y-%m-%d\ %H:%M:%S) $line"
   done >> sensor-log.txt

   # In screen session for remote monitoring
   screen -S bthome-monitor
   bthome-logger -f "Remote-Sensor"
   # Press Ctrl+A, D to detach
   # screen -r bthome-monitor to reattach

Automated Testing
~~~~~~~~~~~~~~~~~

Use in test scripts:

.. code-block:: bash

   #!/bin/bash
   # test-sensor.sh - Automated sensor verification

   SENSOR_NAME="Test-Sensor"
   TIMEOUT=60

   echo "Testing sensor: $SENSOR_NAME"

   # Check if sensor advertises within timeout
   timeout $TIMEOUT bthome-logger -f "$SENSOR_NAME" | grep -q "Temperature"

   if [ $? -eq 0 ]; then
     echo "✓ Sensor is advertising"
     exit 0
   else
     echo "✗ Sensor not found"
     exit 1
   fi

Multi-Device Scenarios
----------------------

Home Monitoring Setup
~~~~~~~~~~~~~~~~~~~~~

Monitor multiple rooms:

.. code-block:: bash

   # Terminal 1: Living room
   bthome-logger -f "Living-Room"

   # Terminal 2: Bedroom
   bthome-logger -f "Bedroom"

   # Terminal 3: Kitchen
   bthome-logger -f "Kitchen"

   # Or use tmux for split screen:
   tmux new-session \; \
     split-window -h \; \
     split-window -v \; \
     send-keys -t 0 'bthome-logger -f "Living"' C-m \; \
     send-keys -t 1 'bthome-logger -f "Bedroom"' C-m \; \
     send-keys -t 2 'bthome-logger -f "Kitchen"' C-m

Filter by Name Pattern
~~~~~~~~~~~~~~~~~~~~~~

Monitor related devices:

.. code-block:: bash

   # All climate sensors
   bthome-logger -f "Climate"

   # All sensors with common prefix
   bthome-logger -f "Home-"

   # Specific location
   bthome-logger -f "Basement"

Data Analysis
-------------

Log and Parse Data
~~~~~~~~~~~~~~~~~~

Capture data for analysis:

.. code-block:: bash

   # Log to file
   bthome-logger -f "Climate" > climate-data.log

   # Parse temperature values
   grep "Temperature" climate-data.log | \
     sed 's/.*Temperature: \([0-9.]*\).*/\1/' > temps.txt

   # Calculate average
   awk '{sum+=$1} END {print "Average:", sum/NR, "°C"}' temps.txt

Extract Specific Measurements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Extract humidity values
   bthome-logger -f "Sensor" | \
     grep "Humidity" | \
     sed 's/.*Humidity: \([0-9.]*\).*/\1/'

   # Extract RSSI values for range testing
   bthome-logger -f "Sensor" | \
     grep "RSSI" | \
     sed 's/.*RSSI: \(-[0-9]*\).*/\1/'

Time-Series Data Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   # collect-data.py - Collect time-series sensor data

   import subprocess
   import re
   import time
   from datetime import datetime

   sensor_name = "Climate-Sensor"
   data_file = "sensor-data.csv"

   # Write CSV header
   with open(data_file, 'w') as f:
       f.write("timestamp,temperature,humidity,battery\n")

   # Start logger process
   proc = subprocess.Popen(
       ['bthome-logger', '-f', sensor_name],
       stdout=subprocess.PIPE,
       stderr=subprocess.PIPE,
       text=True
   )

   temp = humidity = battery = None

   try:
       for line in proc.stdout:
           # Parse temperature
           match = re.search(r'Temperature: ([\d.]+)', line)
           if match:
               temp = match.group(1)

           # Parse humidity
           match = re.search(r'Humidity: ([\d.]+)', line)
           if match:
               humidity = match.group(1)

           # Parse battery
           match = re.search(r'Battery: (\d+)', line)
           if match:
               battery = match.group(1)

               # All values collected, write to CSV
               if temp and humidity:
                   timestamp = datetime.now().isoformat()
                   with open(data_file, 'a') as f:
                       f.write(f"{timestamp},{temp},{humidity},{battery}\n")
                   print(f"Logged: {timestamp}, {temp}°C, {humidity}%, {battery}%")

                   # Reset for next reading
                   temp = humidity = battery = None

   except KeyboardInterrupt:
       print("\nStopped data collection")
   finally:
       proc.terminate()

Development Workflows
---------------------

Rapid Prototyping
~~~~~~~~~~~~~~~~~

Test changes quickly:

.. code-block:: bash

   # Terminal 1: Edit and compile
   vim src/main.cpp
   pio run --target upload

   # Terminal 2: Watch output
   bthome-logger -f "Dev-Sensor"

   # See changes immediately after upload

Debugging Advertisement Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Step 1: Check if device advertises at all
   bthome-logger -v | grep "Your-Device"

   # Step 2: Check BThome company ID
   bthome-logger -v -f "Your-Device" | grep "0xFCD2"

   # Step 3: Verify sensor data
   bthome-logger -f "Your-Device"

Range and Signal Testing
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # range-test.sh - Test signal strength at distances

   SENSOR="Test-Sensor"

   echo "Place sensor at different distances and press Enter"
   echo "Distance (m), RSSI (dBm)"

   for distance in 1 2 5 10 15 20; do
       read -p "Sensor at ${distance}m - Press Enter..."

       # Capture 5 RSSI readings
       rssi=$(timeout 30 bthome-logger -f "$SENSOR" | \
              grep "RSSI" | head -5 | \
              sed 's/.*RSSI: \(-[0-9]*\).*/\1/' | \
              awk '{sum+=$1} END {print sum/NR}')

       echo "$distance, $rssi"
   done

Integration Examples
--------------------

Home Assistant MQTT Bridge
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Forward sensor data to Home Assistant:

.. code-block:: python

   #!/usr/bin/env python3
   # bthome-mqtt-bridge.py

   import subprocess
   import re
   import json
   import paho.mqtt.client as mqtt

   # Configuration
   SENSOR_NAME = "Climate-Sensor"
   MQTT_BROKER = "localhost"
   MQTT_PORT = 1883
   MQTT_TOPIC_PREFIX = "homeassistant/sensor/bthome"

   # Connect to MQTT
   client = mqtt.Client()
   client.connect(MQTT_BROKER, MQTT_PORT)
   client.loop_start()

   # Start logger
   proc = subprocess.Popen(
       ['bthome-logger', '-f', SENSOR_NAME],
       stdout=subprocess.PIPE,
       text=True
   )

   data = {}

   try:
       for line in proc.stdout:
           # Parse values
           if "Temperature:" in line:
               match = re.search(r'Temperature: ([\d.]+)', line)
               if match:
                   data['temperature'] = float(match.group(1))

           elif "Humidity:" in line:
               match = re.search(r'Humidity: ([\d.]+)', line)
               if match:
                   data['humidity'] = float(match.group(1))

           elif "Battery:" in line:
               match = re.search(r'Battery: (\d+)', line)
               if match:
                   data['battery'] = int(match.group(1))

                   # Publish when complete reading received
                   topic = f"{MQTT_TOPIC_PREFIX}/{SENSOR_NAME}/state"
                   payload = json.dumps(data)
                   client.publish(topic, payload)
                   print(f"Published: {payload}")
                   data = {}

   except KeyboardInterrupt:
       print("\nStopping bridge")
   finally:
       proc.terminate()
       client.loop_stop()
       client.disconnect()

Prometheus Exporter
~~~~~~~~~~~~~~~~~~~

Export metrics for Prometheus:

.. code-block:: python

   #!/usr/bin/env python3
   # bthome-prometheus-exporter.py

   from prometheus_client import start_http_server, Gauge
   import subprocess
   import re
   import time

   # Metrics
   temperature = Gauge('bthome_temperature_celsius', 'Temperature in Celsius')
   humidity = Gauge('bthome_humidity_percent', 'Humidity in Percent')
   battery = Gauge('bthome_battery_percent', 'Battery level in Percent')
   rssi = Gauge('bthome_rssi_dbm', 'RSSI in dBm')

   # Start HTTP server
   start_http_server(8000)
   print("Prometheus exporter running on :8000")

   # Start logger
   proc = subprocess.Popen(
       ['bthome-logger', '-f', 'Climate'],
       stdout=subprocess.PIPE,
       text=True
   )

   try:
       for line in proc.stdout:
           # Update metrics
           match = re.search(r'Temperature: ([\d.]+)', line)
           if match:
               temperature.set(float(match.group(1)))

           match = re.search(r'Humidity: ([\d.]+)', line)
           if match:
               humidity.set(float(match.group(1)))

           match = re.search(r'Battery: (\d+)', line)
           if match:
               battery.set(int(match.group(1)))

           match = re.search(r'RSSI: (-\d+)', line)
           if match:
               rssi.set(int(match.group(1)))

   except KeyboardInterrupt:
       print("\nStopping exporter")
   finally:
       proc.terminate()

Alert System
~~~~~~~~~~~~

Send alerts based on sensor values:

.. code-block:: bash

   #!/bin/bash
   # alert-monitor.sh - Monitor and alert on thresholds

   SENSOR="Freezer-Sensor"
   MAX_TEMP="-18"  # Alert if above -18°C
   ALERT_EMAIL="admin@example.com"

   bthome-logger -f "$SENSOR" | while read line; do
       if echo "$line" | grep -q "Temperature"; then
           temp=$(echo "$line" | sed 's/.*Temperature: \([-0-9.]*\).*/\1/')

           if (( $(echo "$temp > $MAX_TEMP" | bc -l) )); then
               # Send alert
               echo "ALERT: Freezer temp $temp°C exceeds $MAX_TEMP°C" | \
                   mail -s "Freezer Temperature Alert" "$ALERT_EMAIL"

               echo "Alert sent: $temp°C > $MAX_TEMP°C"
           fi
       fi
   done

Advanced Filtering
------------------

Multiple Device Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Monitor all sensors matching pattern
   for device in "Living" "Bedroom" "Kitchen"; do
       bthome-logger -f "$device" > "${device}-log.txt" 2>&1 &
   done

   # Wait for all background jobs
   wait

Device Discovery
~~~~~~~~~~~~~~~~

Find all BThome devices:

.. code-block:: bash

   # Scan for 60 seconds and list unique devices
   timeout 60 bthome-logger -v | \
     grep "0xFCD2" | \
     sed 's/.*📱 \([^ ]*\).*/\1/' | \
     sort -u

Tips and Tricks
---------------

Keyboard Shortcuts
~~~~~~~~~~~~~~~~~~

* **Ctrl+C** - Stop scanner
* **Ctrl+Z** - Suspend (use ``fg`` to resume)
* **Ctrl+L** - Clear screen (most terminals)

Output Redirection
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Save to file
   bthome-logger -f "Sensor" > output.log

   # Append to existing file
   bthome-logger -f "Sensor" >> output.log

   # Discard output
   bthome-logger -f "Sensor" > /dev/null

   # Separate stdout and stderr
   bthome-logger -f "Sensor" > output.log 2> errors.log

Performance
~~~~~~~~~~~

.. code-block:: bash

   # Reduce CPU usage with longer scan intervals
   # (Modify source if needed)

   # Monitor resource usage
   top -p $(pgrep -f bthome-logger)

See Also
--------

* :doc:`bthome-logger` - Tool documentation
* :doc:`../library/api` - Library API
* :doc:`../development/workflow` - Development workflow
