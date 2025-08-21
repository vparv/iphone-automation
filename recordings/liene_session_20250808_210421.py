#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def liene_automation_20250808_210421():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(5.10)
    automation.click(489.0, 183.0, button='left')
    time.sleep(2.65)
    automation.click(561.0, 186.0, button='left')
    time.sleep(5.09)
    automation.click(642.0, 131.0, button='left')
    time.sleep(2.07)
    automation.click(639.0, 188.0, button='left')
    time.sleep(4.48)
    automation.press_key('cmd')
    time.sleep(0.62)
    automation.press_key('c')
    time.sleep(2.12)
    automation.press_key('cmd')
    automation.press_key('v')
    time.sleep(3.28)
    automation.press_key('cmd')
    time.sleep(0.20)
    automation.press_key('c')
    time.sleep(2.35)
    automation.press_key('cmd')
    time.sleep(0.11)
    automation.press_key('v')
    time.sleep(3.54)
    automation.press_key('cmd')
    time.sleep(0.14)
    automation.press_key('c')
    time.sleep(1.04)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    liene_automation_20250808_210421()