#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def liene_workflow_20250810_014148():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(0.79)
    automation.click(1000.0, 191.0, button='left')
    time.sleep(0.68)
    automation.click(1002.0, 181.0, button='left')
    time.sleep(3.48)
    automation.click(21.0, 46.0, button='left')
    time.sleep(1.06)
    automation.click(184.0, 5.0, button='left')
    time.sleep(3.09)
    automation.click(366.0, 531.0, button='left')
    time.sleep(2.21)
    automation.click(271.0, 286.0, button='left')
    time.sleep(0.52)
    automation.click(271.0, 286.0, button='left')
    time.sleep(1.48)
    automation.click(177.0, 103.0, button='left')
    time.sleep(0.59)
    automation.click(198.0, 75.0, button='left')
    time.sleep(1.16)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    liene_workflow_20250810_014148()