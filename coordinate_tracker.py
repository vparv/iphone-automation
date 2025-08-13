#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation
import pyautogui
from pynput import mouse

class CoordinateTracker:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        self.window_bounds = None
        self.tracking = False
        
    def focus_and_get_bounds(self):
        """Focus on the app and get window bounds."""
        print("🎯 Focusing on Liene Photo HD app...")
        
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
            
        # Get window bounds
        self.window_bounds = self.automation.window_bounds
        if self.window_bounds:
            print(f"✅ Window focused and bounds captured!")
            print(f"📊 Window bounds: x={self.window_bounds['x']}, y={self.window_bounds['y']}")
            print(f"📊 Window size: width={self.window_bounds['width']}, height={self.window_bounds['height']}")
            return True
        else:
            print("❌ Could not get window bounds")
            return False
    
    def get_relative_coordinates(self, abs_x, abs_y):
        """Convert absolute coordinates to relative coordinates within the window."""
        if not self.window_bounds:
            return None, None
            
        rel_x = abs_x - self.window_bounds['x']
        rel_y = abs_y - self.window_bounds['y']
        
        return rel_x, rel_y
    
    def get_absolute_coordinates(self, rel_x, rel_y):
        """Convert relative coordinates to absolute coordinates."""
        if not self.window_bounds:
            return None, None
            
        abs_x = rel_x + self.window_bounds['x']
        abs_y = rel_y + self.window_bounds['y']
        
        return abs_x, abs_y
    
    def track_mouse_position(self):
        """Track mouse position and show relative coordinates."""
        print("\n🖱️  Mouse Position Tracker")
        print("=" * 40)
        print("Move your mouse over the Liene Photo HD window")
        print("Press Ctrl+C when you find the right position for Step 14")
        print("Current coordinates will be shown relative to the window")
        print()
        
        try:
            while True:
                # Get current mouse position
                current_x, current_y = pyautogui.position()
                
                # Convert to relative coordinates
                rel_x, rel_y = self.get_relative_coordinates(current_x, current_y)
                
                if rel_x is not None and rel_y is not None:
                    # Check if mouse is within window bounds
                    if (0 <= rel_x <= self.window_bounds['width'] and 
                        0 <= rel_y <= self.window_bounds['height']):
                        print(f"\r🎯 Mouse position: ({int(rel_x)}, {int(rel_y)}) relative to window", end="", flush=True)
                    else:
                        print(f"\r📍 Mouse outside window: ({current_x}, {current_y}) absolute", end="", flush=True)
                else:
                    print(f"\r📍 Mouse position: ({current_x}, {current_y}) absolute", end="", flush=True)
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            current_x, current_y = pyautogui.position()
            rel_x, rel_y = self.get_relative_coordinates(current_x, current_y)
            
            print(f"\n\n🎯 Final Position Captured!")
            print(f"📍 Absolute coordinates: ({current_x}, {current_y})")
            if rel_x is not None and rel_y is not None:
                print(f"📍 Relative coordinates: ({int(rel_x)}, {int(rel_y)})")
                
                # Check if within window
                if (0 <= rel_x <= self.window_bounds['width'] and 
                    0 <= rel_y <= self.window_bounds['height']):
                    print(f"✅ Position is within the Liene Photo HD window!")
                    return int(rel_x), int(rel_y)
                else:
                    print(f"⚠️  Position is outside the window bounds")
                    return current_x, current_y
            else:
                return current_x, current_y
    
    def click_at_tracked_position(self, x, y):
        """Click at the tracked position to test it."""
        print(f"\n🖱️  Testing click at position ({x}, {y})")
        
        try:
            # Convert relative to absolute if needed
            if self.window_bounds:
                abs_x, abs_y = self.get_absolute_coordinates(x, y)
                if abs_x and abs_y:
                    print(f"🎯 Clicking at absolute coordinates: ({abs_x}, {abs_y})")
                    self.automation.click(abs_x, abs_y)
                else:
                    print(f"🎯 Clicking at coordinates: ({x}, {y})")
                    self.automation.click(x, y)
            else:
                print(f"🎯 Clicking at coordinates: ({x}, {y})")
                self.automation.click(x, y)
                
            print("✅ Test click executed!")
            
        except Exception as e:
            print(f"❌ Error clicking: {e}")

def main():
    tracker = CoordinateTracker()
    
    print("🎯 Coordinate Tracker for Step 14")
    print("=" * 40)
    print("This will help you find the exact coordinates for Step 14")
    
    # Focus on the app first
    if not tracker.focus_and_get_bounds():
        return
    
    print("\n🖱️  Ready to track mouse coordinates!")
    input("Press Enter to start tracking...")
    
    # Track mouse position
    x, y = tracker.track_mouse_position()
    
    if x is not None and y is not None:
        print(f"\n📋 Suggested coordinates for Step 14: ({x}, {y})")
        
        # Ask if user wants to test the click
        test = input("\nDo you want to test this position? (y/n): ").lower().strip()
        if test == 'y':
            tracker.click_at_tracked_position(x, y)
        
        print(f"\n🔧 To update Step 14, use these coordinates:")
        print(f"   x: {x}")
        print(f"   y: {y}")

if __name__ == "__main__":
    main()
