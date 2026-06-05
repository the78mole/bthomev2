# BThome Logger Tools

This directory contains tools for testing and debugging BThome devices.

## 🐍 Python BThome Logger

A Python tool for scanning and displaying BThome v2 advertisements.
It supports two scan modes:

| Mode | How it works | Privileges needed |
| --- | --- | --- |
| **Normal** (default) | Uses [bleak](https://github.com/hbldh/bleak) via BlueZ D-Bus API | None |
| **Raw HCI** (`-r`) | Passively monitors `HCI_CHANNEL_MONITOR` (kernel channel 2) — receives a copy of every HCI event without interfering with BlueZ | `CAP_NET_RAW + CAP_NET_ADMIN` (via `setcap`, no `sudo` at runtime) |

### Installation

#### Option 1 – `uv tool install` (recommended)

```bash
# Install uv if not already available
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install bthome-logger as an isolated tool
uv tool install bthome-logger

# The bthome-logger command is now available system-wide
bthome-logger --version
```

To also enable **Raw HCI mode** (`-r`), grant capabilities once after installation:

```bash
# Find the Python interpreter inside the uv tool environment
UV_PYTHON=$(readlink -f \
  $(uv tool run bthome-logger python -c 'import sys; print(sys.executable)' \
  2>/dev/null) \
  || readlink -f ~/.local/share/uv/tools/bthome-logger/bin/python)

# Apply file capabilities (no sudo required at runtime afterwards)
sudo setcap cap_net_raw,cap_net_admin+eip "$UV_PYTHON"

# Verify
getcap "$UV_PYTHON"
# Expected:  …/python3.x cap_net_admin,cap_net_raw=eip
```

> **Note:** Re-run the `setcap` command after `uv tool upgrade bthome-logger`,
> because upgrading replaces the Python interpreter binary.

#### Option 2 – `pipx`

```bash
pipx install bthome-logger

# For raw mode, apply capabilities to the pipx venv interpreter
sudo setcap cap_net_raw,cap_net_admin+eip \
  $(readlink -f ~/.local/share/pipx/venvs/bthome-logger/bin/python)
```

#### Option 3 – Development (from repository)

```bash
# Install uv if not already available
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/the78mole/bthomev2.git
cd bthomev2/tools

# Run directly via uv (installs dependencies automatically into tools/.venv)
uv run bthome_logger.py

# For raw mode, apply capabilities to the venv interpreter
sudo setcap cap_net_raw,cap_net_admin+eip \
  $(readlink -f .venv/bin/python)
```

### Usage

```bash
# Basic usage – filters devices with "MAKE" in name
bthome-logger

# Custom name filter
bthome-logger --filter ESP32
bthome-logger -f MyDevice

# Show all advertisements regardless of name
bthome-logger -f ""

# Verbose mode – also print raw hex frames
bthome-logger --verbose
bthome-logger -v

# Raw HCI mode – shows every AD structure (LEN/TYPE/VALUE) directly from HCI socket
bthome-logger --raw
bthome-logger -r

# Raw mode, verbose (also prints raw hex of each monitor frame)
bthome-logger -r -v

# Select a different HCI adapter (default: hci0)
bthome-logger --hci 1
bthome-logger -a 1

# List all available HCI adapters
bthome-logger --list-hci
bthome-logger -l

# Shell completion
bthome-logger --install-completion   # install for current shell
bthome-logger -i                     # same, short form
bthome-logger -i zsh                 # install for specific shell
bthome-logger --show-completion      # print completion script
bthome-logger -s                     # same, short form

# Help / version
bthome-logger --help
bthome-logger -h
bthome-logger --version
bthome-logger -V
```

### Features

- ✅ Scans for BLE devices with customizable name filter
- ✅ Detects BThome v2 Service UUID (0xFCD2)
- ✅ Decodes all common BThome Object IDs (temperature, humidity, battery, …)
- ✅ Colorized terminal output with RSSI color coding
- ✅ Supports encrypted and unencrypted packets
- ✅ **Raw HCI mode** (`-r`): shows every AD structure directly from the HCI socket
  - Decodes both classic LE Advertising Reports (subevent 0x02) and
    BT 5.0 Extended Advertising Reports (subevent 0x0D)
  - Passively monitors via `HCI_CHANNEL_MONITOR` – no BlueZ interference
- ✅ `--list-hci`: enumerate all available HCI adapters
- ✅ CLI with `--help` and `--version` support

### Output Example – Normal Mode

```text
======================================================================
🔵 BThome Logger - Python Edition
Scans for BLE devices with BThome v2 protocol
======================================================================

Filter: Devices with 'MAKE' in name
Press Ctrl+C to exit

✓ Scanner started...

----------------------------------------------------------------------
[14:32:45.123] 📱 MAKE-300 (E8:07:AF:5A:C6:0C)
  RSSI: -65 dBm
  BThome: v2 (unencrypted)
  Values:
    • Temperature (0x02): 22.50 °C [CA08]
    • Packet ID (0x00): 99 [63]
```

### Output Example – Raw HCI Mode (`-r`)

```text
======================================================================
🔵 BThome Logger - Python Edition
Scans for BLE devices with BThome v2 protocol
======================================================================

Filter: Devices with 'MAKE' in name
Press Ctrl+C to exit

✓ Raw HCI monitor started on hci0 (via HCI_CHANNEL_MONITOR)...

----------------------------------------------------------------------
[14:57:49.700] 📱 MAKE-300 (E8:07:AF:5A:C6:0C)
  RSSI: -73 dBm
  AD Structures:
    LEN=0x02  TYPE=0x01  [Flags]
      VALUE= 06  → 0x06 (LE Gen Discoverable, BR/EDR Not Supported)
    LEN=0x09  TYPE=0x09  [Complete Local Name]
      VALUE= 4D 41 4B 45 2D 33 30 30  → "MAKE-300"
    LEN=0x10  TYPE=0x16  [Service Data – 16-bit UUID]
      VALUE= D2 FC 40 00 8F 02 CA 08 0C 18 00 10 00 21 00  → UUID=0xFCD2  payload=…
  BThome: v2 (unencrypted)
  Values:
    • Packet ID (0x00): 143 [8F]
    • Temperature (0x02): 22.50 °C [CA08]
    • Voltage (0x0C): 0.02 V [1800]
    • Power (0x10): 0 [00]
    • Motion (0x21): 0 [00]
```

### Granting capabilities for Raw HCI Mode

Raw HCI mode opens a kernel `HCI_CHANNEL_MONITOR` socket which requires
`CAP_NET_RAW` and `CAP_NET_ADMIN`. These are granted via `setcap` once —
no `sudo` is needed at runtime afterwards.

When capabilities are missing, the tool **automatically detects the installation
method** and prints the exact command to run, including the correct resolved
interpreter path and a reminder when to repeat the step:

```text
✗ Raw HCI monitor bind failed (errno 1): Operation not permitted

  Install context: uv tool install   (tool: bthome-logger)
  Fix (run once):
    sudo setcap cap_net_raw,cap_net_admin+eip /home/…/uv/tools/bthome-logger/bin/python3.11
  Re-run after: uv tool upgrade bthome-logger
  Afterwards run without sudo as usual.
```

Just copy-paste the printed `sudo setcap …` line and run it once.

> **Important:** `setcap` must be applied to the **real binary**, not a symlink.
> The tool always resolves symlinks automatically.
> Re-apply after every interpreter replacement (upgrade, reinstall).

### Troubleshooting

**Raw mode: `bind failed (errno 1): Operation not permitted`**

File capabilities are not set. Copy-paste the `sudo setcap …` command that the
tool prints and run it once.

#### Raw mode: no packets appear, but BlueZ scans fine

Make sure a BLE scan session is active. Raw mode uses `HCI_CHANNEL_MONITOR`
which receives copies of HCI events from BlueZ — it does not start scanning
itself. Either run `bluetoothctl scan on` in another terminal, or start the
logger in normal mode first so it sets up the BlueZ discovery session.

**Problem:** `bleak` cannot be installed

```bash
python --version  # requires Python 3.8+
```

**Problem:** No Bluetooth permissions (normal mode)

```bash
# Add user to bluetooth group
sudo usermod -a -G bluetooth $USER
# Log out and back in, or:
newgrp bluetooth
```
