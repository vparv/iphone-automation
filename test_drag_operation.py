#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

def test_drag_operation():
    """Test drag operation with user-provided coordinates."""
    print("🎯 iPhone Mirroring Drag Test")
    print("=" * 40)
    
    automation = iPhoneAutomation()
    
    print("Looking for iPhone Mirroring window...")
    if not automation.focus_window():
        print("❌ Error: Could not find iPhone Mirroring window")
        print("Make sure iPhone Mirroring is running and visible")
        return False
    
    print("✅ Window found and focused!")
    print(f"Window bounds: {automation.window_bounds}")
    print()
    
    # Get starting coordinates
    print("📍 Please provide the STARTING coordinates for the drag operation:")
    print("(These should be relative to the iPhone Mirroring window, not absolute screen coordinates)")
    
    while True:
        try:
            start_input = input("Start coordinates (x,y): ").strip()
            start_x, start_y = map(int, start_input.split(','))
            break
        except ValueError:
            print("Please enter coordinates in format: x,y (e.g., 100,200)")
    
    # Get ending coordinates
    print("\n📍 Please provide the ENDING coordinates for the drag operation:")
    
    while True:
        try:
            end_input = input("End coordinates (x,y): ").strip()
            end_x, end_y = map(int, end_input.split(','))
            break
        except ValueError:
            print("Please enter coordinates in format: x,y (e.g., 300,400)")
    
    # Get duration
    print("\n⏱️ How long should the drag operation take?")
    while True:
        try:
            duration_input = input("Duration in seconds (default 0.5): ").strip()
            if not duration_input:
                duration = 0.5
            else:
                duration = float(duration_input)
            break
        except ValueError:
            print("Please enter a valid number")
    
    print(f"\n🎬 Ready to perform drag operation:")
    print(f"   From: ({start_x}, {start_y})")
    print(f"   To: ({end_x}, {end_y})")
    print(f"   Duration: {duration} seconds")
    print()
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
    
    print("🚀 Performing drag operation...")
    
    # Try multiple drag methods to see which works best
    methods_to_try = [
        ("Built-in swipe() method", lambda: automation.swipe(start_x, start_y, end_x, end_y, duration)),
        ("Improved step-by-step method", lambda: improved_drag(automation, start_x, start_y, end_x, end_y, duration)),
        ("Simple manual method", lambda: simple_manual_drag(automation, start_x, start_y, end_x, end_y, duration)),
        ("Extended manual method", lambda: extended_manual_drag(automation, start_x, start_y, end_x, end_y, duration))
    ]
    
    for method_name, method_func in methods_to_try:
        print(f"\n🔄 Trying: {method_name}")
        try:
            method_func()
            print(f"✅ Drag operation completed using {method_name}")
            
            # Ask user if it worked
            while True:
                worked = input(f"\nDid the {method_name} work as expected? (y/n): ").lower().strip()
                if worked in ['y', 'yes']:
                    print(f"🎉 Success! {method_name} works for your use case.")
                    return True
                elif worked in ['n', 'no']:
                    print(f"❌ {method_name} didn't work. Trying next method...")
                    break
                else:
                    print("Please enter 'y' or 'n'")
            
        except Exception as e:
            print(f"❌ Error with {method_name}: {e}")
            continue
    
    print("❌ All drag methods failed or didn't work as expected.")
    return False


def improved_drag(automation, start_x, start_y, end_x, end_y, duration):
    """Improved drag method using step-by-step movement like Android implementation."""
    automation._ensure_focus()
    start_abs = automation._to_absolute_coords(start_x, start_y)
    end_abs = automation._to_absolute_coords(end_x, end_y)
    
    import pyautogui
    
    steps = 24  # Number of intermediate steps
    step_duration = duration / steps
    
    print(f"   - Moving to start position ({start_abs[0]}, {start_abs[1]})")
    pyautogui.moveTo(start_abs[0], start_abs[1])
    time.sleep(0.2)
    
    print("   - Mouse down")
    pyautogui.mouseDown(button='left')
    time.sleep(0.05)
    
    print(f"   - Dragging in {steps} steps over {duration}s")
    for i in range(1, steps + 1):
        # Calculate intermediate position
        progress = i / steps
        current_x = start_abs[0] + (end_abs[0] - start_abs[0]) * progress
        current_y = start_abs[1] + (end_abs[1] - start_abs[1]) * progress
        
        pyautogui.moveTo(int(current_x), int(current_y))
        time.sleep(step_duration)
    
    print("   - Mouse up")
    time.sleep(0.05)
    pyautogui.mouseUp(button='left')


def simple_manual_drag(automation, start_x, start_y, end_x, end_y, duration):
    """Simple manual drag method."""
    automation._ensure_focus()
    start_abs = automation._to_absolute_coords(start_x, start_y)
    end_abs = automation._to_absolute_coords(end_x, end_y)
    
    import pyautogui
    
    print(f"   - Moving to start position ({start_abs[0]}, {start_abs[1]})")
    pyautogui.moveTo(start_abs[0], start_abs[1])
    time.sleep(0.2)
    
    print("   - Mouse down")
    pyautogui.mouseDown(button='left')
    time.sleep(0.1)
    
    print(f"   - Dragging to ({end_abs[0]}, {end_abs[1]}) over {duration}s")
    pyautogui.moveTo(end_abs[0], end_abs[1], duration=duration)
    
    print("   - Mouse up")
    time.sleep(0.1)
    pyautogui.mouseUp(button='left')


def extended_manual_drag(automation, start_x, start_y, end_x, end_y, duration):
    """Extended manual drag with longer pauses and focus checks."""
    automation._ensure_focus()
    start_abs = automation._to_absolute_coords(start_x, start_y)
    end_abs = automation._to_absolute_coords(end_x, end_y)
    
    import pyautogui
    
    print(f"   - Moving to start position ({start_abs[0]}, {start_abs[1]})")
    pyautogui.moveTo(start_abs[0], start_abs[1])
    time.sleep(0.5)  # Longer pause
    
    print("   - Re-ensuring focus")
    automation._ensure_focus()
    time.sleep(0.2)
    
    print("   - Mouse down")
    pyautogui.mouseDown(start_abs[0], start_abs[1], button='left')
    time.sleep(0.3)  # Longer pause to ensure registration
    
    print(f"   - Dragging to ({end_abs[0]}, {end_abs[1]}) over {duration}s")
    pyautogui.moveTo(end_abs[0], end_abs[1], duration=duration)
    
    print("   - Final pause before mouse up")
    time.sleep(0.2)
    
    print("   - Mouse up")
    pyautogui.mouseUp(button='left')
    
    print("\n🎉 Drag test completed!")
    
    # Ask if user wants to test again with different coordinates
    while True:
        again = input("\nWould you like to test again with different coordinates? (y/n): ").lower().strip()
        if again in ['y', 'yes']:
            print("\n" + "="*40)
            return test_drag_operation()  # Recursive call for another test
        elif again in ['n', 'no']:
            break
        else:
            print("Please enter 'y' or 'n'")
    
    return True

if __name__ == "__main__":
    test_drag_operation()
