#!/usr/bin/env python3

import time
from iphone_automation import iPhoneAutomation

def scroll_to_nav_buttons():
    """Scroll horizontally to reveal hidden navigation buttons."""
    print("Navigation Bar Horizontal Scroll Script")
    print("=" * 40)
    
    automation = iPhoneAutomation()
    
    print("Looking for iPhone Mirroring window...")
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        print("Make sure iPhone Mirroring is running and visible")
        return
    
    print("Window found and focused!")
    print("\nScript will:")
    print("1. Wait 5 seconds for you to position the app")
    print("2. Scroll horizontally right to reveal hidden nav buttons")
    
    # Give user time to position their app/screen
    print("\nStarting countdown...")
    for i in range(5, 0, -1):
        print(f"Scrolling in {i} seconds...")
        time.sleep(1)
    
    print("\n🔄 Scrolling horizontally to reveal nav buttons...")
    
    # Scroll at the center of the navigation bar area
    # Assuming nav bar is typically in the top portion of the screen
    nav_x = automation.window_bounds['width'] // 2  # Center horizontally
    nav_y = 100  # Top area where nav bars typically are
    
    # Use enhanced horizontal scroll for smooth touchpad-like motion
    automation.enhanced_horizontal_scroll(
        x=nav_x, 
        y=nav_y, 
        direction='right',  # Scroll right to reveal buttons on the right
        distance=200,       # 200px as requested
        smoothness=15       # Very smooth scrolling
    )
    
    print("✅ Horizontal scroll completed!")
    print(f"Scrolled 200px to the right at position ({nav_x}, {nav_y})")

if __name__ == "__main__":
    scroll_to_nav_buttons()