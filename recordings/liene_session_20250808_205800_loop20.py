#!/usr/bin/env python3

import sys
import os
import time
import pyautogui
import json
from typing import List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation


POSITIONS_FILE = os.path.join(os.path.dirname(__file__), "loop_click4_positions.json")


def load_positions(start_position: int = 0) -> List[Tuple[float, float]]:
    """Load per-iteration coordinates for click #4.

    The file should be a JSON array of [x, y] pairs, length >= desired loops.
    start_position: 0-based index to start from (e.g., 3 for position 4)
    """
    try:
        with open(POSITIONS_FILE, "r") as f:
            data = json.load(f)
        positions = [(float(x), float(y)) for x, y in data]
        
        # Slice positions starting from the specified position
        if start_position >= len(positions):
            print(f"⚠️ Start position {start_position} >= available positions {len(positions)}. Using position 0.")
            start_position = 0
        
        sliced_positions = positions[start_position:]
        print(f"📍 Starting from gallery position {start_position + 1} (0-based: {start_position})")
        print(f"📍 Available positions from start: {len(sliced_positions)}")
        
        return sliced_positions
    except FileNotFoundError:
        print(f"⚠️ Positions file not found: {POSITIONS_FILE}. Using default placeholder.")
        # Default to the originally recorded selection coordinate repeated
        return [(414.0, 188.0)] * 32
    except Exception as e:
        print(f"⚠️ Failed to read positions file: {e}. Using default placeholder.")
        return [(414.0, 188.0)] * 32


def _log_click(
    automation: iPhoneAutomation,
    x: float,
    y: float,
    loop_idx: int,
    click_idx: int,
    note: str = "",
    clicks: int = 1,
) -> None:
    label = f"Loop {loop_idx + 1} | Click {click_idx}"
    if note:
        label += f" ({note})"
    if clicks and clicks > 1:
        label += f" x{clicks}"
    print(f"{label}: ({x}, {y})")
    automation.click(x, y, button='left', clicks=clicks)


def run_loop(loop_count: int = 28, start_position: int = 0) -> bool:
    automation = iPhoneAutomation()
    automation.window_title = "Liene Photo HD"

    if not automation.focus_window():
        print("Error: Could not find Liene Photo HD window")
        return False

    positions = load_positions(start_position)
    if len(positions) < loop_count:
        print(f"⚠️ Provided {len(positions)} positions < loop_count {loop_count}. "
              f"The last position will be reused for remaining iterations.")

    print(f"Starting automated sequence... (looping {loop_count} times)")

    for i in range(loop_count):
        sel_x, sel_y = positions[i] if i < len(positions) else positions[-1]
        print(f"\n--- Iteration {i + 1} of {loop_count} (click#4 -> {sel_x}, {sel_y}) ---")

        # Reproduced timing and actions from liene_session_20250808_205800.py
        time.sleep(2.08)
        _log_click(automation, 393.0, 42.0, i, 1)
        _log_click(automation, 502.0, 115.0, i, 2)
        # Hold Option for 0.5s before opening the gallery (click 3)
        print("Holding Option key for 0.5s before opening gallery...")
        pyautogui.keyDown('option')
        time.sleep(0.5)
        pyautogui.keyUp('option')
        time.sleep(0.10)
        _log_click(automation, 32.0, 211.0, i, 3)
        # Inserted extra clicks after click 3
        time.sleep(0.05)
        _log_click(automation, 395.0, 130.0, i, 3, note="inserted after click 3")
        time.sleep(0.05)
        _log_click(automation, 32.0, 211.0, i, 3, note="repeat click 3")
        # Allow gallery grid to fully render before selection
        time.sleep(1.0)

        # CLICK #4: variable per iteration (image selection in gallery) — two clicks at same point with longer gap
        _log_click(automation, sel_x, sel_y, i, 4, note="gallery select 1/2")
        time.sleep(0.15)
        _log_click(automation, sel_x, sel_y, i, 4, note="gallery select 2/2")

        # Give extra time for selection to register
        time.sleep(0.5)
        # CLICK #5: Updated coordinates
        _log_click(automation, 525.0, 710.0, i, 5, note="use it button")
        time.sleep(1.0)
        _log_click(automation, 1022.0, 445.0, i, 6)
        time.sleep(0.52)
        _log_click(automation, 970.0, 447.0, i, 7)
        time.sleep(0.64)
        automation.press_key('backspace')
        time.sleep(0.14)
        automation.press_key('backspace')
        time.sleep(0.46)
        automation.press_key('1')
        time.sleep(0.42)
        automation.press_key('6')
        time.sleep(0.15)
        automation.press_key('6')
        # After typing 166, pause 1s then proceed directly to (former) click 11
        time.sleep(0.50)
        _log_click(automation, 901.0, 129.0, i, 8, note="double-click", clicks=2)
        time.sleep(0.25)
        _log_click(automation, 1015.0, 126.0, i, 9, note="double-click", clicks=2)
        time.sleep(0.725)
        _log_click(automation, 29.0, 43.0, i, 10)
        time.sleep(0.64)
        _log_click(automation, 529.0, 391.0, i, 11)
        time.sleep(0.5725)
        _log_click(automation, 378.0, 39.0, i, 12)
        time.sleep(0.5)
        automation.press_key('c')

        # Small breather to stabilize UI between iterations
        if i < loop_count - 1:
            time.sleep(0.5)

    print("Automation completed!")
    return True


if __name__ == "__main__":
    # Optional CLI: allow overriding loop count and start position
    # Usage: python script.py [loop_count] [start_position]
    # Example: python script.py 25 3  (25 loops starting from position 4, 0-based index 3)
    try:
        count = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    except ValueError:
        count = 28
    
    try:
        start_pos = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    except ValueError:
        start_pos = 0
    
    print(f"🚀 Running automation: {count} loops, starting from gallery position {start_pos + 1}")
    run_loop(loop_count=count, start_position=start_pos)


