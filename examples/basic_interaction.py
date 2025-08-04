#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation
import time

def main():
    print("iPhone Mirroring Basic Interaction Demo")
    print("=" * 40)
    
    automation = iPhoneAutomation()
    
    print("Looking for iPhone Mirroring window...")
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        print("Make sure iPhone Mirroring is running and visible")
        return
    
    print("Window found and focused!")
    time.sleep(1)
    
    center_x = automation.window_bounds['width'] // 2
    center_y = automation.window_bounds['height'] // 2
    
    print("\n1. Testing native CGEvent scroll down...")
    automation.native_scroll(center_x, center_y, delta_y=-10)
    time.sleep(2)
    
    print("\n2. Testing native CGEvent scroll up...")
    automation.native_scroll(center_x, center_y, delta_y=10)
    time.sleep(2)
    
    print("\n3. Testing enhanced native horizontal scroll left...")
    automation.native_scroll(center_x, center_y, delta_x=20, repeat=3)
    time.sleep(2)
    
    print("\n4. Testing enhanced native horizontal scroll right...")
    automation.native_scroll(center_x, center_y, delta_x=-20, repeat=3)
    time.sleep(2)
    
    print("\n5. Testing enhanced horizontal scroll method left...")
    automation.enhanced_horizontal_scroll(center_x, center_y, direction='left', distance=30, smoothness=15)
    time.sleep(2)
    
    print("\n6. Testing enhanced horizontal scroll method right...")
    automation.enhanced_horizontal_scroll(center_x, center_y, direction='right', distance=30, smoothness=15)
    time.sleep(2)
    
    print("\n7. Testing continuous scroll left...")
    automation.continuous_scroll(center_x, center_y, direction='left', duration=1.5, speed=8)
    time.sleep(2)
    
    print("\n8. Testing continuous scroll right...")
    automation.continuous_scroll(center_x, center_y, direction='right', duration=1.5, speed=8)
    time.sleep(2)
    
    print("\n9. Testing continuous scroll down...")
    automation.continuous_scroll(center_x, center_y, direction='down', duration=2.0, speed=3)
    time.sleep(1)
    
    print("\n10. Testing continuous scroll up...")
    automation.continuous_scroll(center_x, center_y, direction='up', duration=2.0, speed=3)
    time.sleep(2)
    
    
    print("\nDemo completed!")
    print("\nNote: This demo performs basic interactions.")
    print("For app-specific automation, see app_automation.py")

if __name__ == "__main__":
    main()