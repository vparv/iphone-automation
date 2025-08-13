#!/usr/bin/env python3

import subprocess
import sys
import re
import time
from typing import List


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


def screen_size() -> tuple[int, int]:
    out = adb("shell", "wm", "size").stdout
    m = re.search(r"(\d+)x(\d+)", out)
    if not m:
        print("Could not determine screen size")
        sys.exit(1)
    return int(m.group(1)), int(m.group(2))


def swipe(x1: int, y1: int, x2: int, y2: int, ms: int = 450) -> None:
    print(f"swipe: ({x1}, {y1}) -> ({x2}, {y2}) in {ms}ms (input swipe)")
    adb("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms))


def swipe_cmd(x1: int, y1: int, x2: int, y2: int, ms: int = 450) -> None:
    print(f"swipe: ({x1}, {y1}) -> ({x2}, {y2}) in {ms}ms (cmd input swipe)")
    adb("shell", "cmd", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms))


def main() -> None:
    # Defaults: y=2230, duration=450ms, margin 10% from edges
    y = 2230
    duration_ms = 450
    scan = True  # try multiple offsets/durations for reliability
    if len(sys.argv) >= 2:
        y = int(float(sys.argv[1]))
    if len(sys.argv) >= 3:
        duration_ms = int(float(sys.argv[2]))
    if len(sys.argv) >= 4:
        scan = sys.argv[3].lower() not in ["0", "false", "no"]

    ensure_device()
    w, h = screen_size()

    y = max(1, min(h - 2, y))
    start_x = int(w * 0.88)
    end_x = int(w * 0.12)

    print(f"Screen: {w}x{h}; base y={y}")

    if not scan:
        swipe(start_x, y, end_x, y, ms=duration_ms)
        time.sleep(0.2)
        swipe_cmd(start_x, y, end_x, y, ms=duration_ms)
        print("Done.")
        return

    # Scan a few nearby Y positions and durations; try both input variants
    y_candidates: List[int] = [y, max(1, y - 60), max(1, y - 120)]
    dur_candidates: List[int] = [duration_ms, max(200, duration_ms * 2), 800]

    for yi in y_candidates:
        print(f"\n-- Trying y={yi} --")
        for d in dur_candidates:
            try:
                swipe(start_x, yi, end_x, yi, ms=d)
                time.sleep(0.25)
            except subprocess.CalledProcessError as e:
                print(f"input swipe failed: {e}")
            try:
                swipe_cmd(start_x, yi, end_x, yi, ms=d)
                time.sleep(0.25)
            except subprocess.CalledProcessError as e:
                print(f"cmd input swipe failed: {e}")

    print("\nScan complete.")


if __name__ == "__main__":
    main()


