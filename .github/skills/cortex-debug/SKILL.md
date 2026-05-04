---
name: cortex-debug
description: "Configure and use the Cortex-Debug VS Code extension for ARM Cortex-M debugging. Use when: setting up launch.json for J-Link/SWD, debugging nRF52840 with FreeRTOS RTOS plugin, using gdb-multiarch, reading CPU registers via JLinkExe, resolving 'CPU halted' or 'no blink' issues after halt commands, checking PC/reset vector after corrupt flash."
argument-hint: "Optional: target MCU or specific debug issue (e.g. 'nRF52840 FreeRTOS', 'halt', 'reset vector')"
---

# Cortex-Debug für nRF52840 (J-Link + VS Code)

## VS Code Extension

- Extension ID: `marus25.cortex-debug`
- Erfordert: `gdb-multiarch` (`sudo apt install gdb-multiarch`)
- J-Link GDB Server: `/opt/SEGGER/JLink_V876/JLinkGDBServerCLExe` (symlink: `/usr/bin/JLinkGDBServer`)

## launch.json (nRF52840-DK mit FreeRTOS)

```json
{
  "version": "0.2.0",
  "configurations": [{
    "name": "nRF52840-DK (J-Link)",
    "type": "cortex-debug",
    "request": "launch",
    "servertype": "jlink",
    "device": "nRF52840_xxAA",
    "interface": "swd",
    "runToEntryPoint": "setup",
    "executable": "${workspaceFolder}/examples/nRF52_Basic/.pio/build/nrf52840dk/firmware.elf",
    "svdFile": "/home/daniel/.platformio/platforms/nordicnrf52/misc/svd/nrf52840.svd",
    "JLinkGDBServerPath": "/usr/bin/JLinkGDBServer",
    "serverArgs": ["-rtos", "GDBServer/RTOSPlugin_FreeRTOS"],
    "armToolchainPath": "/home/daniel/.platformio/packages/toolchain-gccarmnoneeabi/bin",
    "gdbPath": "/usr/bin/gdb-multiarch"
  }]
}
```

**Wichtig:** Das FreeRTOS-Plugin (`serverArgs`) ist zwingend, wenn das
Adafruit-BSP verwendet wird – sonst werden FreeRTOS-Tasks nicht aufgelöst
und `runToEntryPoint: "setup"` funktioniert nicht.

## platformio.ini Debug-Konfiguration

```ini
debug_tool = jlink
build_type = debug
debug_build_flags = -O0 -ggdb3
debug_svd_path = /home/daniel/.platformio/platforms/nordicnrf52/misc/svd/nrf52840.svd
debug_server_parameters = -rtos GDBServer/RTOSPlugin_FreeRTOS
```

## CPU-Zustand per JLinkExe prüfen

```bash
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000 -autoconnect 1 << 'EOF'
halt
regs
mem32 0x26000 4
exit
EOF
```

Wichtige Register:

- `PC` = aktueller Programmzähler
- `XPSR` Bit 0–8 = Exception-Nummer (0 = kein Fault)
- `CONTROL` = 02 → FreeRTOS Task aktiv (PSP), 00 → privileged MSP

## ⚠️ Häufige Falle: CPU bleibt im Halt

Nach einem `halt`-Befehl im JLinkExe-Skript wird die CPU eingefroren.
Wenn das Script danach `exit` ausführt,
**läuft die CPU NICHT weiter**.

**⚠️ Das gilt auch nach `pio run -t upload` (jlink)!**
PIO's `_jlink_cmd_script()` in `builder/main.py` generiert hardcodiert
`r` (Reset+Halt) + `q` (quit) ohne `g`.
→ **Dauerlösung: `post_upload.py` als
`extra_scripts = post:post_upload.py`**
(siehe nrf52840-platformio SKILL).

Das Script übernimmt zwei Aufgaben:

- **Pre-Upload**: Stellt MBR + SoftDevice S140 + Bootloader + UICR aus der
  Framework-HEX wieder her (automatisch bei jedem Upload → kein manueller
  Full-Restore mehr nötig)
- **Post-Upload**: Sendet `g` damit die CPU tatsächlich startet

**Manueller Fix (Tempfile – `/dev/stdin` funktioniert NICHT mit JLinkExe!):**

```bash
printf 'g\nexit\n' > /tmp/jlink_go.jlink
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000 -autoconnect 1 -CommandFile /tmp/jlink_go.jlink
```

## ⚠️ Flash komplett gelöscht – Diagnose

```bash
printf 'regs\nmem 0x00000000, 4\nexit\n' > /tmp/jlink_diag.jlink
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000 -autoconnect 1 -CommandFile /tmp/jlink_diag.jlink
```

Auswertung:

- `PC` = gültige Adresse + kein Fault → nur CPU angehalten → `g` genügt
- `PC = FFFFFFFE` **und** `0x00000000 = FF FF FF FF` → SoftDevice weg,
  CPU in HardFault → `g` hilft nicht
  → Full-Restore nötig (siehe nrf52840-platformio SKILL)
- `XPSR IPSR = 003 (HardFault)` → gleiches wie oben

## Ausführungskette verifizieren (gdb-multiarch)

```bash
gdb-multiarch -batch \
  -ex "file firmware.elf" \
  -ex "info line *0x<PC-Adresse>" \
  -ex "disassemble /m 0x<PC>,+32"
```

Erwartete Boot-Kette auf nRF52840 (Adafruit BSP):

1. `Reset_Handler` (SoftDevice MBR springt zu App-Vektor-Tabelle)
2. `main()` → FreeRTOS-Init
3. `vTaskStartScheduler()`
4. `loop_task` → `setup()` → `loop()`

## Reset-Vektor prüfen

```bash
JLinkExe -device nRF52840_xxAA -if SWD -speed 4000 -autoconnect 1 << 'EOF'
mem32 0x26000 4
exit
EOF
```

- `0x26000` = App-Vektor-Tabelle (Anfang nach SoftDevice)
- Word 0 = Initial Stack Pointer (~`0x20040000`)
- Word 1 = Reset Handler Adresse (Bit 0 = 1 = Thumb-Mode)

Beispiel OK: `20040000 00039B8D` → Stack bei 0x20040000, Reset_Handler bei 0x39B8C.

## Troubleshooting

**`runToEntryPoint: "setup"` bricht nie an:**

- FreeRTOS-Plugin fehlt in `serverArgs` → setup() wird im Task-Kontext nie erkannt

**Kein Symbol-Info in GDB:**

- `build_type = debug` und `debug_build_flags = -O0 -ggdb3` in platformio.ini sicherstellen

**J-Link GDB Server startet nicht:**

- Pfad prüfen: `which JLinkGDBServer` → sollte `/usr/bin/JLinkGDBServer` sein
- `JLinkGDBServerPath` in launch.json explizit setzen

**gdb-multiarch nicht gefunden:**

```bash
sudo apt install gdb-multiarch
```
