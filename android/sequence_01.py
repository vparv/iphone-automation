#!/usr/bin/env python3

import subprocess
import sys
import time
from typing import List, Tuple


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


def swipe(x1: int, y1: int, x2: int, y2: int, ms: int = 350) -> None:
    print(f"swipe: ({x1}, {y1}) -> ({x2}, {y2}) in {ms}ms")
    adb("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms))


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


def text(s: str) -> None:
    s_escaped = s.replace(" ", "%s")
    print(f"text: '{s}'")
    adb("shell", "input", "text", s_escaped)


def keyevent(code: int) -> None:
    print(f"keyevent: {code}")
    adb("shell", "input", "keyevent", str(code))


def main() -> None:
    # Default 2.0s pause can be overridden by first CLI arg
    default_pause = 2.0
    if len(sys.argv) >= 2:
        try:
            default_pause = float(sys.argv[1])
        except ValueError:
            print("Usage: python3 sequence_01.py [default_pause_seconds]")
            sys.exit(1)

    steps: List[Tuple[int, int]] = [
        (500, 450),
        (518, 2276),
        (110, 376),
        (340, 2222),
        (614, 2227),
    ]

    ensure_device()

    for i, (x, y) in enumerate(steps, 1):
        print(f"\nStep {i}/{len(steps)}")
        tap(x, y)
        if i < len(steps):
            if i == 4:
                # Custom pause after click 4 (now 10s)
                time.sleep(10.0)
            else:
                time.sleep(default_pause)

    # After the post-click-4 pause, we kept the next click (click 5) above.
    # Now perform the drag sequence and end.
    print("\nStarting drag sequence…")
    drag(600, 1350, 775, 2015, duration_ms=800)
    time.sleep(0.25)
    drag(480, 960, 45, 400, duration_ms=700)
    
    # Final taps before loop restarts
    time.sleep(default_pause)
    tap(70, 190)
    time.sleep(default_pause)
    tap(630, 1780)

    print("\nSequence completed.")


if __name__ == "__main__":
    main()


