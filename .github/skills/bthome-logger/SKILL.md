---
name: bthome-logger
description: "Install and run the bthome-logger BLE scanner tool. Use when: installing bthome-logger, running bthome-logger, scanning for BThome BLE devices, filtering BLE advertisements, debugging BThome sensors, using uv tool install bthome-logger, using uv run with bthome_logger.py, accessing the bthome-logger Python environment from scripts."
argument-hint: "Optional: device name filter (e.g. 'BThome', 'ESP32', 'MAKE')"
---

# BThome Logger

Scans BLE advertisements and decodes BThome v2 sensor data.
The tool source lives in [`tools/`](../../tools/) of this repository.

## Installation

### Recommended: `uv tool install` (isolated, system-wide)

```bash
# Install from PyPI
uv tool install bthome-logger

# Or directly from the local repo (picks up local changes)
uv tool install ./tools
```

After installation `bthome-logger` is available as a regular command:

```bash
bthome-logger                       # default filter: "MAKE"
bthome-logger --filter BThome       # custom name filter
bthome-logger --filter ""           # no filter – show all BThome devices
bthome-logger --filter ESP32 -v     # verbose output
```

To upgrade or reinstall:

```bash
uv tool install --reinstall bthome-logger
uv tool install --reinstall ./tools   # from local repo
```

### Alternative: `uv run` (no install, uses project venv)

Run directly from the `tools/` directory – `uv` resolves dependencies
from `tools/pyproject.toml` automatically:

```bash
cd tools
uv run python bthome_logger.py
uv run python bthome_logger.py --filter BThome
uv run python bthome_logger.py --filter "" -v
```

> **Note:** `uv run bthome_logger.py` (without `python`) fails –
> uv cannot spawn `.py` files directly.
> Always use `uv run python bthome_logger.py`.

From any directory using an absolute path:

```bash
uv run --project ./tools python tools/bthome_logger.py --filter BThome
```

### Access from own scripts

To call the bthome-logger Python API from custom scripts,
use `uv run` with the project as context:

```bash
# Run a custom script that imports bthome_logger inside the tool's venv
uv run --project ./tools python my_script.py
```

Inside `my_script.py`:

```python
# bthome_logger is resolvable because uv --project provides the venv
from bthome_logger import parse_bthome_packet, BTHOME_OBJECTS
```

## Common Options

| Option          | Short | Default | Description                        |
|-----------------|-------|---------|------------------------------------|
| `--filter TEXT` | `-f`  | `MAKE`  | Substring filter on device name    |
| `--verbose`     | `-v`  | off     | Show raw hex dump of each packet   |

## Expected Output

```text
Scans for BLE devices with BThome v2 protocol
======================================================================

Filter: Devices with 'BThome' in name
Press Ctrl+C to exit

✓ Scanner started...

[22:03:46.909] 📱 MAKE-nRF52 (CC:8F:EB:B8:55:B8)
  RSSI: -40 dBm
  Raw: 40 01 5d 02 3b 08 03 37 1a
  BThome: v2 (unencrypted)
  Values:
    • Battery (0x01): 93.00 % [5d]
    • Temperature (0x02): 21.07 °C [3b 08]
    • Humidity (0x03): 67.11 % [37 1a]
```

## Troubleshooting

**No devices shown:**

- Verify Bluetooth adapter is up: `hciconfig hci0 up`
- Check `bleak` requires no root on Linux if `CAP_NET_RAW` is set;
  otherwise run with `sudo`
- Confirm the device name filter matches: use `--filter ""` to see all BThome devices

**`bthome-logger: command not found` after `uv tool install`:**

- Ensure `~/.local/bin` is in `$PATH`: `export PATH="$HOME/.local/bin:$PATH"`
- Or run via `uv tool run bthome-logger`

**Install `uv` if not present:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
