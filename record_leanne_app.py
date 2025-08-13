#!/usr/bin/env python3

import sys
import os
import time
import signal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

def record_liene_session():
    """Record a manual interaction session with Liene Photo HD app."""
    print("Liene Photo HD Recording Session")
    print("=" * 40)
    
    # Create automation instance
    automation = iPhoneAutomation()
    
    # Set the correct window title for Liene Photo HD
    automation.window_title = "Liene Photo HD"
    
    print(f"Looking for '{automation.window_title}' window...")
    if not automation.focus_window():
        print(f"Error: Could not find '{automation.window_title}' window")
        print("Make sure Liene Photo HD is running and visible")
        print("\nTip: If the window title is different, update the 'window_title' variable in this script")
        return
    
    print("Window found and focused!")
    print("\nInstructions:")
    print("1. This script will start recording your manual interactions")
    print("2. Perform your desired actions in Liene Photo HD window")
    print("3. Upload images, edit photos, or whatever workflow you want to automate")
    print("4. Press Ctrl+C in this terminal to stop recording")
    print("5. The recording will be saved and you can replay it later")
    
    input("\nPress Enter to start recording...")
    
    # Set up Ctrl+C handler to stop recording gracefully
    def signal_handler(signum, frame):
        print("\n\nStopping recording...")
        actions = automation.stop_recording()
        
        if actions:
            # Save the recording
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"recordings/liene_session_{timestamp}.json"
            
            # Create recordings directory if it doesn't exist
            os.makedirs("recordings", exist_ok=True)
            automation.save_recording(filename)
            
            # Generate a Python script
            script_content = automation.generate_script(actions, f"liene_automation_{timestamp}")
            script_filename = f"recordings/liene_session_{timestamp}.py"
            
            with open(script_filename, 'w') as f:
                f.write(script_content)
            
            print(f"📝 Generated script saved to {script_filename}")
            
            # Ask if user wants to replay immediately
            while True:
                replay = input("\nWould you like to replay the recording now? (y/n): ").lower().strip()
                if replay in ['y', 'yes']:
                    print("\nReplaying in 3 seconds...")
                    time.sleep(3)
                    automation.replay_recording(actions, speed_multiplier=1.0)
                    break
                elif replay in ['n', 'no']:
                    break
                else:
                    print("Please enter 'y' or 'n'")
            
            print(f"\n✅ Session complete!")
            print(f"📁 Recording saved: {filename}")
            print(f"🐍 Script saved: {script_filename}")
        
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start recording
    automation.start_recording()
    
    # Keep the script running until Ctrl+C
    try:
        while automation.recording:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    record_liene_session()
