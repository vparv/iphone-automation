#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def recorded_session_20250812_211057():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(1.83)
    automation.click(192.0, 316.98046875, button='left')
    time.sleep(1.64)
    automation.click(195.0, 314.98046875, button='left')
    time.sleep(2.49)
    automation.click(109.0, 937.98046875, button='left')
    time.sleep(1.38)
    automation.click(313.0, 589.98046875, button='left')
    time.sleep(5.47)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    recorded_session_20250812_211057()