#!/usr/bin/env python3
"""
BThome Logger - Python Edition
Scans for BLE devices and displays BThome v2 advertisements
"""

import asyncio
import struct
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version

import typer
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

# Global variable for device name filter
DEVICE_NAME_FILTER = "MAKE"

# Global variable for verbose mode
VERBOSE = False


def get_version() -> str:
    """Get the package version"""
    try:
        return version("bthome-logger")
    except PackageNotFoundError:
        return "dev"


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"


# BThome v2 Object IDs with factors and units
# Keys: name, factor, unit, size (bytes), optional: signed, timestamp, firmware, variable
BTHOME_OBJECTS = {
    # --- Misc ---
    0x00: {"name": "Packet ID", "factor": 1, "unit": "", "size": 1},
    # --- Sensor data ---
    0x01: {"name": "Battery", "factor": 1, "unit": "%", "size": 1},
    0x02: {
        "name": "Temperature",
        "factor": 0.01,
        "unit": "°C",
        "signed": True,
        "size": 2,
    },
    0x03: {"name": "Humidity", "factor": 0.01, "unit": "%", "size": 2},
    0x04: {"name": "Pressure", "factor": 0.01, "unit": "hPa", "size": 3},
    0x05: {"name": "Illuminance", "factor": 0.01, "unit": "lx", "size": 3},
    0x06: {"name": "Mass (kg)", "factor": 0.01, "unit": "kg", "size": 2},
    0x07: {"name": "Mass (lb)", "factor": 0.01, "unit": "lb", "size": 2},
    0x08: {
        "name": "Dew Point",
        "factor": 0.01,
        "unit": "°C",
        "signed": True,
        "size": 2,
    },
    0x09: {"name": "Count", "factor": 1, "unit": "", "size": 1},
    0x0A: {"name": "Energy", "factor": 0.001, "unit": "kWh", "size": 3},
    0x0B: {"name": "Power", "factor": 0.01, "unit": "W", "size": 3},
    0x0C: {"name": "Voltage", "factor": 0.001, "unit": "V", "size": 2},
    0x0D: {"name": "PM2.5", "factor": 1, "unit": "µg/m³", "size": 2},
    0x0E: {"name": "PM10", "factor": 1, "unit": "µg/m³", "size": 2},
    # --- Binary sensors ---
    0x0F: {"name": "Generic Boolean", "factor": 1, "unit": "", "size": 1},
    0x10: {"name": "Power", "factor": 1, "unit": "", "size": 1},
    0x11: {"name": "Opening", "factor": 1, "unit": "", "size": 1},
    # --- Sensor data (continued) ---
    0x12: {"name": "CO2", "factor": 1, "unit": "ppm", "size": 2},
    0x13: {"name": "TVOC", "factor": 1, "unit": "µg/m³", "size": 2},
    0x14: {"name": "Moisture", "factor": 0.01, "unit": "%", "size": 2},
    # --- Binary sensors (continued) ---
    0x15: {"name": "Battery Low", "factor": 1, "unit": "", "size": 1},
    0x16: {"name": "Battery Charging", "factor": 1, "unit": "", "size": 1},
    0x17: {"name": "Carbon Monoxide", "factor": 1, "unit": "", "size": 1},
    0x18: {"name": "Cold", "factor": 1, "unit": "", "size": 1},
    0x19: {"name": "Connectivity", "factor": 1, "unit": "", "size": 1},
    0x1A: {"name": "Door", "factor": 1, "unit": "", "size": 1},
    0x1B: {"name": "Garage Door", "factor": 1, "unit": "", "size": 1},
    0x1C: {"name": "Gas Detected", "factor": 1, "unit": "", "size": 1},
    0x1D: {"name": "Heat", "factor": 1, "unit": "", "size": 1},
    0x1E: {"name": "Light Detected", "factor": 1, "unit": "", "size": 1},
    0x1F: {"name": "Lock", "factor": 1, "unit": "", "size": 1},
    0x20: {"name": "Moisture Detected", "factor": 1, "unit": "", "size": 1},
    0x21: {"name": "Motion", "factor": 1, "unit": "", "size": 1},
    0x22: {"name": "Moving", "factor": 1, "unit": "", "size": 1},
    0x23: {"name": "Occupancy", "factor": 1, "unit": "", "size": 1},
    0x24: {"name": "Plug", "factor": 1, "unit": "", "size": 1},
    0x25: {"name": "Presence", "factor": 1, "unit": "", "size": 1},
    0x26: {"name": "Problem", "factor": 1, "unit": "", "size": 1},
    0x27: {"name": "Running", "factor": 1, "unit": "", "size": 1},
    0x28: {"name": "Safety", "factor": 1, "unit": "", "size": 1},
    0x29: {"name": "Smoke", "factor": 1, "unit": "", "size": 1},
    0x2A: {"name": "Sound", "factor": 1, "unit": "", "size": 1},
    0x2B: {"name": "Tamper", "factor": 1, "unit": "", "size": 1},
    0x2C: {"name": "Vibration", "factor": 1, "unit": "", "size": 1},
    0x2D: {"name": "Window", "factor": 1, "unit": "", "size": 1},
    # --- Sensor data (0x2E+) ---
    0x2E: {"name": "Humidity", "factor": 1, "unit": "%", "size": 1},
    0x2F: {"name": "Moisture", "factor": 1, "unit": "%", "size": 1},
    # --- Events ---
    0x3A: {"name": "Button", "factor": 1, "unit": "", "size": 1},
    0x3B: {"name": "Command", "factor": 1, "unit": "", "size": -1, "variable": True},
    0x3C: {"name": "Dimmer", "factor": 1, "unit": "", "size": 2},
    # --- Sensor data (0x3D+) ---
    0x3D: {"name": "Count", "factor": 1, "unit": "", "size": 2},
    0x3E: {"name": "Count", "factor": 1, "unit": "", "size": 4},
    0x3F: {"name": "Rotation", "factor": 0.1, "unit": "°", "signed": True, "size": 2},
    0x40: {"name": "Distance (mm)", "factor": 1, "unit": "mm", "size": 2},
    0x41: {"name": "Distance (m)", "factor": 0.1, "unit": "m", "size": 2},
    0x42: {"name": "Duration", "factor": 0.001, "unit": "s", "size": 3},
    0x43: {"name": "Current", "factor": 0.001, "unit": "A", "size": 2},
    0x44: {"name": "Speed", "factor": 0.01, "unit": "m/s", "size": 2},
    0x45: {
        "name": "Temperature",
        "factor": 0.1,
        "unit": "°C",
        "signed": True,
        "size": 2,
    },
    0x46: {"name": "UV Index", "factor": 0.1, "unit": "", "size": 1},
    0x47: {"name": "Volume", "factor": 0.1, "unit": "L", "size": 2},
    0x48: {"name": "Volume", "factor": 1, "unit": "mL", "size": 2},
    0x49: {"name": "Volume Flow Rate", "factor": 0.001, "unit": "m³/hr", "size": 2},
    0x4A: {"name": "Voltage", "factor": 0.1, "unit": "V", "size": 2},
    0x4B: {"name": "Gas", "factor": 0.001, "unit": "m³", "size": 3},
    0x4C: {"name": "Gas", "factor": 0.001, "unit": "m³", "size": 4},
    0x4D: {"name": "Energy", "factor": 0.001, "unit": "kWh", "size": 4},
    0x4E: {"name": "Volume", "factor": 0.001, "unit": "L", "size": 4},
    0x4F: {"name": "Water", "factor": 0.001, "unit": "L", "size": 4},
    0x50: {"name": "Timestamp", "factor": 1, "unit": "", "size": 4, "timestamp": True},
    0x51: {"name": "Acceleration", "factor": 0.001, "unit": "m/s²", "size": 2},
    0x52: {"name": "Gyroscope", "factor": 0.001, "unit": "°/s", "size": 2},
    0x53: {"name": "Text", "factor": 1, "unit": "", "size": -1, "variable": True},
    0x54: {"name": "Raw", "factor": 1, "unit": "", "size": -1, "variable": True},
    0x55: {"name": "Volume Storage", "factor": 0.001, "unit": "L", "size": 4},
    0x56: {"name": "Conductivity", "factor": 1, "unit": "µS/cm", "size": 2},
    0x57: {"name": "Temperature", "factor": 1, "unit": "°C", "signed": True, "size": 1},
    0x58: {
        "name": "Temperature",
        "factor": 0.35,
        "unit": "°C",
        "signed": True,
        "size": 1,
    },
    0x59: {"name": "Count", "factor": 1, "unit": "", "signed": True, "size": 1},
    0x5A: {"name": "Count", "factor": 1, "unit": "", "signed": True, "size": 2},
    0x5B: {"name": "Count", "factor": 1, "unit": "", "signed": True, "size": 4},
    0x5C: {"name": "Power", "factor": 0.01, "unit": "W", "signed": True, "size": 4},
    0x5D: {"name": "Current", "factor": 0.001, "unit": "A", "signed": True, "size": 2},
    0x5E: {"name": "Direction", "factor": 0.01, "unit": "°", "size": 2},
    0x5F: {"name": "Precipitation", "factor": 0.1, "unit": "mm", "size": 2},
    0x60: {"name": "Channel", "factor": 1, "unit": "", "size": 1},
    0x61: {"name": "Rotational Speed", "factor": 1, "unit": "rpm", "size": 2},
    0x62: {
        "name": "Speed",
        "factor": 0.000001,
        "unit": "m/s",
        "signed": True,
        "size": 4,
    },
    0x63: {
        "name": "Acceleration",
        "factor": 0.000001,
        "unit": "m/s²",
        "signed": True,
        "size": 4,
    },
    0x64: {"name": "Light Level", "factor": 1, "unit": "", "size": 1},
    0x65: {"name": "Settings Revision", "factor": 1, "unit": "", "size": 1},
    # --- Device information ---
    0xF0: {"name": "Device Type ID", "factor": 1, "unit": "", "size": 2},
    0xF1: {
        "name": "Firmware Version",
        "factor": 1,
        "unit": "",
        "size": 4,
        "firmware": True,
    },
    0xF2: {
        "name": "Firmware Version",
        "factor": 1,
        "unit": "",
        "size": 3,
        "firmware": True,
    },
}

# BThome Company ID / Service Data UUID
BTHOME_COMPANY_ID = 0xFCD2
BTHOME_SERVICE_UUID = "0000fcd2-0000-1000-8000-00805f9b34fb"


def parse_bthome_packet(data: bytes) -> dict:
    """
    Parses a BThome v2 packet and returns decoded values

    Args:
        data: Raw manufacturer data without company ID

    Returns:
        Dictionary with device info and decoded values
    """
    if len(data) < 1:
        return None

    result = {
        "device_info": data[0],
        "encrypted": bool(data[0] & 0x01),
        "version": "v2",
        "values": [],
    }

    index = 1

    # Decode objects
    while index < len(data):
        object_id = data[index]
        index += 1

        if object_id not in BTHOME_OBJECTS:
            # Unbekanntes Object ID - abbrechen
            result["values"].append(
                {
                    "object_id": object_id,
                    "name": f"Unbekannt (0x{object_id:02X})",
                    "raw_value": None,
                    "value": None,
                    "unit": "",
                }
            )
            break

        obj_def = BTHOME_OBJECTS[object_id]
        size = obj_def["size"]

        # Sonderfälle: Variable Länge (Text, Raw, Command)
        if obj_def.get("variable", False):
            if index >= len(data):
                break
            if object_id in (0x53, 0x54):  # Text / Raw: volle Länge
                var_len = data[index]
                index += 1
                if index + var_len > len(data):
                    break
                raw_bytes = data[index : index + var_len]
                index += var_len
                display = (
                    raw_bytes.decode("utf-8", errors="replace")
                    if object_id == 0x53
                    else " ".join(f"{b:02x}" for b in raw_bytes)
                )
            else:  # Command (0x3B): low 5 bits = arg length, then opcode + args
                arg_len = data[index] & 0x1F
                cmd_total = 1 + arg_len  # opcode + args
                index += 1
                if index + cmd_total > len(data):
                    break
                raw_bytes = data[index : index + cmd_total]
                index += cmd_total
                display = " ".join(f"{b:02x}" for b in raw_bytes)
            result["values"].append(
                {
                    "object_id": object_id,
                    "name": obj_def["name"],
                    "raw_value": None,
                    "value": display,
                    "unit": "",
                    "formatted_value": display,
                }
            )
            continue

        if index + size > len(data):
            # Nicht genug Daten
            break

        # Wert auslesen
        raw_bytes = data[index : index + size]
        index += size

        # Wert dekodieren (Little Endian)
        if size == 1:
            raw_value = raw_bytes[0]
            if obj_def.get("signed", False) and raw_value >= 0x80:
                raw_value = raw_value - 0x100
        elif size == 2:
            raw_value = struct.unpack("<H", raw_bytes)[0]
            if obj_def.get("signed", False) and raw_value >= 0x8000:
                raw_value = raw_value - 0x10000
        elif size == 3:
            # 3 Bytes zu int (Little Endian)
            raw_value = raw_bytes[0] | (raw_bytes[1] << 8) | (raw_bytes[2] << 16)
            if obj_def.get("signed", False) and raw_value >= 0x800000:
                raw_value = raw_value - 0x1000000
        elif size == 4:
            raw_value = struct.unpack("<I", raw_bytes)[0]
            if obj_def.get("signed", False) and raw_value >= 0x80000000:
                raw_value = raw_value - 0x100000000
        else:
            raw_value = 0

        # Faktor anwenden
        value = raw_value * obj_def["factor"]

        # Eintrag aufbauen; ggf. Sonderformatierung ergänzen
        entry: dict = {
            "object_id": object_id,
            "name": obj_def["name"],
            "raw_value": raw_value,
            "value": value,
            "unit": obj_def["unit"],
        }
        if obj_def.get("timestamp", False):
            entry["formatted_value"] = datetime.fromtimestamp(
                raw_value, tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S UTC")
        elif obj_def.get("firmware", False):
            if size == 4:
                entry["formatted_value"] = (
                    f"{(raw_value >> 24) & 0xFF}.{(raw_value >> 16) & 0xFF}"
                    f".{(raw_value >> 8) & 0xFF}.{raw_value & 0xFF}"
                )
            else:  # size == 3
                entry["formatted_value"] = (
                    f"{(raw_value >> 16) & 0xFF}.{(raw_value >> 8) & 0xFF}"
                    f".{raw_value & 0xFF}"
                )
        result["values"].append(entry)

    return result


def format_timestamp() -> str:
    """Formats the current timestamp"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def print_header():
    """Prints the program header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}🔵 BThome Logger - Python Edition{Colors.RESET}")
    print(f"{Colors.CYAN}Scans for BLE devices with BThome v2 protocol{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")
    print(
        f"{Colors.YELLOW}Filter: Devices with '{DEVICE_NAME_FILTER}' in name{Colors.RESET}"
    )
    print(f"{Colors.GRAY}Press Ctrl+C to exit{Colors.RESET}\n")


def print_separator():
    """Prints a separator line"""
    print(f"{Colors.GRAY}{'-'*70}{Colors.RESET}")


def advertisement_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    """Called when a BLE advertisement is received"""
    try:
        _advertisement_callback_inner(device, advertisement_data)
    except Exception as exc:  # noqa: BLE001
        print(
            f"{Colors.RED}[{format_timestamp()}] Fehler im Callback für "
            f"{device.name} ({device.address}): {exc}{Colors.RESET}"
        )


def _advertisement_callback_inner(
    device: BLEDevice, advertisement_data: AdvertisementData
) -> None:
    """Inner callback – raises exceptions so the outer wrapper can display them."""

    # Apply device name filter
    if device.name and DEVICE_NAME_FILTER not in device.name:
        return

    # --- BThome via Service Data (Standard-Format) ---
    raw_data: bytes | None = None
    data_source = ""
    if advertisement_data.service_data:
        for uuid_key, svc_bytes in advertisement_data.service_data.items():
            if uuid_key.lower() == BTHOME_SERVICE_UUID:
                raw_data = svc_bytes
                data_source = "service_data"
                break

    # --- BThome via Manufacturer Data (nicht-standardisierte Implementierungen) ---
    if raw_data is None:
        if not advertisement_data.manufacturer_data:
            if VERBOSE:
                print(
                    f"{Colors.GRAY}[{format_timestamp()}] "
                    f"{device.name} ({device.address}) | no adv data | "
                    f"RSSI: {advertisement_data.rssi} dBm{Colors.RESET}"
                )
            return
        if BTHOME_COMPANY_ID in advertisement_data.manufacturer_data:
            raw_data = advertisement_data.manufacturer_data[BTHOME_COMPANY_ID]
            data_source = "manufacturer_data"
        else:
            # Kein BThome – im Verbose-Modus trotzdem anzeigen
            if VERBOSE:
                for (
                    company_id,
                    mfr_bytes,
                ) in advertisement_data.manufacturer_data.items():
                    hex_data = " ".join(f"{b:02x}" for b in mfr_bytes)
                    print(
                        f"{Colors.GRAY}[{format_timestamp()}]{Colors.RESET} "
                        f"{Colors.BLUE}{device.name}{Colors.RESET} "
                        f"({Colors.GRAY}{device.address}{Colors.RESET}) "
                        f"| Company ID: 0x{company_id:04X} | Data: {hex_data} | "
                        f"RSSI: {advertisement_data.rssi} dBm"
                    )
            return

    # BThome data found!
    if raw_data is None:
        return
    hex_data = " ".join(f"{b:02x}" for b in raw_data)

    # Header with device name and timestamp
    print_separator()
    print(
        f"{Colors.GRAY}[{format_timestamp()}]{Colors.RESET} "
        f"{Colors.BOLD}{Colors.GREEN}📱 {device.name}{Colors.RESET} "
        f"({Colors.GRAY}{device.address}{Colors.RESET})"
    )

    # RSSI
    if advertisement_data.rssi > -70:
        rssi_color = Colors.GREEN
    elif advertisement_data.rssi > -85:
        rssi_color = Colors.YELLOW
    else:
        rssi_color = Colors.RED

    rssi_text = f"{rssi_color}{advertisement_data.rssi} dBm{Colors.RESET}"
    print(f"  {Colors.GRAY}RSSI:{Colors.RESET} {rssi_text}")

    # Raw Data
    print(
        f"  {Colors.GRAY}Raw ({data_source}):{Colors.RESET} {Colors.CYAN}{hex_data}{Colors.RESET}"
    )

    # Parse BThome packet
    parsed = parse_bthome_packet(raw_data)

    if parsed:
        # Device Info
        encrypted_str = (
            f"{Colors.RED}encrypted{Colors.RESET}"
            if parsed["encrypted"]
            else f"{Colors.GREEN}unencrypted{Colors.RESET}"
        )
        print(
            f"  {Colors.GRAY}BThome:{Colors.RESET} {parsed['version']} ({encrypted_str})"
        )

        # Decoded values
        if parsed["values"]:
            print(f"  {Colors.GRAY}Values:{Colors.RESET}")
            for val in parsed["values"]:
                if "formatted_value" in val:
                    value_str = val["formatted_value"]
                elif val["unit"]:
                    value_str = f"{val['value']:.2f} {val['unit']}"
                else:
                    value_str = f"{val['value']}"

                raw = val["raw_value"]
                if raw is None:
                    hex_str = ""
                else:
                    obj_def = BTHOME_OBJECTS.get(val["object_id"], {})
                    sz = obj_def.get("size", 1)
                    hex_str = (
                        " [" + raw.to_bytes(sz, byteorder="little").hex().upper() + "]"
                    )

                print(
                    f"    {Colors.BOLD}{Colors.MAGENTA}• {val['name']} "
                    f"(0x{val['object_id']:02X}){Colors.RESET}: "
                    f"{Colors.YELLOW}{value_str}{Colors.GRAY}{hex_str}{Colors.RESET}"
                )
        else:
            print(f"    {Colors.GRAY}(No decoded values){Colors.RESET}")
    else:
        print(f"  {Colors.RED}Error parsing BThome packet{Colors.RESET}")

    print()  # Leerzeile


async def scan_forever():
    """Scans continuously for BLE devices"""
    print(f"{Colors.GREEN}✓ Scanner started...{Colors.RESET}\n")

    scanner = BleakScanner(detection_callback=advertisement_callback)

    try:
        await scanner.start()

        # Scan forever (or until Ctrl+C)
        while True:
            await asyncio.sleep(1.0)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Stopping scanner...{Colors.RESET}")
    finally:
        await scanner.stop()
        print(f"{Colors.GREEN}✓ Scanner stopped{Colors.RESET}\n")


app = typer.Typer(
    help="BThome v2 BLE Advertisement Logger - Scans and displays BThome devices"
)


@app.command()
def main(
    device_filter: str = typer.Option(
        "MAKE",
        "--filter",
        "-f",
        help="Filter BLE devices by this name (substring matching)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show all BLE advertisements, not just BThome devices",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        is_flag=True,
        help="Show version and exit",
    ),
):
    """
    Continuously scans for BLE devices and displays BThome v2 advertisements.

    The scanner filters devices by the specified name (substring matching).
    Press Ctrl+C to exit.
    """
    if version:
        print(f"bthome-logger {get_version()}")
        return

    global DEVICE_NAME_FILTER, VERBOSE
    DEVICE_NAME_FILTER = device_filter
    VERBOSE = verbose

    # Print header after filter is set
    print_header()

    try:
        asyncio.run(scan_forever())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app()
