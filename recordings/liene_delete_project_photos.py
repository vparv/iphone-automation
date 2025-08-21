#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation


def _log_click(automation: iPhoneAutomation, x: float, y: float, loop_idx: int, click_idx: int, note: str = "") -> None:
    label = f"Loop {loop_idx + 1} | Click {click_idx}"
    if note:
        label += f" ({note})"
    print(f"{label}: ({x}, {y})")
    automation.click(x, y, button='left')


def liene_delete_project_photos(loop_count: int = 10) -> bool:
    """Run the recorded sequence in Liene Photo HD multiple times.

    Args:
        loop_count: Number of times to repeat the recorded action sequence.
    """
    automation = iPhoneAutomation()
    automation.window_title = "Liene Photo HD"

    if not automation.focus_window():
        print("Error: Could not find Liene Photo HD window")
        return False

    print(f"Starting automated sequence... (looping {loop_count} times)")

    for i in range(loop_count):
        print(f"\n--- Iteration {i + 1} of {loop_count} ---")

        # Recorded action sequence (one pass)
        time.sleep(3.78)
        _log_click(automation, 327.0, 37.0, i, 1)
        time.sleep(3.12)
        _log_click(automation, 158.0, 169.0, i, 2)
        time.sleep(2.06)
        _log_click(automation, 464.0, 507.0, i, 3)
        time.sleep(1.48)
        _log_click(automation, 588.0, 469.0, i, 4)
        time.sleep(2.88)
        _log_click(automation, 156.0, 171.0, i, 5)
        time.sleep(1.53)
        _log_click(automation, 452.0, 507.0, i, 6)
        time.sleep(0.87)
        _log_click(automation, 571.0, 468.0, i, 7)
        time.sleep(2.50)
        _log_click(automation, 157.0, 171.0, i, 8)
        time.sleep(1.20)
        _log_click(automation, 457.0, 506.0, i, 9)
        time.sleep(0.61)
        _log_click(automation, 620.0, 469.0, i, 10)
        time.sleep(3.06)
        _log_click(automation, 155.0, 169.0, i, 11)
        time.sleep(1.18)
        _log_click(automation, 462.0, 502.0, i, 12)
        time.sleep(0.69)
        _log_click(automation, 608.0, 476.0, i, 13)
        time.sleep(2.99)
        _log_click(automation, 157.0, 169.0, i, 14)
        time.sleep(1.15)
        _log_click(automation, 463.0, 506.0, i, 15)
        time.sleep(0.99)
        _log_click(automation, 569.0, 475.0, i, 16)
        time.sleep(3.65)
        automation.press_key('c')

        # Optional brief breather between loops to allow UI to settle
        if i < loop_count - 1:
            time.sleep(0.5)

    print("Automation completed!")
    return True


if __name__ == "__main__":
    liene_delete_project_photos(loop_count=10)


