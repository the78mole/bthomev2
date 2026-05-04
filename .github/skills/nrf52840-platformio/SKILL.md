---
name: nrf52840-platformio
description: "Build, flash, and debug nRF52840 projects with PlatformIO and the Adafruit BSP. Use when: setting up PlatformIO for nRF52840-DK, flashing via J-Link, restoring SoftDevice and Bootloader, understanding the flash memory layout, fixing 'pulsing LED' DFU mode, using firmware_signature.bin, selective app-only flash, checking UICR.BOOTLOADERADDR."
argument-hint: "Optional: specific issue (e.g. 'flash layout', 'restore bootloader', 'upload')"
---

# nRF52840 mit PlatformIO (Adafruit BSP)

## Hardware & Software

- **Board:** nRF52840-DK (pca10056)
- **Debugger:** SEGGER J-Link OB (onboard), S/N: 1050252111
- **Platform:** `nordicnrf52` 10.9.0
- **Framework:** `arduino`
  (Adafruit Bluefruit52Lib / framework-arduinoadafruitnrf52 1.10601.0)
- **Board-ID:** `nrf52840_dk_adafruit` (Adafruit-Variante, nicht `nrf52840_dk`)
- **Serielle Ports** (Nummerierung kann je nach Enumeration variieren
  – mit `ls /dev/ttyACM*` prüfen):
  - J-Link VCOM (Serial2 UART, P0.06=TX / P0.08=RX) → aktuell `/dev/ttyACM0`
  - J-Link CDC Command-Kanal → weiterer ACM-Port (kein UART-Output)
  - App-TinyUSB-CDC = separater Port (erscheint nur wenn zweites USB-Kabel
    an J18 angesteckt)

## platformio.ini (Minimal-Konfiguration)

```ini
[env:nrf52840dk]
platform = nordicnrf52
board = nrf52840_dk_adafruit
framework = arduino
lib_extra_dirs = ../../
monitor_port = /dev/ttyACM0   ; J-Link VCOM = Serial2 UART (Nummer ggf. anpassen)
monitor_speed = 115200
upload_protocol = jlink
lib_deps = adafruit/Adafruit nRFCrypto@^0.1.2
build_flags =
    -DBOARD_NRF52DK
    -I.pio/libdeps/nrf52840dk/Adafruit\ nRFCrypto/src
debug_svd_path = /home/daniel/.platformio/platforms/nordicnrf52/misc/svd/nrf52840.svd
debug_tool = jlink
build_type = debug
debug_build_flags = -O0 -ggdb3
debug_server_parameters = -rtos GDBServer/RTOSPlugin_FreeRTOS
```

**Wichtig:** Immer `nrf52840_dk_adafruit` verwenden, nicht `nrf52840_dk`
(Nordic BSP)!
Der Nordic-BSP hat ein falsches Pin-Mapping: `LED_BUILTIN` → Arduino-Pin 6
→ P0.17 (falsch, LEDs sind P0.13–P0.16).

## Flash-Speicherlayout (nRF52840, Adafruit BSP)

| Region              | Adresse      | Inhalt                          |
|---------------------|--------------|---------------------------------|
| MBR                 | `0x00000000` | Nordic MBR (4 KB)               |
| SoftDevice S140     | `0x00001000` | S140 BLE-Stack (~152 KB)        |
| App                 | `0x00026000` | Adafruit Arduino App            |
| Bootloader          | `0x000F4000` | Adafruit DFU Bootloader         |
| Bootloader Settings | `0x000FF000` | CRC + App-Metadaten (4 KB)      |
| UICR                | `0x10001000` | `BOOTLOADERADDR` @ `0x10001014` |

### UICR prüfen

```bash
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000 -autoconnect 1 << 'EOF'
mem32 0x10001014 1
exit
EOF
```

Erwarteter Wert: `0x000F4000` (Bootloader-Adresse).
Wert `0xFFFFFFFF` → Bootloader fehlt oder UICR gelöscht → Full-Restore nötig.

## Upload (Normalfall)

```bash
cd examples/nRF52_Basic
pio run -e nrf52840dk -t upload
```

PlatformIO schreibt automatisch:

1. `firmware.bin` @ `0x26000`
2. `firmware_signature.bin` @ `0xFF000` (Bootloader-Settings mit App-CRC)

**Ohne `firmware_signature.bin`** startet der Bootloader die App nicht
und bleibt im DFU-Modus (pulsierendes LED).

## ⚠️ CPU bleibt nach jedem PIO-Upload gehalten

**Ursache (hardcodiert in PIO):**
`~/.platformio/platforms/nordicnrf52/builder/main.py` → `_jlink_cmd_script()` generiert:

```text
h
loadbin firmware.bin, 0x26000
loadbin firmware_signature.bin, 0xFF000
r
q
```

`r` = Reset+Halt, `q` = quit – **kein `g` (go)**. CPU friert nach jedem Upload ein.

**Dauerlösung: `extra_scripts = post:post_upload.py` in platformio.ini**

`post_upload.py` übernimmt **zwei** Aufgaben:

1. **Pre-Upload** – stellt den kompletten BLE-Stack (MBR, SoftDevice S140,
   Bootloader, UICR) aus der Framework-HEX wieder her, bevor PIO das
   App-Binary flasht.
   JLink vergleicht zuerst und flasht nur geänderte Sektoren – dauert
   ≈ 2–3 s extra wenn der Stack intakt ist, spart den manuellen
   Full-Restore wenn er gelöscht wurde.

2. **Post-Upload** – sendet `g` (go) damit die CPU nach dem Upload
   tatsächlich startet.

```python
# post_upload.py  (examples/nRF52_Basic/post_upload.py)
import glob
import os
import subprocess
import tempfile

Import("env")  # noqa: F821


def _jlink_run(commands):
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jlink", delete=False) as f:
        f.write("\n".join(commands) + "\n")
        tmpfile = f.name
    try:
        return subprocess.run(
            ["JLinkExe", "-device", "nRF52840_xxAA", "-if", "SWD",
             "-speed", "4000", "-autoconnect", "1", "-CommandFile", tmpfile],
            capture_output=True, text=True,
        )
    finally:
        os.unlink(tmpfile)


def jlink_restore_stack(source, target, env):
    if env.get("UPLOAD_PROTOCOL") != "jlink":
        return
    fw_dir = env.PioPlatform().get_package_dir("framework-arduinoadafruitnrf52")
    board_variant = env.BoardConfig().get("build.variant", "pca10056")
    bl_dir = os.path.join(fw_dir, "bootloader", board_variant)
    matches = sorted(glob.glob(os.path.join(bl_dir, "*.hex")))
    if not matches:
        print(f">> pre_upload: No bootloader HEX found in {bl_dir} – skipping")
        return
    bl_hex = matches[-1]
    print(">> pre_upload: Restoring MBR + SoftDevice + Bootloader + UICR")
    print(f"   HEX: {os.path.basename(bl_hex)}")
    r = _jlink_run(["h", f"loadfile {bl_hex}", "exit"])
    print(">> pre_upload: BLE stack restored OK" if r.returncode == 0
          else ">> pre_upload: Restore FAILED\n" + r.stderr)


def jlink_go_after_upload(source, target, env):
    if env.get("UPLOAD_PROTOCOL") != "jlink":
        return
    print(">> post_upload: sending 'g' to release CPU halt...")
    r = _jlink_run(["g", "exit"])
    print(">> post_upload: CPU released (go OK)" if r.returncode == 0
          else ">> post_upload: FAILED\n" + r.stderr)


env.AddPreAction("upload", jlink_restore_stack)   # noqa: F821
env.AddPostAction("upload", jlink_go_after_upload)  # noqa: F821
```

> **Hinweis:** `/dev/stdin` funktioniert **nicht** als `-CommandFile`
> bei JLinkExe → immer Tempfile verwenden.

**Manueller Einzel-Fix (ohne Post-Script):**

```bash
# Tempfile nötig – /dev/stdin funktioniert nicht mit JLinkExe!
printf 'g\nexit\n' > /tmp/jlink_go.jlink
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000 -autoconnect 1 \
  -CommandFile /tmp/jlink_go.jlink
```

**Flash-Zustand prüfen (vor `g`):**

```bash
printf 'regs\nmem 0x00000000, 4\nexit\n' > /tmp/jlink_diag.jlink
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000 -autoconnect 1 \
  -CommandFile /tmp/jlink_diag.jlink
```

- `PC` = gültige Adresse + kein Fault → nur CPU angehalten → `g` genügt
- `PC = FFFFFFFE` + `0x00000000 = FF FF FF FF` → SoftDevice gelöscht
  → **Full-Restore nötig**
- `XPSR IPSR = 003 (HardFault)` → CPU in HardFault
  → `g` hilft nicht → **Full-Restore nötig**

## Full-Restore (nach versehentlichem Chip-Erase)

> **Normalfall:** `post_upload.py` stellt den Stack automatisch vor jedem
> Upload wieder her. Der manuelle Restore unten ist nur nötig wenn auch
> `post_upload.py` nicht mehr hilft
> (z. B. JLink-Verbindung verloren, PIO gar nicht startbar).

```bash
BL=~/.platformio/packages/framework-arduinoadafruitnrf52/bootloader/pca10056/pca10056_bootloader-0.9.0_s140_6.1.1.hex

# Schreibt erase + komplette HEX (MBR + SoftDevice + Bootloader + UICR) + go
printf "erase\nloadfile %s\nr\ng\nexit\n" "$BL" > /tmp/restore.jlink
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000 -autoconnect 1 -CommandFile /tmp/restore.jlink

# Danach: App + firmware_signature.bin via PIO flashen
cd examples/nRF52_Basic && pio run -e nrf52840dk -t upload
```

> **Hinweis:** `loadfile` für die `.hex`
> (enthält SoftDevice + Bootloader + UICR).
> `loadbin` für die App `.bin`
> (ohne Header, immer mit Zieladresse `0x26000`).

## ⚠️ Häufige Falle: Partielles Erase löscht Bootloader

`erase 0x26000 0x100000` löscht auch den Bootloader bei `0xF4000`!
UICR bleibt erhalten → Boot-Loop / DFU-Pulsieren.

**Sichere Alternative für App-only Update:**

```bash
# Nur App-Seiten (0x26000–0x51FFF), Bootloader bei 0xF4000 bleibt
erase 0x26000 0x51000
loadbin firmware.bin 0x26000
```

Besser: immer `pio run -t upload` verwenden.

## LED-Pin-Mapping (pca10056 / Adafruit BSP)

```text
LED_RED   = PIN_LED1 = Arduino 13 → P0.13 (LED1 auf DK)
LED_BLUE  = PIN_LED2 = Arduino 14 → P0.14 (LED2 auf DK)
PIN_LED3  = Arduino 15 → P0.15 (LED3 auf DK)
PIN_LED4  = Arduino 16 → P0.16 (LED4 auf DK)
LED_STATE_ON = 0 (active-LOW)
```

`initVariant()` im BSP setzt alle 4 LEDs automatisch auf OUTPUT + OFF beim Start.

## Direktes GPIO ohne BSP (Busy-Wait-Blink für Early-Boot-Test)

```cpp
#define GPIO0_OUTSET (*(volatile uint32_t*)0x50000508UL)
#define GPIO0_OUTCLR (*(volatile uint32_t*)0x5000050CUL)
#define GPIO0_DIRSET (*(volatile uint32_t*)0x50000518UL)
#define LED1_BIT (1u << 13)

GPIO0_DIRSET = LED1_BIT;
GPIO0_OUTCLR = LED1_BIT;  // ON  (active-LOW)
for (volatile uint32_t d = 0; d < 400000; d++) {}
GPIO0_OUTSET = LED1_BIT;  // OFF
```

Nützlich wenn `delay()` / FreeRTOS noch nicht initialisiert sind.

## DFU-Modus erkennen

- **Pulsierendes LED** = Adafruit Bootloader im DFU-Modus
- Ursache: `firmware_signature.bin` fehlt oder ist ungültig
- Fix: `pio run -t upload` (schreibt signature automatisch)

## Serial Monitor

### J-Link VCOM (Serial2 / UART) – empfohlen für nRF52840-DK

- Port: J-Link VCOM (Serial2 UART) – aktuell `/dev/ttyACM0`, Nummer kann variieren
- Kein zweites USB-Kabel nötig
- Port-Nummer mit `ls /dev/ttyACM*` oder `pio device list` ermitteln

```bash
pio device monitor --port /dev/ttyACM0 --baud 115200
```

**Im Code mit `DBG_SERIAL`-Makro (statt `-DSerial=Serial2` Build-Flag):**

```cpp
#if defined(BOARD_NRF52DK)
  #define DBG_SERIAL Serial2   // J-Link VCOM (ttyACM2)
#else
  #define DBG_SERIAL Serial    // TinyUSB CDC
#endif
```

> **Warum nicht `-DSerial=Serial2`?**
> Der Präprozessor würde `Adafruit_USBD_CDC Serial` zu
> `Adafruit_USBD_CDC Serial2` umbenennen – und kollidiert dann mit der
> BSP-Deklaration `Uart Serial2`. Build-Fehler.

### TinyUSB CDC (`Serial`) – für XIAO / Feather

TinyUSB erzeugt einen eigenen CDC-Port (erscheint nach `Serial.begin()`).
`monitor_port` weglassen oder auf den USB-CDC-Port zeigen.

Warte-Schleife im Code:

```cpp
while (!DBG_SERIAL && (millis() - startTime < 8000)) { /* ... */ }
```

`!Serial2` (UART) ist immer `false` → Schleife verlässt sofort;
`!Serial` (USB CDC) wartet bis Port geöffnet.
