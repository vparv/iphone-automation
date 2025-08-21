#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def liene_automation_20250808_203655():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(7.57)
    automation.click(156.0, 170.0, button='left')
    time.sleep(3.69)
    automation.click(157.0, 170.0, button='left')
    time.sleep(2.18)
    automation.click(540.0, 556.0, button='left')
    time.sleep(1.64)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    liene_automation_20250808_203655()