#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def recorded_session_20250813_014823():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(2.39)
    automation.click(206.0, 211.0, button='left')
    time.sleep(0.94)
    automation.click(226.0, 220.0, button='left')
    time.sleep(2.18)
    automation.click(217.0, 876.0, button='left')
    time.sleep(6.24)
    automation.click(30.0, 112.0, button='left')
    time.sleep(1.88)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    recorded_session_20250813_014823()