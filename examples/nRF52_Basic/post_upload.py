"""
post_upload.py – PlatformIO extra_script (pre+post:upload)

PRE-upload  : Always restores the full BLE stack (MBR + SoftDevice S140 + Adafruit
              Bootloader + UICR) from the merged bootloader HEX that ships with the
              framework package.  JLink only erases/programs sectors that differ, so
              if the stack is already intact this adds only a few seconds for verify.

POST-upload : PIO's JLink upload script ends with 'r' (reset+halt) + 'q' without 'g'.
              This sends 'g' so the CPU actually runs after every upload.

Both hooks are only active when upload_protocol = jlink.
"""

import glob
import os
import subprocess
import tempfile

Import("env")  # noqa: F821


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _jlink_run(commands):
    """Write a JLink command file, run JLinkExe, return CompletedProcess."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jlink", delete=False) as f:
        f.write("\n".join(commands) + "\n")
        tmpfile = f.name
    try:
        return subprocess.run(
            [
                "JLinkExe",
                "-device",
                "nRF52840_xxAA",
                "-if",
                "SWD",
                "-speed",
                "4000",
                "-autoconnect",
                "1",
                "-CommandFile",
                tmpfile,
            ],
            capture_output=True,
            text=True,
        )
    finally:
        os.unlink(tmpfile)


# ---------------------------------------------------------------------------
# PRE-upload: restore full BLE stack
# ---------------------------------------------------------------------------


def jlink_restore_stack(source, target, env):
    if env.get("UPLOAD_PROTOCOL") != "jlink":
        return

    # Locate the merged bootloader HEX (MBR + SoftDevice + Bootloader + UICR)
    fw_dir = env.PioPlatform().get_package_dir("framework-arduinoadafruitnrf52")
    board_variant = env.BoardConfig().get("build.variant", "pca10056")
    bl_dir = os.path.join(fw_dir, "bootloader", board_variant)
    matches = sorted(glob.glob(os.path.join(bl_dir, "*.hex")))
    if not matches:
        print(f">> pre_upload: No bootloader HEX found in {bl_dir} – skipping restore")
        return
    bl_hex = matches[-1]  # take the newest if multiple exist

    print(">> pre_upload: Restoring MBR + SoftDevice + Bootloader + UICR")
    print(f"   HEX: {os.path.basename(bl_hex)}")
    r = _jlink_run(["h", f"loadfile {bl_hex}", "exit"])
    if r.returncode == 0:
        print(">> pre_upload: BLE stack restored OK")
    else:
        print(">> pre_upload: Restore FAILED – check JLink connection")
        print(r.stderr)


# ---------------------------------------------------------------------------
# POST-upload: release CPU from halt
# ---------------------------------------------------------------------------


def jlink_go_after_upload(source, target, env):
    if env.get("UPLOAD_PROTOCOL") != "jlink":
        return
    print(">> post_upload: sending 'g' to release CPU halt...")
    r = _jlink_run(["g", "exit"])
    if r.returncode == 0:
        print(">> post_upload: CPU released (go OK)")
    else:
        print(">> post_upload: FAILED")
        print(r.stderr)


env.AddPreAction("upload", jlink_restore_stack)  # noqa: F821
env.AddPostAction("upload", jlink_go_after_upload)  # noqa: F821
