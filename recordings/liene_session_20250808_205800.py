#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def liene_automation_20250808_205800():
    """Generated automation script"""
    automation = iPhoneAutomation()
    
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return False
    
    print("Starting automated sequence...")
    
    time.sleep(4.16)
    automation.click(393.0, 42.0, button='left')
    time.sleep(0.87)
    automation.click(502.0, 115.0, button='left')
    time.sleep(1.63)
    automation.click(32.0, 211.0, button='left')
    time.sleep(2.89)
    automation.click(414.0, 188.0, button='left')
    time.sleep(3.35)
    automation.click(530.0, 645.0, button='left')
    time.sleep(11.23)
    automation.click(527.0, 711.0, button='left')
    time.sleep(3.12)
    automation.click(1022.0, 445.0, button='left')
    time.sleep(1.04)
    automation.click(977.0, 447.0, button='left')
    time.sleep(1.28)
    automation.press_key('backspace')
    time.sleep(0.14)
    automation.press_key('backspace')
    time.sleep(0.46)
    automation.press_key('1')
    time.sleep(0.42)
    automation.press_key('6')
    time.sleep(0.15)
    automation.press_key('6')
    time.sleep(2.34)
    automation.click(636.0, 218.0, button='left')
    time.sleep(1.33)
    automation.click(496.0, 456.0, button='left')
    time.sleep(2.10)
    automation.click(901.0, 129.0, button='left')
    time.sleep(0.99)
    automation.click(1015.0, 126.0, button='left')
    time.sleep(2.90)
    automation.click(29.0, 43.0, button='left')
    time.sleep(2.56)
    automation.click(529.0, 391.0, button='left')
    time.sleep(4.58)
    automation.click(378.0, 39.0, button='left')
    time.sleep(1.91)
    automation.press_key('c')
    
    print("Automation completed!")
    return True

if __name__ == "__main__":
    liene_automation_20250808_205800()