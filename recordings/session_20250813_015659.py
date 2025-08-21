#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def recorded_session_20250813_015659():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(19.19)
    automation.click(248.0, 542.0, button='left')
    time.sleep(1.55)
    automation.click(246.0, 542.0, button='left')
    time.sleep(14.62)
    automation.click(245.0, 542.0, button='left')
    time.sleep(12.34)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    recorded_session_20250813_015659()