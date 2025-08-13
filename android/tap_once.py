#!/usr/bin/env python3

import subprocess
import sys


def adb(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["adb", *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)


def ensure_device() -> None:
    out = adb("devices").stdout.strip().splitlines()
    lines = [ln for ln in out if "\t" in ln]
    if not lines:
        print("No devices attached. Connect your Android and run again.")
        sys.exit(1)
    status = lines[0].split("\t", 1)[1]
    if status != "device":
        print(f"Device status is '{status}'. Authorize device and retry.")
        sys.exit(1)


def tap(x: int, y: int) -> None:
    print(f"tap: ({x}, {y})")
    adb("shell", "input", "tap", str(x), str(y))


def main() -> None:
    # Defaults to 535,434 but can accept CLI args: tap_once.py [x] [y]
    if len(sys.argv) >= 3:
        try:
            x = int(float(sys.argv[1]))
            y = int(float(sys.argv[2]))
        except ValueError:
            print("Usage: python3 tap_once.py [x y]")
            sys.exit(1)
    else:
        x, y = 535, 434

    ensure_device()
    tap(x, y)


if __name__ == "__main__":
    main()


