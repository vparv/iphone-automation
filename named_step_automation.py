#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

class NamedStepAutomation:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        
    def execute_step(self, step_name, action_type, x=None, y=None, key=None, delay=1.0):
        """Execute a named step with error handling."""
        print(f"🔄 STEP: {step_name}")
        
        try:
            if action_type == "click":
                print(f"   🖱️  Clicking at ({x}, {y})")
                self.automation.click(x, y)
                print(f"   ✅ Click executed")
                
            elif action_type == "key":
                print(f"   ⌨️  Pressing key: {key}")
                self.automation.press_key(key)
                print(f"   ✅ Key pressed")
                
            elif action_type == "wait":
                print(f"   ⏳ Waiting {delay} seconds")
                
            time.sleep(delay)
            print(f"   ✅ STEP COMPLETED: {step_name}")
            return True
            
        except Exception as e:
            print(f"   ❌ STEP FAILED: {step_name} - {e}")
            return False
    
    def process_single_image(self, image_num):
        """Process one image with named steps."""
        print(f"\n🎯 === PROCESSING IMAGE #{image_num} ===")
        
        if not self.automation.focus_window():
            print("❌ Could not focus window")
            return False
        
        steps = [
            # Step 1: Click Use It button
            {
                "name": "CLICK_USE_IT_BUTTON",
                "type": "click",
                "x": 567,
                "y": 648,
                "delay": 4.0
            },
            
            # Step 2: Click Next button (AI remove bg dialog)
            {
                "name": "CLICK_NEXT_IN_AI_DIALOG", 
                "type": "click",
                "x": 567,
                "y": 702,
                "delay": 3.0
            },
            
            # Step 3: Click size input field
            {
                "name": "CLICK_SIZE_INPUT_FIELD",
                "type": "click", 
                "x": 1024,
                "y": 443,
                "delay": 2.0
            },
            
            # Step 4: Clear field
            {
                "name": "CLEAR_SIZE_FIELD",
                "type": "click",
                "x": 970,
                "y": 440,
                "delay": 1.0
            },
            
            # Step 5: Delete existing text
            {
                "name": "DELETE_TEXT_1",
                "type": "key",
                "key": "backspace",
                "delay": 0.2
            },
            
            {
                "name": "DELETE_TEXT_2", 
                "type": "key",
                "key": "backspace",
                "delay": 0.5
            },
            
            # Step 6: Type new size
            {
                "name": "TYPE_1",
                "type": "key", 
                "key": "1",
                "delay": 0.1
            },
            
            {
                "name": "TYPE_6_FIRST",
                "type": "key",
                "key": "6", 
                "delay": 0.1
            },
            
            {
                "name": "TYPE_6_SECOND",
                "type": "key",
                "key": "6",
                "delay": 1.0
            },
            
            # Step 7: Tab to next field
            {
                "name": "TAB_TO_NEXT_FIELD",
                "type": "key",
                "key": "tab",
                "delay": 0.5
            },
            
            # Step 8: Click confirmation
            {
                "name": "CLICK_CONFIRMATION_BUTTON",
                "type": "click",
                "x": 963,
                "y": 559, 
                "delay": 3.0
            },
            
            # Step 9: Navigate back - First click
            {
                "name": "NAVIGATE_BACK_1",
                "type": "click",
                "x": 903,
                "y": 129,
                "delay": 1.0
            },
            
            # Step 10: Return to gallery
            {
                "name": "RETURN_TO_GALLERY_LOOP_POINT", 
                "type": "click",
                "x": 1015,
                "y": 113,
                "delay": 1.0
            },
            
            # Step 14: Click at tracked position (FINAL LOOP POINT)
            {
                "name": "CLICK_TRACKED_POSITION_FINAL",
                "type": "click", 
                "x": 1014,
                "y": 129,
                "delay": 2.0
            },
            
            # Step 15: Click at new coordinate
            {
                "name": "CLICK_NEW_POSITION_STEP_15",
                "type": "click",
                "x": 25,
                "y": 40,
                "delay": 2.0
            }
        ]
        
        # Execute each step
        for i, step in enumerate(steps, 1):
            print(f"\n📍 Step {i}/{len(steps)}")
            
            success = self.execute_step(
                step["name"],
                step["type"],
                step.get("x"),
                step.get("y"), 
                step.get("key"),
                step.get("delay", 1.0)
            )
            
            if not success:
                print(f"❌ AUTOMATION FAILED AT STEP: {step['name']}")
                return False
        
        print(f"\n✅ IMAGE #{image_num} COMPLETED SUCCESSFULLY!")
        return True

def run_image(image_num):
    """Run automation for a specific image number."""
    from gallery_navigator import GalleryNavigator
    
    # Calculate position
    row = (image_num - 1) // 4
    col = (image_num - 1) % 4
    
    print(f"🎯 Setting up Image #{image_num}")
    print(f"📍 Position: Row {row + 1}, Column {col + 1}")
    
    # Set position
    navigator = GalleryNavigator()
    navigator.save_state(row, col)
    
    # Navigate to gallery
    print("📂 Navigating to gallery...")
    if not navigator.navigate_to_gallery():
        print("❌ Failed to navigate to gallery")
        return False
    time.sleep(1.5)
    
    # Select image
    print(f"🖱️  Selecting Image #{image_num}...")
    if not navigator.select_next_image():
        print(f"❌ Failed to select Image #{image_num}")
        return False
    time.sleep(1.5)
    
    # Run workflow
    automation = NamedStepAutomation()
    return automation.process_single_image(image_num)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_num = int(sys.argv[1])
        print(f"🚀 Running Named Step Automation for Image #{image_num}")
        print("=" * 60)
        
        success = run_image(image_num)
        
        if success:
            print(f"\n🎉 SUCCESS! Image #{image_num} completed!")
        else:
            print(f"\n❌ FAILED! Image #{image_num} did not complete!")
    else:
        print("Usage: python3 named_step_automation.py <image_number>")
        print("Example: python3 named_step_automation.py 6")
