#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def recorded_session_20250813_014453():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(2.38)
    automation.click(210.36328125, 214.38671875, button='left')
    time.sleep(0.91)
    automation.click(210.36328125, 214.38671875, button='left')
    time.sleep(2.06)
    automation.click(214.36328125, 888.38671875, button='left')
    time.sleep(5.08)
    automation.click(32.36328125, 116.38671875, button='left')
    time.sleep(0.89)
    automation.click(32.36328125, 116.38671875, button='left')
    time.sleep(2.86)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    recorded_session_20250813_014453()