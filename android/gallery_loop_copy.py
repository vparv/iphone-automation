#!/usr/bin/env python3

import json
import os
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


def tap_retry(x: int, y: int, attempts: int = 4, gap_s: float = 0.25) -> None:
    """Tap gallery item with small offsets to avoid hitting stale hotspot overlays."""
    offsets = [(0, 0), (6, 0), (-6, 0), (0, 6), (0, -6)]
    for i in range(min(attempts, len(offsets))):
        dx, dy = offsets[i]
        x2, y2 = x + dx, y + dy
        print(f"tap-retry {i+1}: ({x2},{y2})")
        # light press with slightly longer dwell
        motionevent("DOWN", x2, y2)
        time.sleep(0.10)
        motionevent("UP", x2, y2)
        time.sleep(gap_s)


def load_positions(path: str) -> List[Tuple[int, int]]:
    with open(path, "r") as f:
        arr = json.load(f)
    return [(int(p[0]), int(p[1])) for p in arr]


def main() -> None:
    # Config
    default_pause = 0.75
    between_loops_pause = 2.0  # extra stabilization time before next loop starts
    # Toggle this to insert extra taps after drags and end the loop early
    optional_post_drag_enabled = False
    # Use explicit gallery coordinates provided (4 columns x 5 rows = 20 positions)
    x_values = [170, 400, 630, 940]
    y_values = [360, 620, 880, 1140, 1400]
    positions: List[Tuple[int, int]] = [(x, y) for y in y_values for x in x_values]

    # Optional CLI:
    #   arg1: starting loop index (1-based). Example: python3 gallery_loop.py 2
    #   arg2: count of loops to run. Example: python3 gallery_loop.py 5 1  (run only loop 5)
    start_index = 1
    loop_count = 25  # Set to 25 loops
    if len(sys.argv) >= 2:
        try:
            start_index = max(1, int(sys.argv[1]))
        except ValueError:
            start_index = 1
    if len(sys.argv) >= 3:
        try:
            loop_count = max(1, int(sys.argv[2]))
        except ValueError:
            loop_count = None

    ensure_device()

    print(f"Starting gallery run… (start={start_index}, total={len(positions)}, count={loop_count or 'all'})")
    if loop_count is None:
        pos_slice = positions[start_index - 1:]
    else:
        end_index = (start_index - 1) + loop_count
        pos_slice = positions[start_index - 1:end_index]
    for idx, (gx, gy) in enumerate(pos_slice, start=start_index):
        print(f"\n=== Loop {idx}/{len(positions)} ===")

        # Open gallery flow: Steps 1-2 fixed; Step 3 selects gallery item; Step 4 fixed
        print("Step 1: tap 500,450")
        tap(500, 450)
        time.sleep(default_pause)

        print("Step 2: tap 518,2276")
        tap(518, 2276)
        time.sleep(default_pause)

        # Select image for this loop (Step 3)
        print(f"Step 3: gallery select {gx},{gy}")
        tap_retry(gx, gy, attempts=2, gap_s=0.15)
        time.sleep(default_pause)

        print("Step 4: tap 640,2222")
        tap(640, 2222)
        time.sleep(1.0)

        # Drag sequence
        print("Drag 1…")
        drag(600, 1350, 775, 2010, duration_ms=500)
        time.sleep(0.25)
        print("Drag 2…")
        drag(480, 960, 230, 390, duration_ms=500)
        time.sleep(default_pause)

        # Optional post-drag sequence; if enabled, this ends the loop early
        if optional_post_drag_enabled:
            print("Optional post-drag: tap 920,200")
            tap(920, 200)
            time.sleep(3.0)
            print("Optional post-drag: tap 680,220")
            tap(680, 220)
            time.sleep(3.0)
            print("Optional post-drag: tap 800,2150")
            tap(800, 2150)
            # End of loop per request with special handling for first loop
            if idx == 1:
                time.sleep(20.0)
                continue
            else:
                # Pre-final-click settle
                time.sleep(2.0)
                print("Optional post-drag final: tap 550,1400")
                tap(550, 1400)
                # Ensure 2s between loops
                time.sleep(2.0)
                continue

        # Final taps
        tap(70, 190)
        time.sleep(default_pause)
        tap(630, 1780)
        time.sleep(default_pause)

        # Inter-loop stabilization pause
        time.sleep(between_loops_pause)

    print("\nAll loops completed.")


if __name__ == "__main__":
    main()
