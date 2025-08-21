#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def liene_automation_20250808_205407():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(3.35)
    automation.click(362.984375, 44.0, button='left')
    time.sleep(2.41)
    automation.click(527.984375, 120.0, button='left')
    time.sleep(1.89)
    automation.click(39.984375, 206.0, button='left')
    time.sleep(2.66)
    automation.click(417.984375, 182.0, button='left')
    time.sleep(2.78)
    automation.click(528.984375, 648.0, button='left')
    time.sleep(10.81)
    automation.click(526.984375, 711.0, button='left')
    time.sleep(2.66)
    automation.click(972.984375, 446.0, button='left')
    time.sleep(1.17)
    automation.press_key('backspace')
    time.sleep(0.14)
    automation.press_key('backspace')
    time.sleep(0.44)
    automation.press_key('1')
    time.sleep(0.37)
    automation.press_key('6')
    time.sleep(0.15)
    automation.press_key('6')
    time.sleep(3.36)
    automation.click(1023.984375, 448.0, button='left')
    time.sleep(1.37)
    automation.press_key('cmd')
    automation.press_key('z')
    time.sleep(1.47)
    automation.press_key('shift')
    time.sleep(0.50)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    liene_automation_20250808_205407()