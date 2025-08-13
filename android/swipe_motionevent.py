#!/usr/bin/env python3

import subprocess
import sys
import re
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


def screen_size() -> Tuple[int, int]:
    out = adb("shell", "wm", "size").stdout
    m = re.search(r"(\d+)x(\d+)", out)
    if not m:
        print("Could not determine screen size")
        sys.exit(1)
    return int(m.group(1)), int(m.group(2))


def motionevent(action: str, x: int, y: int) -> None:
    # Actions: DOWN, MOVE, UP
    adb("shell", "input", "motionevent", action.upper(), str(x), str(y))


def swipe_motionevent(y: int, duration_ms: int = 450, start_ratio: float = 0.9, end_ratio: float = 0.1, steps: int = 16) -> None:
    w, h = screen_size()
    y = max(1, min(h - 2, y))
    x1 = int(w * start_ratio)
    x2 = int(w * end_ratio)
    dt = max(1, duration_ms // max(1, steps)) / 1000.0

    print(f"motionevent swipe: ({x1},{y}) -> ({x2},{y}) in ~{duration_ms}ms, steps={steps}")

    # Press, move in steps, release
    motionevent("DOWN", x1, y)
    time.sleep(0.04)
    for i in range(1, steps):
        x = x1 + (x2 - x1) * i // steps
        motionevent("MOVE", int(x), y)
        time.sleep(dt)
    motionevent("UP", x2, y)


def main() -> None:
    # Usage: python3 swipe_motionevent.py [y=2230] [duration_ms=450]
    y = 2230
    duration_ms = 450
    if len(sys.argv) >= 2:
        y = int(float(sys.argv[1]))
    if len(sys.argv) >= 3:
        duration_ms = int(float(sys.argv[2]))

    ensure_device()
    swipe_motionevent(y=y, duration_ms=duration_ms)
    print("Done.")


if __name__ == "__main__":
    main()


