#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def recorded_session_20250813_014414():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(3.88)
    automation.click(309.36328125, 9.38671875, button='left')
    time.sleep(2.12)
    automation.click(205.36328125, 207.38671875, button='left')
    time.sleep(2.62)
    automation.click(210.36328125, 877.38671875, button='left')
    time.sleep(7.64)
    automation.click(56.36328125, 497.38671875, button='left')
    time.sleep(2.98)
    automation.click(308.36328125, 901.38671875, button='left')
    time.sleep(2.33)
    automation.click(243.36328125, 542.38671875, button='left')
    time.sleep(7.67)
    automation.click(196.36328125, 398.38671875, button='left')
    time.sleep(9.20)
    automation.click(387.36328125, 110.38671875, button='left')
    time.sleep(10.47)
    automation.press_key('media_volume_down')
    time.sleep(0.29)
    automation.press_key('media_volume_down')
    time.sleep(0.25)
    automation.press_key('media_volume_down')
    time.sleep(0.23)
    automation.press_key('media_volume_down')
    time.sleep(0.22)
    automation.press_key('media_volume_down')
    time.sleep(0.22)
    automation.press_key('media_volume_down')
    time.sleep(49.15)
    automation.click(210.36328125, 892.38671875, button='left')
    time.sleep(42.19)
    automation.click(349.36328125, 876.38671875, button='left')
    time.sleep(135.21)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    recorded_session_20250813_014414()