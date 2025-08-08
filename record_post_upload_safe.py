#!/usr/bin/env python3

import sys
import os
import time
import signal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

class SafePostUploadRecorder:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        
    def record_post_upload_workflow(self):
        """Record the workflow starting after image selection - SAFE MODE."""
        print("🎬 SAFE Post-Upload Workflow Recorder")
        print("=" * 45)
        print("⚠️  SAFE MODE: This script will ONLY record, no automation will run!")
        
        print("\n📋 Instructions:")
        print("1. Get back to the Preview screen with 'Use it' button")
        print("2. This script will ONLY record your clicks")
        print("3. No automation will run automatically")
        
        # Wait for user to be ready
        print("\n🔄 First, navigate back to the Preview screen:")
        print("   - Go to Canvas > Upload")
        print("   - Select any image from the grid")
        print("   - Wait for the Preview dialog with 'Use it' button")
        
        input("\nPress Enter when you're back at the Preview screen...")
        
        # Check window focus but don't auto-focus to avoid triggering anything
        try:
            window = self.automation.automation.find_iphone_window(self.automation.window_title)
            if not window:
                print("⚠️  Warning: Cannot find Liene Photo HD window")
                proceed = input("Continue anyway? (y/n): ").lower().strip()
                if proceed != 'y':
                    return False
            else:
                print("✅ Liene Photo HD window detected!")
        except:
            print("⚠️  Window detection failed, but proceeding...")
        
        print("\n📝 Workflow to Record:")
        print("1. Click 'Use it' button")
        print("2. Wait for next screen") 
        print("3. Click 'Next' button")
        print("4. Handle size input (clear field, type 166, press Enter)")
        print("5. Click any confirmation buttons")
        print("6. Click back button to return to main screen")
        
        print("\n⚠️  Recording Tips:")
        print("   - Perform each action slowly")
        print("   - Wait for UI responses between clicks")
        print("   - Don't rush through the steps")
        
        input("\nReady to start recording? Press Enter...")
        
        # Set up signal handler for stopping recording
        def signal_handler(signum, frame):
            print("\n\n⏹️  Stopping recording...")
            try:
                actions = self.automation.stop_recording()
                
                if actions and len(actions) > 0:
                    # Save with timestamp
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"recordings/post_upload_safe_{timestamp}.json"
                    
                    # Create recordings directory if needed
                    os.makedirs("recordings", exist_ok=True)
                    self.automation.save_recording(filename)
                    
                    # Generate Python script
                    script_content = self.automation.generate_script(actions, f"post_upload_safe_{timestamp}")
                    script_filename = f"recordings/post_upload_safe_{timestamp}.py"
                    
                    with open(script_filename, 'w') as f:
                        f.write(script_content)
                    
                    print(f"\n✅ Post-upload workflow recorded successfully!")
                    print(f"   📁 JSON: {filename}")
                    print(f"   🐍 Script: {script_filename}")
                    print(f"   📊 Actions recorded: {len(actions)}")
                    
                    # Analyze the recording
                    self.analyze_recording(actions)
                    
                else:
                    print("\n❌ No actions were recorded!")
                    print("Make sure you clicked within the Liene Photo HD window.")
                    
            except Exception as e:
                print(f"\n❌ Error saving recording: {e}")
                
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Start recording with explicit window focus
        print("\n🔴 Recording started!")
        print("   Perform your workflow now...")
        print("   Press Ctrl+C in this terminal when completely finished.")
        print("   (Make sure you're back at the main screen before stopping)")
        
        try:
            self.automation.start_recording()
            
            # Keep running until stopped
            while self.automation.recording:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n⏹️  Recording stopped by user")
        except Exception as e:
            print(f"\n❌ Recording error: {e}")
    
    def analyze_recording(self, actions):
        """Analyze the recorded actions and provide coordinate summary."""
        print("\n📊 Recording Analysis")
        print("=" * 25)
        
        click_actions = [action for action in actions if action['type'] == 'click']
        key_actions = [action for action in actions if action['type'] == 'key']
        
        print(f"✅ Total clicks recorded: {len(click_actions)}")
        print(f"✅ Total key presses: {len(key_actions)}")
        
        if len(click_actions) == 0:
            print("❌ No clicks recorded! Make sure you clicked in the app window.")
            return
        
        print("\n📍 Recorded Click Coordinates:")
        step_labels = [
            "Use it button",
            "Next button", 
            "Size input field",
            "Confirmation button 1",
            "Confirmation button 2", 
            "Back button"
        ]
        
        for i, action in enumerate(click_actions):
            x, y = action['x'], action['y']
            label = step_labels[i] if i < len(step_labels) else f"Additional click {i+1}"
            timestamp = action.get('timestamp', 0)
            print(f"   {i+1}. {label}: ({x}, {y}) at {timestamp:.1f}s")
        
        if key_actions:
            print(f"\n⌨️  Keyboard sequence:")
            for action in key_actions:
                key = action['key']
                timestamp = action.get('timestamp', 0)
                print(f"   Key '{key}' at {timestamp:.1f}s")
        
        # Generate updated coordinates for the main automation
        if len(click_actions) >= 2:
            print(f"\n🔧 Suggested coordinate updates:")
            print(f"   'use_it_button': ({click_actions[0]['x']}, {click_actions[0]['y']}),")
            if len(click_actions) > 1:
                print(f"   'next_button': ({click_actions[1]['x']}, {click_actions[1]['y']}),")
            if len(click_actions) > 2:
                print(f"   'size_input': ({click_actions[2]['x']}, {click_actions[2]['y']}),")

if __name__ == "__main__":
    print("🛡️  SAFE RECORDING MODE")
    print("This script will only record - no automation will run!")
    
    recorder = SafePostUploadRecorder()
    recorder.record_post_upload_workflow()
