#!/usr/bin/env python3

import subprocess
import sys
import time


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


def drag(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 800, steps: int = 24) -> None:
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
    # Sequence:
    # 1) Drag from (600,1350) -> (775,2015) over ~800ms (your working drag)
    # 2) Drag from (480,960) -> (45,400) (click-and-drag), ~700ms
    ensure_device()

    drag(600, 1350, 775, 2015, duration_ms=800)
    time.sleep(0.25)
    drag(480, 960, 45, 400, duration_ms=700)
    print("Done.")


if __name__ == "__main__":
    main()


