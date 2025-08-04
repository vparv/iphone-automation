#!/usr/bin/env python3

import sys
import os
import time
import signal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation

def record_session():
    """Record a manual interaction session."""
    print("iPhone Mirroring Recording Session")
    print("=" * 40)
    
    automation = iPhoneAutomation()
    
    print("Looking for iPhone Mirroring window...")
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        print("Make sure iPhone Mirroring is running and visible")
        return
    
    print("Window found and focused!")
    print("\nInstructions:")
    print("1. This script will start recording your manual interactions")
    print("2. Perform your desired actions in the iPhone Mirroring window")
    print("3. Press Ctrl+C in this terminal to stop recording")
    print("4. The recording will be saved and you can replay it later")
    
    input("\nPress Enter to start recording...")
    
    # Set up Ctrl+C handler to stop recording gracefully
    def signal_handler(signum, frame):
        print("\n\nStopping recording...")
        actions = automation.stop_recording()
        
        if actions:
            # Save the recording
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"recordings/session_{timestamp}.json"
            
            # Create recordings directory if it doesn't exist
            os.makedirs("recordings", exist_ok=True)
            automation.save_recording(filename)
            
            # Generate a Python script
            script_content = automation.generate_script(actions, f"recorded_session_{timestamp}")
            script_filename = f"recordings/session_{timestamp}.py"
            
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

def replay_session():
    """Replay a previously recorded session."""
    print("iPhone Mirroring Replay Session")
    print("=" * 35)
    
    automation = iPhoneAutomation()
    
    print("Looking for iPhone Mirroring window...")
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return
    
    # List available recordings
    recordings_dir = "recordings"
    if not os.path.exists(recordings_dir):
        print("No recordings directory found. Record a session first!")
        return
    
    recording_files = [f for f in os.listdir(recordings_dir) if f.endswith('.json')]
    
    if not recording_files:
        print("No recordings found. Record a session first!")
        return
    
    print("\nAvailable recordings:")
    for i, filename in enumerate(recording_files, 1):
        print(f"  {i}. {filename}")
    
    while True:
        try:
            choice = input(f"\nSelect recording (1-{len(recording_files)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(recording_files):
                selected_file = recording_files[idx]
                break
            else:
                print(f"Please enter a number between 1 and {len(recording_files)}")
        except ValueError:
            print("Please enter a valid number")
    
    # Load and replay the recording
    filepath = os.path.join(recordings_dir, selected_file)
    actions = automation.load_recording(filepath)
    
    if actions:
        while True:
            try:
                speed = input("\nPlayback speed (0.5=slow, 1.0=normal, 2.0=fast): ").strip()
                if not speed:
                    speed = 1.0
                else:
                    speed = float(speed)
                break
            except ValueError:
                print("Please enter a valid number")
        
        print(f"\nStarting playback in 3 seconds...")
        time.sleep(3)
        automation.replay_recording(actions, speed_multiplier=speed)

def main():
    """Main menu for recording and playback."""
    while True:
        print("\niPhone Mirroring Automation Recorder")
        print("=" * 40)
        print("1. Record new session")
        print("2. Replay existing session")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            record_session()
        elif choice == '2':
            replay_session()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()