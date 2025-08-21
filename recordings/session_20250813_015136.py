#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def recorded_session_20250813_015136():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(6.48)
    automation.click(215.0, 219.0, button='left')
    time.sleep(0.68)
    automation.click(213.0, 206.0, button='left')
    time.sleep(3.97)
    automation.click(214.0, 870.0, button='left')
    time.sleep(2.83)
    automation.click(59.0, 194.0, button='left')
    time.sleep(2.03)
    automation.click(349.0, 893.0, button='left')
    time.sleep(2.59)
    automation.click(247.0, 540.0, button='left')
    time.sleep(5.55)
    automation.click(192.0, 399.0, button='left')
    time.sleep(21.91)
    automation.click(406.0, 297.0, button='left')
    time.sleep(1.14)
    automation.click(372.0, 114.0, button='left')
    time.sleep(30.17)
    automation.click(282.0, 892.0, button='left')
    time.sleep(14.35)
    automation.click(331.0, 888.0, button='left')
    time.sleep(6.19)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    recorded_session_20250813_015136()