#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def liene_automation_20250808_203512():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(7.70)
    automation.click(168.0, 217.0, button='left')
    time.sleep(2.73)
    automation.click(167.0, 220.0, button='left')
    time.sleep(2.81)
    automation.click(454.0, 507.0, button='left')
    time.sleep(1.30)
    automation.click(583.0, 471.0, button='left')
    time.sleep(2.93)
    automation.click(165.0, 219.0, button='left')
    time.sleep(1.48)
    automation.click(456.0, 505.0, button='left')
    time.sleep(1.05)
    automation.click(588.0, 470.0, button='left')
    time.sleep(4.40)
    automation.click(168.0, 222.0, button='left')
    time.sleep(1.20)
    automation.click(465.0, 505.0, button='left')
    time.sleep(0.96)
    automation.click(569.0, 472.0, button='left')
    time.sleep(2.75)
    automation.click(166.0, 218.0, button='left')
    time.sleep(1.06)
    automation.click(483.0, 505.0, button='left')
    time.sleep(0.65)
    automation.click(583.0, 471.0, button='left')
    time.sleep(2.57)
    automation.click(169.0, 219.0, button='left')
    time.sleep(1.04)
    automation.click(490.0, 506.0, button='left')
    time.sleep(0.89)
    automation.click(567.0, 468.0, button='left')
    time.sleep(5.53)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    liene_automation_20250808_203512()