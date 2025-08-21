#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def delete_projects_liene_mac():
    """Generated automation script (2x speed)"""
    automation = iPhoneAutomation()
    automation.window_title = "Liene Photo HD"
    
    if not automation.focus_window():
        print("Error: Could not find Liene Photo HD window")
        return False
    
    print("Starting automated sequence (100 loops at 2x speed)...")
    
    for i in range(100):
        time.sleep(0.66)
        automation.click(161.98046875, 169.98046875, button='left')
        time.sleep(0.69)
        automation.click(465.98046875, 508.98046875, button='left')
        time.sleep(0.31)
        automation.click(596.98046875, 466.98046875, button='left')
        time.sleep(1.23)
        automation.press_key('c')
        
        if i < 99:
            time.sleep(0.25)
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    delete_projects_liene_mac()


