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


def main() -> None:
    # Config
    sleep_duration = 0.2
    total_iterations = 300
    
    # Sequence coordinates
    sequence = [
        (470, 670),   # Step 2, 6, 10, etc.
        (250, 2150),  # Step 3, 7, 11, etc.
        (900, 1320),  # Step 4, 8, 12, etc.
    ]

    ensure_device()

    print(f"Starting delete projects automation... (total iterations: {total_iterations})")
    
    for iteration in range(1, total_iterations + 1):
        print(f"\n=== Iteration {iteration}/{total_iterations} ===")
        
        # Step 1, 5, 9, etc. - Initial sleep
        print(f"Step {iteration * 4 - 3}: sleep {sleep_duration}s")
        time.sleep(sleep_duration)
        
        # Execute the 3-click sequence
        for step_offset, (x, y) in enumerate(sequence, start=1):
            step_number = iteration * 4 - 3 + step_offset
            print(f"Step {step_number}: click {x},{y}")
            tap(x, y)
    
    print(f"\nAll {total_iterations} iterations completed.")


if __name__ == "__main__":
    main()
