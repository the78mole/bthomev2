#!/usr/bin/env python3
"""
BThome Logger - Python Edition
Scans for BLE devices and displays BThome v2 advertisements
"""

import asyncio
import ctypes
import os
import socket
import struct
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from typing import Optional

import typer
from bleak import BleakScanner
from bleak.args.bluez import BlueZScannerArgs, OrPattern
from bleak.assigned_numbers import AdvertisementDataType
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from typer.completion import install_callback, show_callback

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


def format_adv_header(advertisement_data: AdvertisementData) -> str:
    """Builds a compact header string from all available AdvertisementData fields."""
    parts: list[str] = []
    if advertisement_data.local_name:
        parts.append(f"Name: {advertisement_data.local_name}")
    if advertisement_data.tx_power is not None:
        parts.append(f"TX: {advertisement_data.tx_power} dBm")
    if advertisement_data.service_uuids:
        svc_data_keys = {k.lower() for k in (advertisement_data.service_data or {})}
        extra_uuids = [
            u
            for u in advertisement_data.service_uuids
            if u.lower() not in svc_data_keys
        ]
        if extra_uuids:
            parts.append(f"SvcUUIDs: {', '.join(extra_uuids)}")
    if advertisement_data.service_data:
        for uuid_key, svc_bytes in advertisement_data.service_data.items():
            hex_str = " ".join(f"{b:02x}" for b in svc_bytes)
            parts.append(f"SvcData[{uuid_key}]: {hex_str}")
    if advertisement_data.manufacturer_data:
        for company_id, mfr_bytes in advertisement_data.manufacturer_data.items():
            hex_str = " ".join(f"{b:02x}" for b in mfr_bytes)
            parts.append(f"MfrData[0x{company_id:04X}]: {hex_str}")
    return (" | " + " | ".join(parts)) if parts else ""


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
                    f"{Colors.GRAY}[{format_timestamp()}]{Colors.RESET} "
                    f"{device.name} ({device.address}) | no adv data"
                    f"{format_adv_header(advertisement_data)} | "
                    f"RSSI: {advertisement_data.rssi} dBm"
                )
            return
        if BTHOME_COMPANY_ID in advertisement_data.manufacturer_data:
            raw_data = advertisement_data.manufacturer_data[BTHOME_COMPANY_ID]
            data_source = "manufacturer_data"
        else:
            # Kein BThome – im Verbose-Modus trotzdem anzeigen
            if VERBOSE:
                print(
                    f"{Colors.GRAY}[{format_timestamp()}]{Colors.RESET} "
                    f"{Colors.BLUE}{device.name}{Colors.RESET} "
                    f"({Colors.GRAY}{device.address}{Colors.RESET})"
                    f"{format_adv_header(advertisement_data)} | "
                    f"RSSI: {advertisement_data.rssi} dBm"
                )
            return

    # BThome data found!
    if raw_data is None:
        return

    # Reconstruct full AD value including UUID/company-ID prefix (like nRF Connect shows)
    if data_source == "service_data":
        prefix_bytes = bytes(
            [BTHOME_COMPANY_ID & 0xFF, (BTHOME_COMPANY_ID >> 8) & 0xFF]
        )
    else:
        prefix_bytes = bytes(
            [BTHOME_COMPANY_ID & 0xFF, (BTHOME_COMPANY_ID >> 8) & 0xFF]
        )
    hex_data_full = " ".join(f"{b:02x}" for b in (prefix_bytes + raw_data))
    hex_data = " ".join(f"{b:02x}" for b in raw_data)

    # Im Verbose-Modus kompakte Einzeiler-Ausgabe (wie andere Geräte)
    if VERBOSE:
        print(
            f"{Colors.GRAY}[{format_timestamp()}]{Colors.RESET} "
            f"{Colors.GREEN}{device.name}{Colors.RESET} "
            f"({Colors.GRAY}{device.address}{Colors.RESET})"
            f"{format_adv_header(advertisement_data)} | "
            f"RSSI: {advertisement_data.rssi} dBm"
        )

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

    # Local Name (explicit, wie nRF Connect)
    local_name = advertisement_data.local_name or device.name
    if local_name:
        print(f"  {Colors.GRAY}Local Name:{Colors.RESET} {local_name}")

    # Raw Data – mit UUID/Company-ID-Präfix (wie nRF Connect Type 0x16)
    print(
        f"  {Colors.GRAY}Raw ({data_source}):{Colors.RESET} "
        f"{Colors.CYAN}{hex_data_full}{Colors.RESET}"
        f"  {Colors.GRAY}({hex_data}){Colors.RESET}"
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
                    is_signed = obj_def.get("signed", False)
                    hex_str = (
                        " ["
                        + raw.to_bytes(sz, byteorder="little", signed=is_signed)
                        .hex()
                        .upper()
                        + "]"
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

    scanner = BleakScanner(
        detection_callback=advertisement_callback,
        bluez=BlueZScannerArgs(
            or_patterns=[
                # Match BThome v2 Service Data UUID 0xFCD2 (little-endian)
                # Using advertisement monitor forces BlueZ to report duplicates
                OrPattern(
                    0,
                    AdvertisementDataType.SERVICE_DATA_UUID16,
                    b"\xd2\xfc",
                )
            ]
        ),
    )

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


# ── Raw HCI scanning ──────────────────────────────────────────────────────────
# Uses a raw AF_BLUETOOTH/BTPROTO_HCI socket to capture every advertisement
# with all AD structures intact (LEN / TYPE / VALUE), just like nRF Connect.
# Requires root or CAP_NET_RAW on the process.

_AF_BLUETOOTH = getattr(socket, "AF_BLUETOOTH", 31)
_BTPROTO_HCI = getattr(socket, "BTPROTO_HCI", 1)
_SOL_HCI = 0
_HCI_FILTER = 2
_HCI_EVENT_PKT = 0x04
_HCI_LE_META = 0x3E
_LE_ADV_REPORT = 0x02
_LE_EXT_ADV_REPORT = 0x0D
_OGF_LE_CTL = 0x08
_OCF_LE_SET_SCAN_PARAMS = 0x000B
_OCF_LE_SET_SCAN_ENABLE = 0x000C
_HCI_CHANNEL_RAW = 0
_HCI_CHANNEL_MONITOR = 2
_HCI_DEV_NONE = 0xFFFF  # used with HCI_CHANNEL_MONITOR


def _hci_bind(
    sock: socket.socket, dev_id: int, channel: int = _HCI_CHANNEL_RAW
) -> None:
    """Bind an HCI socket to a device and channel.

    Use channel=_HCI_CHANNEL_MONITOR (4) to receive a copy of all HCI traffic
    without interfering with BlueZ (like btmon).  This works even when BlueZ
    manages the adapter and requires only CAP_NET_RAW.

    Python's socket.bind() raises 'bad family' when AF_BLUETOOTH is not
    compiled into the Python build (e.g. uv standalone Pythons).  Fall back
    to calling libc.bind() directly via ctypes.
    """
    # sockaddr_hci: sa_family_t (u16) + hci_dev (u16) + hci_channel (u16)
    sockaddr = struct.pack("HHH", 31, dev_id, channel)
    if hasattr(socket, "AF_BLUETOOTH") and channel == _HCI_CHANNEL_RAW:
        sock.bind((dev_id,))
        return
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    ret = libc.bind(sock.fileno(), ctypes.c_char_p(sockaddr), len(sockaddr))
    if ret != 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))


_AD_TYPE_NAMES: dict[int, str] = {
    0x01: "Flags",
    0x02: "Incomplete 16-bit Service UUIDs",
    0x03: "Complete 16-bit Service UUIDs",
    0x06: "Incomplete 128-bit Service UUIDs",
    0x07: "Complete 128-bit Service UUIDs",
    0x08: "Shortened Local Name",
    0x09: "Complete Local Name",
    0x0A: "TX Power Level",
    0x16: "Service Data – 16-bit UUID",
    0xFF: "Manufacturer Specific Data",
}


class _HciFilter(ctypes.Structure):
    """Platform-correct hci_filter struct (unsigned long = 4 or 8 bytes depending on arch)."""

    _fields_ = [
        ("type_mask", ctypes.c_ulong),
        ("event_mask", ctypes.c_ulong * 2),
        ("opcode", ctypes.c_uint16),
    ]


def _hci_filter_le_adv() -> bytes:
    """HCI socket filter: only LE Meta events (struct hci_filter)."""
    f = _HciFilter()
    f.type_mask = 1 << _HCI_EVENT_PKT  # bit 4
    f.event_mask[0] = 1 << _HCI_LE_META  # bit 62
    f.event_mask[1] = 0
    f.opcode = 0
    return bytes(f)


def _hci_cmd(sock: socket.socket, ogf: int, ocf: int, params: bytes = b"") -> None:
    opcode = (ogf << 10) | ocf
    sock.send(struct.pack("<BHB", 0x01, opcode, len(params)) + params)


def _ad_parse(data: bytes) -> list[tuple[int, int, bytes]]:
    """Parse BLE AD structures. Returns list of (length, type, value)."""
    result: list[tuple[int, int, bytes]] = []
    i = 0
    while i < len(data):
        length = data[i]
        if length == 0:
            break
        if i + 1 + length > len(data):
            break
        result.append((length, data[i + 1], data[i + 2 : i + 1 + length]))
        i += 1 + length
    return result


def _ad_decode(ad_type: int, value: bytes) -> str:
    """Human-readable inline decode of an AD value."""
    if ad_type in (0x08, 0x09) and value:
        return f'"{value.decode("utf-8", errors="replace")}"'
    if ad_type == 0x01 and value:
        f = value[0]
        parts = []
        if f & 0x01:
            parts.append("LE Ltd Discoverable")
        if f & 0x02:
            parts.append("LE Gen Discoverable")
        if f & 0x04:
            parts.append("BR/EDR Not Supported")
        return f"0x{f:02X}" + (f" ({', '.join(parts)})" if parts else "")
    if ad_type in (0x02, 0x03) and len(value) >= 2:
        uuids = [
            f"0x{value[j] | value[j + 1] << 8:04X}" for j in range(0, len(value) - 1, 2)
        ]
        return ", ".join(uuids)
    if ad_type == 0x16 and len(value) >= 2:
        uuid = value[0] | (value[1] << 8)
        payload_hex = " ".join(f"{b:02X}" for b in value[2:])
        return f"UUID=0x{uuid:04X}" + (f"  payload={payload_hex}" if value[2:] else "")
    if ad_type == 0xFF and len(value) >= 2:
        cid = value[0] | (value[1] << 8)
        return f"Company=0x{cid:04X}"
    if ad_type == 0x0A and value:
        return f"{struct.unpack('b', bytes([value[0]]))[0]} dBm"
    return ""


def _hci_parse_ext_adv_reports(data: bytes) -> list[dict]:
    """Parse LE Extended Advertising Report payload (BT 5.0, subevent 0x0D)."""
    # Per report: event_type(2) addr_type(1) addr(6) primary_phy(1) secondary_phy(1)
    #             sid(1) tx_power(1) rssi(1) periodic_interval(2)
    #             direct_addr_type(1) direct_addr(6) data_len(1) = 24 bytes fixed
    reports: list[dict] = []
    if not data:
        return reports
    num = data[0]
    pos = 1
    for _ in range(num):
        if pos + 24 > len(data):
            break
        addr = ":".join(f"{b:02X}" for b in reversed(data[pos + 3 : pos + 9]))
        rssi = struct.unpack("b", bytes([data[pos + 13]]))[0]
        ad_len = data[pos + 23]
        pos += 24
        if pos + ad_len > len(data):
            break
        ad_data = data[pos : pos + ad_len]
        pos += ad_len
        reports.append({"address": addr, "ad_data": ad_data, "rssi": rssi})
    return reports


def _hci_parse_adv_reports(data: bytes) -> list[dict]:
    """Parse LE Advertising Report payload (starting at num_reports byte)."""
    reports: list[dict] = []
    if not data:
        return reports
    num = data[0]
    offset = 1
    for _ in range(num):
        if offset + 9 > len(data):
            break
        addr = ":".join(f"{b:02X}" for b in reversed(data[offset + 2 : offset + 8]))
        data_len = data[offset + 8]
        offset += 9
        if offset + data_len + 1 > len(data):
            break
        ad_data = data[offset : offset + data_len]
        rssi = struct.unpack("b", bytes([data[offset + data_len]]))[0]
        offset += data_len + 1
        reports.append({"address": addr, "ad_data": ad_data, "rssi": rssi})
    return reports


def _print_raw_adv_report(report: dict) -> None:
    """Display a raw advertising report with all AD structures and BThome decode."""
    ad_structs = _ad_parse(report["ad_data"])

    local_name: str | None = None
    for _, t, v in ad_structs:
        if t in (0x08, 0x09) and v:
            local_name = v.decode("utf-8", errors="replace")
            break

    if DEVICE_NAME_FILTER and (
        local_name is None or DEVICE_NAME_FILTER not in local_name
    ):
        return

    rssi = report["rssi"]
    rssi_color = (
        Colors.GREEN if rssi > -70 else (Colors.YELLOW if rssi > -85 else Colors.RED)
    )

    print_separator()
    print(
        f"{Colors.GRAY}[{format_timestamp()}]{Colors.RESET} "
        f"{Colors.BOLD}{Colors.GREEN}📱 {local_name or report['address']}{Colors.RESET} "
        f"({Colors.GRAY}{report['address']}{Colors.RESET})"
    )
    print(f"  {Colors.GRAY}RSSI:{Colors.RESET} {rssi_color}{rssi} dBm{Colors.RESET}")

    print(f"  {Colors.GRAY}AD Structures:{Colors.RESET}")
    for length, ad_type, value in ad_structs:
        type_name = _AD_TYPE_NAMES.get(ad_type, f"Unknown (0x{ad_type:02X})")
        hex_val = " ".join(f"{b:02X}" for b in value)
        decoded = _ad_decode(ad_type, value)
        decoded_part = f"  {Colors.GRAY}→ {decoded}{Colors.RESET}" if decoded else ""
        print(
            f"    {Colors.CYAN}LEN=0x{length:02X}  TYPE=0x{ad_type:02X}  "
            f"{Colors.GRAY}[{type_name}]{Colors.RESET}\n"
            f"      VALUE= {Colors.YELLOW}{hex_val}{Colors.RESET}{decoded_part}"
        )

    # BThome decode from Service Data
    for _, ad_type, value in ad_structs:
        if ad_type != 0x16 or len(value) < 3:
            continue
        uuid = value[0] | (value[1] << 8)
        if uuid != BTHOME_COMPANY_ID:
            continue
        parsed = parse_bthome_packet(value[2:])
        if not parsed:
            continue
        enc_str = (
            f"{Colors.RED}encrypted{Colors.RESET}"
            if parsed["encrypted"]
            else f"{Colors.GREEN}unencrypted{Colors.RESET}"
        )
        print(f"  {Colors.GRAY}BThome:{Colors.RESET} {parsed['version']} ({enc_str})")
        if parsed["values"]:
            print(f"  {Colors.GRAY}Values:{Colors.RESET}")
            for val in parsed["values"]:
                if "formatted_value" in val:
                    value_str = val["formatted_value"]
                elif val["unit"]:
                    value_str = f"{val['value']:.2f} {val['unit']}"
                else:
                    value_str = f"{val['value']}"
                raw_val = val["raw_value"]
                if raw_val is None:
                    hex_str = ""
                else:
                    od = BTHOME_OBJECTS.get(val["object_id"], {})
                    sz = od.get("size", 1)
                    signed = od.get("signed", False)
                    hex_str = (
                        " ["
                        + raw_val.to_bytes(sz, byteorder="little", signed=signed)
                        .hex()
                        .upper()
                        + "]"
                    )
                print(
                    f"    {Colors.BOLD}{Colors.MAGENTA}• {val['name']} "
                    f"(0x{val['object_id']:02X}){Colors.RESET}: "
                    f"{Colors.YELLOW}{value_str}{Colors.GRAY}{hex_str}{Colors.RESET}"
                )
        break

    print()


def list_hci_adapters() -> None:
    """Print all available HCI adapters via HCIGETDEVLIST/HCIGETDEVINFO ioctls."""
    import fcntl

    # ioctl numbers (Linux/amd64 & arm; same values everywhere)
    HCIGETDEVLIST = 0x800448D2
    HCIGETDEVINFO = 0x800448D3
    HCI_MAX_DEV = 16

    # struct hci_dev_list_req: u16 dev_num + HCI_MAX_DEV * hci_dev_req (u16+u32)
    req = bytearray(2 + HCI_MAX_DEV * 6)
    struct.pack_into("<H", req, 0, HCI_MAX_DEV)

    try:
        sock = socket.socket(_AF_BLUETOOTH, socket.SOCK_RAW, _BTPROTO_HCI)
    except OSError as exc:
        print(f"{Colors.RED}✗ Cannot open HCI socket: {exc}{Colors.RESET}")
        return

    try:
        fcntl.ioctl(sock.fileno(), HCIGETDEVLIST, req)
    except OSError as exc:
        print(f"{Colors.RED}✗ HCIGETDEVLIST failed: {exc}{Colors.RESET}")
        sock.close()
        return

    num_devs = struct.unpack_from("<H", req, 0)[0]
    if num_devs == 0:
        print(f"{Colors.YELLOW}No HCI adapters found.{Colors.RESET}")
        sock.close()
        return

    print(f"{Colors.BOLD}Available HCI adapters:{Colors.RESET}")
    for i in range(num_devs):
        dev_id = struct.unpack_from("<H", req, 2 + i * 6)[0]

        # struct hci_dev_info (272 bytes):
        #   u16 dev_id, char name[8], bdaddr[6], flags u32, type u8, ...
        info = bytearray(272)
        struct.pack_into("<H", info, 0, dev_id)
        try:
            fcntl.ioctl(sock.fileno(), HCIGETDEVINFO, info)
        except OSError:
            continue

        name_bytes = info[2:10]
        dev_name = name_bytes.split(b"\x00")[0].decode("ascii", errors="replace")
        addr_bytes = info[10:16]
        address = ":".join(f"{b:02X}" for b in reversed(addr_bytes))
        flags = struct.unpack_from("<I", info, 16)[0]
        dev_type_raw = info[20]
        bus = dev_type_raw & 0x0F
        _BUS = {
            0: "VIRTUAL",
            1: "USB",
            2: "PCCARD",
            3: "UART",
            4: "RS232",
            5: "PCI",
            6: "SDIO",
            7: "SPI",
            8: "I2C",
            9: "SMD",
            10: "VIRTIO",
        }
        bus_str = _BUS.get(bus, f"0x{bus:02X}")
        up = bool(flags & (1 << 1))
        state = (
            f"{Colors.GREEN}UP{Colors.RESET}"
            if up
            else f"{Colors.GRAY}DOWN{Colors.RESET}"
        )

        print(
            f"  {Colors.BOLD}{Colors.GREEN}{dev_name}{Colors.RESET}"
            f"  index={Colors.CYAN}{dev_id}{Colors.RESET}"
            f"  addr={Colors.YELLOW}{address}{Colors.RESET}"
            f"  bus={bus_str}"
            f"  state={state}"
        )

    sock.close()


def _build_caps_hint() -> str:
    """Return a user-friendly setcap hint with the correct interpreter path and install context."""
    import pathlib

    exe = pathlib.Path(sys.executable)
    real = exe.resolve()
    real_str = str(real)
    exe_str = str(exe)

    # Detect install method.
    # Use the RESOLVED path for uv/pipx (their tool envs survive resolve()),
    # but check the ORIGINAL exe path for .venv (uv run resolves to the bare
    # uv Python binary, losing the .venv component).
    if "/uv/tools/" in real_str:
        parts = real.parts
        tool_name = (
            parts[parts.index("tools") + 1] if "tools" in parts else "bthome-logger"
        )
        context = f"uv tool install   (tool: {tool_name})"
        upgrade_note = (
            f"  Re-run after: {Colors.GRAY}uv tool upgrade {tool_name}{Colors.RESET}"
        )
    elif "/pipx/venvs/" in real_str:
        parts = real.parts
        tool_name = (
            parts[parts.index("venvs") + 1] if "venvs" in parts else "bthome-logger"
        )
        context = f"pipx              (tool: {tool_name})"
        upgrade_note = (
            f"  Re-run after: {Colors.GRAY}pipx upgrade {tool_name}{Colors.RESET}"
        )
    elif "/.venv/" in exe_str or "/venv/" in exe_str:
        context = "uv run / venv     (development)"
        upgrade_note = (
            f"  Re-run after: {Colors.GRAY}"
            f"uv python install / venv recreation{Colors.RESET}"
        )
    elif "/uv/python/" in real_str:
        # uv run with project – sys.executable already points at the uv Python
        context = "uv run            (project venv)"
        upgrade_note = f"  Re-run after: {Colors.GRAY}uv python install{Colors.RESET}"
    else:
        context = "system / pip"
        upgrade_note = (
            f"  Re-run after: {Colors.GRAY}Python interpreter upgrades{Colors.RESET}"
        )

    return (
        f"\n  Install context: {Colors.GRAY}{context}{Colors.RESET}\n"
        f"  Fix (run once):\n"
        f"    {Colors.YELLOW}sudo setcap cap_net_raw,cap_net_admin+eip {real_str}{Colors.RESET}\n"
        f"{upgrade_note}\n"
        f"  Afterwards run without sudo as usual."
    )


async def scan_hci_raw(hci_index: int = 0) -> None:
    """Scan via raw HCI socket – shows every AD structure (requires root / CAP_NET_RAW)."""
    _caps_hint = _build_caps_hint()
    try:
        sock = socket.socket(_AF_BLUETOOTH, socket.SOCK_RAW, _BTPROTO_HCI)
    except (PermissionError, OSError) as exc:
        print(
            f"{Colors.RED}✗ Cannot open raw HCI socket: {exc}{Colors.RESET}"
            + _caps_hint
        )
        return

    # Use HCI_CHANNEL_MONITOR (4): receives a copy of all HCI traffic without
    # interfering with BlueZ.  No setsockopt(HCI_FILTER) needed – the monitor
    # channel delivers everything and we filter in Python.
    try:
        _hci_bind(sock, _HCI_DEV_NONE, channel=_HCI_CHANNEL_MONITOR)
    except OSError as exc:
        sock.close()
        print(
            f"{Colors.RED}✗ Raw HCI monitor bind failed "
            f"(errno {exc.errno}): {exc.strerror}{Colors.RESET}" + _caps_hint
        )
        return

    # Start a BleakScanner in the background to keep BlueZ's LE discovery
    # session alive.  The raw monitor socket receives a copy of all HCI
    # events that BlueZ processes, including LE advertising reports.
    bleak_scanner = BleakScanner()
    await bleak_scanner.start()

    print(
        f"{Colors.GREEN}✓ Raw HCI monitor started on hci{hci_index}"
        f" (via HCI_CHANNEL_MONITOR)...{Colors.RESET}\n"
    )

    sock.setblocking(False)
    loop = asyncio.get_event_loop()
    queue: asyncio.Queue[bytes] = asyncio.Queue()

    def _reader() -> None:
        try:
            data = sock.recv(512)
            loop.call_soon_threadsafe(queue.put_nowait, data)
        except OSError:
            pass

    loop.add_reader(sock.fileno(), _reader)

    try:
        while True:
            try:
                data = await asyncio.wait_for(queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue

            if VERBOSE:
                print(f"{Colors.GRAY}[raw] {data.hex()}{Colors.RESET}")

            # HCI monitor frame (hci_mon_hdr, 6 bytes, little-endian):
            # opcode(2) + index(2) + len(2)  → payload starts at byte 6
            # opcode 0x0003 = HCI Event packet
            if len(data) < 7:
                continue
            opcode = data[0] | (data[1] << 8)
            if opcode != 0x0003:  # only HCI Event packets
                continue
            payload = data[6:]  # skip 6-byte monitor header

            # HCI Event: event_code(1) + param_len(1) + params...
            if len(payload) < 3:
                continue
            if payload[0] != _HCI_LE_META:
                continue
            subevent = payload[2] if len(payload) >= 3 else 0
            if subevent == _LE_ADV_REPORT:
                for report in _hci_parse_adv_reports(payload[3:]):
                    _print_raw_adv_report(report)
            elif subevent == _LE_EXT_ADV_REPORT:
                for report in _hci_parse_ext_adv_reports(payload[3:]):
                    _print_raw_adv_report(report)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Stopping scanner...{Colors.RESET}")
    finally:
        loop.remove_reader(sock.fileno())
        sock.close()
        await bleak_scanner.stop()
        print(f"{Colors.GREEN}✓ Scanner stopped{Colors.RESET}\n")


app = typer.Typer(
    help="BThome v2 BLE Advertisement Logger - Scans and displays BThome devices",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
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
    raw: bool = typer.Option(
        False,
        "--raw",
        "-r",
        help="Raw HCI mode: show all AD structures (LEN/TYPE/VALUE). Requires root / CAP_NET_RAW.",
    ),
    hci_index: int = typer.Option(
        0,
        "--hci",
        "-a",
        help="HCI adapter index to use in raw mode (default: 0 → hci0)",
    ),
    list_hci: bool = typer.Option(
        False,
        "--list-hci",
        "-l",
        is_flag=True,
        help="List all available HCI adapters and exit.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        is_flag=True,
        help="Show version and exit",
    ),
    install_completion: Optional[str] = typer.Option(
        None,
        "--install-completion",
        "-i",
        is_eager=True,
        callback=install_callback,
        expose_value=False,
        help="Install shell completion (bash/zsh/fish/powershell). Auto-detects shell if omitted.",
    ),
    show_completion: Optional[str] = typer.Option(
        None,
        "--show-completion",
        "-s",
        is_eager=True,
        callback=show_callback,
        expose_value=False,
        help="Show shell completion script for the current (or given) shell.",
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

    if list_hci:
        list_hci_adapters()
        return

    global DEVICE_NAME_FILTER, VERBOSE
    DEVICE_NAME_FILTER = device_filter
    VERBOSE = verbose

    # Print header after filter is set
    print_header()

    try:
        if raw:
            asyncio.run(scan_hci_raw(hci_index))
        else:
            asyncio.run(scan_forever())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app()
