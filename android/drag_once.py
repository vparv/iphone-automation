#!/usr/bin/env python3

import subprocess
import sys
import time
from typing import Tuple


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


def motionevent(action: str, x: int, y: int) -> None:
    adb("shell", "input", "motionevent", action.upper(), str(x), str(y))


def drag(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 600, steps: int = 24) -> None:
    print(f"drag (motionevent): ({x1},{y1}) -> ({x2},{y2}) in ~{duration_ms}ms, steps={steps}")
    dt = max(1, duration_ms // max(1, steps)) / 1000.0
    motionevent("DOWN", x1, y1)
    time.sleep(0.03)
    for i in range(1, steps):
        x = x1 + (x2 - x1) * i // steps
        y = y1 + (y2 - y1) * i // steps
        motionevent("MOVE", int(x), int(y))
        time.sleep(dt)
    motionevent("UP", x2, y2)


def main() -> None:
    # Usage: python3 drag_once.py [x1 y1 x2 y2 duration_ms]
    if len(sys.argv) >= 5:
        try:
            x1 = int(float(sys.argv[1])); y1 = int(float(sys.argv[2]))
            x2 = int(float(sys.argv[3])); y2 = int(float(sys.argv[4]))
            duration_ms = int(float(sys.argv[5])) if len(sys.argv) >= 6 else 600
        except ValueError:
            print("Usage: python3 drag_once.py [x1 y1 x2 y2 duration_ms]")
            sys.exit(1)
    else:
        x1, y1, x2, y2, duration_ms = 520, 1000, 775, 2015, 600

    ensure_device()
    drag(x1, y1, x2, y2, duration_ms)
    print("Done.")


if __name__ == "__main__":
    main()


