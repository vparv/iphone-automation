#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def liene_automation_20250808_205533():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(2.37)
    automation.click(380.984375, 42.0, button='left')
    time.sleep(2.77)
    automation.click(530.984375, 120.0, button='left')
    time.sleep(4.25)
    automation.click(37.984375, 216.0, button='left')
    time.sleep(3.56)
    automation.click(411.984375, 187.0, button='left')
    time.sleep(2.20)
    automation.click(527.984375, 646.0, button='left')
    time.sleep(9.82)
    automation.click(525.984375, 716.0, button='left')
    time.sleep(3.35)
    automation.click(1021.984375, 448.0, button='left')
    time.sleep(1.54)
    automation.click(973.984375, 448.0, button='left')
    time.sleep(1.41)
    automation.press_key('backspace')
    time.sleep(0.39)
    automation.press_key('backspace')
    time.sleep(0.53)
    automation.press_key('1')
    time.sleep(0.30)
    automation.press_key('6')
    time.sleep(0.17)
    automation.press_key('6')
    time.sleep(4.52)
    automation.click(643.984375, 389.0, button='left')
    time.sleep(2.00)
    automation.click(491.984375, 489.0, button='left')
    time.sleep(3.62)
    automation.click(904.984375, 125.0, button='left')
    time.sleep(1.57)
    automation.click(1020.984375, 129.0, button='left')
    time.sleep(3.85)
    automation.click(25.984375, 49.0, button='left')
    automation.click(25.984375, 49.0, button='left')
    time.sleep(1.80)
    automation.click(26.984375, 50.0, button='left')
    time.sleep(2.27)
    automation.click(529.984375, 391.0, button='left')
    time.sleep(6.48)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    liene_automation_20250808_205533()