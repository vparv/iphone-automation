#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def liene_automation_20250808_210953():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(4.87)
    automation.click(414.0, 253.0, button='left')
    time.sleep(4.29)
    automation.click(487.0, 255.0, button='left')
    time.sleep(3.67)
    automation.press_key('cmd')
    time.sleep(0.17)
    automation.press_key('c')
    time.sleep(0.57)
    automation.press_key('c')
    time.sleep(0.22)
    automation.press_key('c')
    time.sleep(1.23)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    liene_automation_20250808_210953()