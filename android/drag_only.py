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


def drag(start: Tuple[int, int], end: Tuple[int, int], duration_ms: int = 500, steps: int = 24) -> None:
    (x1, y1), (x2, y2) = start, end
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
    ensure_device()

    # Drag 1: expand from lower-left towards lower-right (tuned to avoid overshoot)
    drag((600, 1350), (775, 2010), duration_ms=500, steps=24)
    time.sleep(0.25)

    # Drag 2: grab opposite corner and expand further
    drag((480, 960), (260, 360), duration_ms=500, steps=24)


if __name__ == "__main__":
    main()


