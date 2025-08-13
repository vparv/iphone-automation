#!/usr/bin/env python3

import sys
import os
import time
import signal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

class PostUploadRecorder:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        
    def record_post_upload_workflow(self):
        """Record the workflow starting after image selection."""
        print("🎬 Post-Upload Workflow Recorder")
        print("=" * 40)
        print("This will record the workflow starting AFTER image selection.")
        
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
            
        print("✅ Window found and focused!")
        
        print("\n📋 Setup Instructions:")
        print("1. Manually navigate to: Canvas > Upload")
        print("2. Select ANY image from the grid")
        print("3. Get to the point where you see the 'Use it' button")
        print("4. DO NOT click 'Use it' yet - that's where recording starts")
        
        print("\n📝 Workflow Steps to Record:")
        print("4. Click 'Use it' button")
        print("5. Click 'Next' button") 
        print("6. Handle size input and confirmations")
        print("7. Navigate back to main screen")
        
        print("\n⚠️  IMPORTANT:")
        print("   - Start recording when you can see the 'Use it' button")
        print("   - Perform each step slowly and wait for UI responses")
        print("   - Complete the entire post-upload workflow")
        print("   - End when you're back at the main screen")
        
        ready = input("\nAre you ready at the 'Use it' button screen? (y/n): ").lower().strip()
        if ready != 'y':
            print("Please navigate to the 'Use it' button screen first.")
            return False
        
        # Set up signal handler for stopping recording
        def signal_handler(signum, frame):
            print("\n\n⏹️  Stopping recording...")
            actions = self.automation.stop_recording()
            
            if actions:
                # Save with timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"recordings/post_upload_{timestamp}.json"
                
                # Create recordings directory if needed
                os.makedirs("recordings", exist_ok=True)
                self.automation.save_recording(filename)
                
                # Generate Python script
                script_content = self.automation.generate_script(actions, f"post_upload_{timestamp}")
                script_filename = f"recordings/post_upload_{timestamp}.py"
                
                with open(script_filename, 'w') as f:
                    f.write(script_content)
                
                print(f"\n✅ Post-upload workflow recorded:")
                print(f"   📁 JSON: {filename}")
                print(f"   🐍 Script: {script_filename}")
                
                # Analyze the recording
                self.analyze_post_upload_recording(actions)
                
                # Generate integration code
                self.generate_integration_code(actions, timestamp)
                
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Start recording
        print("\n🔴 Recording started!")
        print("   Click 'Use it' and complete the workflow...")
        print("   Press Ctrl+C in this terminal when finished.")
        self.automation.start_recording()
        
        # Keep running until stopped
        try:
            while self.automation.recording:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
    
    def analyze_post_upload_recording(self, actions):
        """Analyze the recorded post-upload actions."""
        print("\n📊 Post-Upload Recording Analysis")
        print("=" * 35)
        
        click_actions = [action for action in actions if action['type'] == 'click']
        key_actions = [action for action in actions if action['type'] == 'key']
        
        print(f"Total click actions: {len(click_actions)}")
        print(f"Total keyboard actions: {len(key_actions)}")
        
        print("\n📍 Detected Coordinates:")
        
        step_names = [
            "Use it button",
            "Next button", 
            "Size input area",
            "Confirmation button 1",
            "Confirmation button 2",
            "Back button",
            "Additional step"
        ]
        
        for i, action in enumerate(click_actions):
            x, y = action['x'], action['y']
            step_name = step_names[i] if i < len(step_names) else f"Step {i+1}"
            print(f"   {step_name}: ({x}, {y})")
        
        if key_actions:
            print(f"\n⌨️  Keyboard Input Sequence:")
            for action in key_actions:
                print(f"   Key: '{action['key']}'")
    
    def generate_integration_code(self, actions, timestamp):
        """Generate code to integrate the new recording into existing automation."""
        click_actions = [action for action in actions if action['type'] == 'click']
        key_actions = [action for action in actions if action['type'] == 'key']
        
        code_filename = f"recordings/integration_code_{timestamp}.py"
        
        code_content = f'''#!/usr/bin/env python3
# Generated integration code for post-upload workflow
# Recorded: {time.strftime("%Y-%m-%d %H:%M:%S")}

def execute_post_upload_workflow(automation):
    """
    Execute the post-upload workflow starting after image selection.
    
    Args:
        automation: iPhoneAutomation instance
    """
    import time
    
    print("Executing post-upload workflow...")
    
'''
        
        # Add click actions
        step_counter = 1
        for i, action in enumerate(click_actions):
            x, y = action['x'], action['y']
            
            # Try to identify the step
            if i == 0:
                step_name = "Click 'Use it' button"
                delay = 3.0  # Wait for processing
            elif i == 1:
                step_name = "Click 'Next' button"
                delay = 2.0
            elif 'size' in str(action).lower() or (i == 2 and len(click_actions) > 3):
                step_name = "Click size input area"
                delay = 0.5
            elif i >= len(click_actions) - 2:
                if i == len(click_actions) - 1:
                    step_name = "Click back button"
                    delay = 2.0
                else:
                    step_name = "Click confirmation button"
                    delay = 1.0
            else:
                step_name = f"Click step {step_counter}"
                delay = 1.0
            
            code_content += f'''    # STEP {step_counter}: {step_name}
    print("{step_counter}. {step_name}...")
    automation.click({x}, {y})
    time.sleep({delay})
    
'''
            step_counter += 1
        
        # Add keyboard actions if any
        if key_actions:
            code_content += f'''    # Handle keyboard input
    print("{step_counter}. Handling keyboard input...")
'''
            for action in key_actions:
                key = action['key']
                if key == 'backspace':
                    code_content += f"    automation.press_key('backspace')\n"
                elif key == 'enter':
                    code_content += f"    automation.press_key('enter')\n"
                elif len(key) == 1 and key.isalnum():
                    # Single character - part of typing
                    continue  # We'll handle this as type_text
                else:
                    code_content += f"    automation.press_key('{key}')\n"
            
            # Extract typed text from consecutive character keys
            typed_chars = []
            for action in key_actions:
                key = action['key']
                if len(key) == 1 and key.isalnum():
                    typed_chars.append(key)
                elif key in ['backspace', 'enter'] and typed_chars:
                    if typed_chars:
                        text = ''.join(typed_chars)
                        code_content += f"    automation.type_text('{text}')\n"
                        typed_chars = []
            
            if typed_chars:
                text = ''.join(typed_chars)
                code_content += f"    automation.type_text('{text}')\n"
            
            code_content += f"    time.sleep(1.0)\n\n"
        
        code_content += '''    print("✅ Post-upload workflow completed!")
    return True

# Example usage:
if __name__ == "__main__":
    from iphone_automation import iPhoneAutomation
    
    automation = iPhoneAutomation()
    automation.window_title = "Liene Photo HD"
    
    if automation.focus_window():
        execute_post_upload_workflow(automation)
    else:
        print("Could not find Liene Photo HD window")
'''
        
        with open(code_filename, 'w') as f:
            f.write(code_content)
        
        print(f"\n🔧 Integration code generated: {code_filename}")
        print("This code can be used to replace the post-upload steps in your main automation.")

if __name__ == "__main__":
    recorder = PostUploadRecorder()
    recorder.record_post_upload_workflow()
