---
name: nrf52840-ble-bthomev2
description: "BLE advertising with BThomeV2 library on nRF52840, SoftDevice S140 specifics, Adafruit Bluefruit52 BLE stack. Use when: BThomeV2 advertising on nRF52840, SoftDevice memory layout, GPIO restrictions with SoftDevice, startAdvertising / begin() calls, verifying BLE output with bthome-logger, BLE advertising packet format."
argument-hint: "Optional: specific topic (e.g. 'SoftDevice GPIO', 'advertising', 'bthome-logger output')"
---

# BLE + BThomeV2 auf nRF52840 (SoftDevice S140)

## Stack-Architektur

```text
┌─────────────────────────────┐  0x100000
│   Bootloader Settings       │  0xFF000  (4 KB)
├─────────────────────────────┤  0xF4000
│   Adafruit DFU Bootloader   │  0xF4000  (~40 KB)
├─────────────────────────────┤  0x26000
│   App (Arduino / BThomeV2)  │  0x26000  (variable)
├─────────────────────────────┤  0x01000
│   SoftDevice S140 v6.1.1    │  0x01000  (~148 KB)
├─────────────────────────────┤  0x00000
│   MBR (Nordic Master Boot)  │  0x00000  (4 KB)
└─────────────────────────────┘
```

Das SoftDevice läuft **parallel** zur App und übernimmt die gesamte
BLE-HW-Steuerung (Radio, Timer, CLOCK, RTC0, RTC1, ...).
Die App kommuniziert ausschließlich über SVC-Calls (SoftDevice API).

## SoftDevice-Eigenarten (wichtig!)

### Gesperrte Peripherie

Das SoftDevice reserviert exklusiv für sich:

- `RADIO`, `TIMER0`, `RTC0`, `RTC1`, `CCM`, `AAR`, `ECB`, `TEMP`
- `CLOCK` (indirekt – nur über SD_CLOCK_HFCLK_REQUEST)

**App darf diese NICHT direkt ansprechen** – sonst Hard Fault oder Deadlock.

### GPIO mit SoftDevice

`digitalWrite()` / `pinMode()` via Adafruit-BSP funktioniert normal
(nrf5 GPIO ist nicht SoftDevice-reserviert).
Direkte Registerzugriffe auf `P0.OUT` / `P0.DIR` sind ebenfalls erlaubt.

### Interrupt-Prioritäten

SoftDevice belegt Prioritäten 0–1 (höchste).
App-Interrupts müssen Priorität ≥ 4 haben.
FreeRTOS und Adafruit-BSP beachten das automatisch.

### delay() unter SoftDevice + FreeRTOS

`delay()` im Adafruit-BSP ruft `vTaskDelay()` → FreeRTOS-Scheduler muss
laufen.
Im frühen Boot (vor `vTaskStartScheduler`) blockiert `delay()` potentiell
ewig.
→ Für Early-Boot-Blinks immer **Busy-Wait** verwenden
(siehe nrf52840-platformio SKILL).

## BThomeV2-Library auf nRF52840

### Initialisierung

```cpp
#include <BThomeV2.h>

BThomeV2 bthome;  // globales Objekt

void setup() {
    // BLE-Stack starten + Advertising konfigurieren
    if (!bthome.begin("MAKE-nRF52")) {
        // Fehler – BLE-Stack konnte nicht initialisiert werden
    }

    // Sensor-Daten hinzufügen
    bthome.addTemperature(21.5f);
    bthome.addHumidity(65.0f);
    bthome.addBattery(100);

    // Advertising starten
    bthome.startAdvertising();
}
```

`bthome.begin()` initialisiert intern Bluefruit (SoftDevice enablen, GAP/GATT einrichten).
Das ist ein blocking-Call und kann mehrere Sekunden dauern.

### Sensor-Daten aktualisieren (loop)

```cpp
void loop() {
    bthome.resetMeasurements();
    bthome.addTemperature(temperature);
    bthome.addHumidity(humidity);
    bthome.addBattery(battery);
    bthome.startAdvertising();  // aktualisiert den Advertising-Payload
    delay(5000);
}
```

## BLE Advertising Packet Format (BThomeV2)

BThomeV2 sendet als **Non-connectable Undirected Advertising** (ADV_NONCONN_IND).
Der Payload steckt im Service-Data-AD-Element (UUID 0xFCD2).

Beispiel-Payload (hex): `40 01 5d 02 3b 08 03 37 1a`

```text
40        = BThome Device Info Byte
            Bit 6 = 1 → v2, Bit 0 = 0 → unverschlüsselt
01 5d     = Object 0x01 (Battery) = 0x5d = 93 %
02 3b 08  = Object 0x02 (Temperature) = 0x083b = 2107 → 21.07 °C
03 37 1a  = Object 0x03 (Humidity) = 0x1a37 = 6711 → 67.11 %
```

Alle Werte sind **Little-Endian**.
Skalierung je nach Object-ID (Temperatur ÷ 100, Humidity ÷ 100).

## Verifikation mit bthome-logger

```bash
# Via installiertem Tool (empfohlen)
bthome-logger --filter "MAKE"

# Via uv run (lokal aus tools/)
cd tools
uv run python bthome_logger.py --filter "MAKE"
```

Erwartete Ausgabe:

```text
[22:03:46.909] 📱 MAKE-nRF52 (CC:8F:EB:B8:55:B8)
  RSSI: -40 dBm
  Raw: 40 01 5d 02 3b 08 03 37 1a
  BThome: v2 (unencrypted)
  Values:
    • Battery (0x01): 93.00 % [5d]
    • Temperature (0x02): 21.07 °C [3b 08]
    • Humidity (0x03): 67.11 % [37 1a]
```

## Boot-Sequenz (Adafruit BSP + SoftDevice)

```text
Reset
 └→ MBR (0x0000)
     └→ SoftDevice Init (0x1000)
         └→ App Reset_Handler (0x26000+)
             └→ main()
                 └→ vTaskStartScheduler()
                     └→ loop_task
                         └→ setup()   ← Arduino-Code startet hier
                             └→ bthome.begin()   ← BLE-Stack aktivieren
                                 └→ startAdvertising()
```

**setup() läuft innerhalb eines FreeRTOS-Tasks** – `delay()` funktioniert,
Interrupts laufen, SoftDevice ist aktiv.

## Troubleshooting

**bthome.begin() hängt / kehrt nie zurück:**

- SoftDevice wurde nicht korrekt geflasht → Full-Restore durchführen
  (siehe nrf52840-platformio SKILL)
- UICR.BOOTLOADERADDR zeigt auf erased Flash
  → MBR kann SoftDevice nicht initialisieren

**Keine BLE-Advertisements sichtbar (bthome-logger findet nichts):**

1. `bthome-logger --filter ""` – zeigt alle BThome-Geräte ohne Namensfilter
2. `hciconfig hci0 up` – Bluetooth-Adapter prüfen
3. Gerätename prüfen: muss den Filter-String enthalten (default: `MAKE`)
4. RSSI-Problem: Logger und DK müssen < 10m Abstand haben

**LED pulsiert (DFU-Modus) statt App zu starten:**

- `firmware_signature.bin` fehlt → `pio run -t upload` ausführen
  (schreibt Signature bei 0xFF000)
- Nie nur `loadbin firmware.bin 0x26000` – immer mit pio upload
  oder manuell Signature flashen

**App läuft aber keine LED-Aktivität:**

- CPU könnte durch J-Link `halt`-Befehl eingefroren sein →
  Play-Button im Debugger oder `JLinkExe go`
- Pulsieren = DFU (s. o.) – kein Pulsieren, keine LEDs = CPU gehaltet
