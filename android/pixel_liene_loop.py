#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
import time
from typing import List, Tuple, Optional


def adb(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["adb", *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=check)


def adb_shell(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return adb("shell", *args, check=check)


def tap(x: int, y: int) -> None:
    print(f"tap: ({x}, {y})")
    adb_shell("input", "tap", str(x), str(y))


def swipe(x1: int, y1: int, x2: int, y2: int, ms: int = 300) -> None:
    print(f"swipe: ({x1}, {y1}) -> ({x2}, {y2}) in {ms}ms")
    adb_shell("input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms))


def text(s: str) -> None:
    # Escape spaces for adb input text
    s_escaped = s.replace(" ", "%s")
    print(f"text: '{s}'")
    adb_shell("input", "text", s_escaped)


def keyevent(code: int) -> None:
    print(f"keyevent: {code}")
    adb_shell("input", "keyevent", str(code))


def ensure_device() -> None:
    out = adb("devices").stdout.strip()
    lines = [ln for ln in out.splitlines() if "\t" in ln]
    if not lines:
        print("No devices attached. Run 'adb devices' and connect your Pixel.")
        sys.exit(1)
    serial, status = lines[0].split("\t", 1)
    if status != "device":
        print(f"Device status is '{status}'. Authorize device and retry.")
        sys.exit(1)


def load_positions(path: str, expected: int) -> List[Tuple[int, int]]:
    try:
        with open(path, "r") as f:
            arr = json.load(f)
        positions = [(int(p[0]), int(p[1])) for p in arr]
        if len(positions) < expected:
            print(f"Warning: only {len(positions)} positions provided, reusing last for remaining loops")
            last = positions[-1] if positions else (0, 0)
            positions = positions + [last] * (expected - len(positions))
        return positions
    except FileNotFoundError:
        print(f"Positions file not found: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to load positions: {e}")
        sys.exit(1)


def maybe_tap(pt: Optional[Tuple[int, int]], label: str, delay_s: float = 0.0) -> None:
    if pt is None:
        print(f"skip: {label}")
        return
    if delay_s > 0:
        time.sleep(delay_s)
    print(label)
    tap(pt[0], pt[1])


def main() -> None:
    parser = argparse.ArgumentParser(description="ADB-driven Liene Photo automation on Android")
    parser.add_argument("--loops", type=int, default=32, help="Number of iterations (default: 32)")
    parser.add_argument("--positions", default=os.path.join(os.path.dirname(__file__), "positions_32.json"), help="JSON file with 32 [x,y] pairs used for image selection per loop")
    parser.add_argument("--package", default=None, help="App package to launch (optional)")
    parser.add_argument("--activity", default=None, help="Activity to launch (optional)")
    parser.add_argument("--pointer", action="store_true", help="Enable on-device pointer overlay for debugging")
    args = parser.parse_args()

    ensure_device()

    if args.pointer:
        adb_shell("settings", "put", "system", "pointer_location", "1")

    if args.package and args.activity:
        print(f"Launching {args.package}/{args.activity} via am start...")
        adb_shell("am", "start", "-n", f"{args.package}/{args.activity}")
        time.sleep(1.5)
    elif args.package:
        print(f"Launching {args.package} via monkey...")
        adb_shell("monkey", "-p", args.package, "-c", "android.intent.category.LAUNCHER", "1")
        time.sleep(1.5)

    # Configure known step coordinates here (fill in from pointer overlay)
    # Set to None to skip a step.
    coords = {
        "canvas": None,      # e.g., (x, y)
        "upload": None,      # e.g., (x, y)
        "use_it": None,      # e.g., (x, y)
        "next": None,        # e.g., (x, y)
        "size_input": None,  # e.g., (x, y)
        "confirm1": None,    # e.g., (x, y)
        "confirm2": None,    # e.g., (x, y)
        "back": None,        # e.g., (x, y)
    }

    positions = load_positions(args.positions, args.loops)

    print(f"Starting automation for {args.loops} loops…")
    for i in range(args.loops):
        print(f"\n=== Loop {i+1}/{args.loops} ===")

        # Navigate to gallery (fill in coords to enable these)
        maybe_tap(coords.get("canvas"),   "tap: canvas/+", 0.5)
        maybe_tap(coords.get("upload"),   "tap: upload",   1.0)

        # Select image for this loop
        sel_x, sel_y = positions[i]
        print(f"tap: image selection ({sel_x}, {sel_y})")
        tap(sel_x, sel_y)
        time.sleep(1.5)

        # Proceed workflow (fill in coords to enable these)
        maybe_tap(coords.get("use_it"),      "tap: Use it",      2.0)
        maybe_tap(coords.get("next"),        "tap: Next",        1.0)
        maybe_tap(coords.get("size_input"),  "tap: size input",  0.5)

        # Enter 166 if size_input was tapped
        if coords.get("size_input") is not None:
            text("166")
            keyevent(66)  # ENTER
            time.sleep(1.0)

        maybe_tap(coords.get("confirm1"), "tap: confirm 1", 0.5)
        maybe_tap(coords.get("confirm2"), "tap: confirm 2", 1.0)
        maybe_tap(coords.get("back"),     "tap: back",      1.0)

        # Small breather between loops
        time.sleep(0.5)

    print("Automation completed.")

    if args.pointer:
        adb_shell("settings", "put", "system", "pointer_location", "0")


if __name__ == "__main__":
    main()


