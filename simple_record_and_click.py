#!/usr/bin/env python3

import sys
import os
import time
import signal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

def record_and_click():
    """Simple recording with automatic first click."""
    print("🎬 Simple Record & Click")
    print("=" * 30)
    
    automation = iPhoneAutomation()
    automation.window_title = "Liene Photo HD"
    
    print("1. Make sure you're at the Preview screen with 'Use it' button")
    input("Press Enter when ready...")
    
    # Focus window properly
    print("🔍 Focusing window...")
    if automation.focus_window():
        print("✅ Window focused successfully!")
    else:
        print("⚠️  Window focus failed, but continuing...")
    
    print("\n🎯 I'll click the 'Use it' button first, then start recording")
    print("After that, continue with your workflow manually")
    
    input("Press Enter to click 'Use it' and start recording...")
    
    # Click the Use it button (current coordinate)
    try:
        print("Clicking 'Use it' button at (530, 647)...")
        automation.click(530, 647)
        time.sleep(2)
        print("✅ Clicked 'Use it' button!")
    except Exception as e:
        print(f"❌ Error clicking: {e}")
        return
    
    # Set up recording stop handler
    def stop_recording(signum, frame):
        print("\n\n⏹️  Stopping recording...")
        try:
            actions = automation.stop_recording()
            
            if actions and len(actions) > 0:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"recordings/post_click_{timestamp}.json"
                
                os.makedirs("recordings", exist_ok=True)
                automation.save_recording(filename)
                
                print(f"\n✅ Recording saved: {filename}")
                print(f"📊 Actions recorded: {len(actions)}")
                
                # Quick analysis
                clicks = [a for a in actions if a['type'] == 'click']
                keys = [a for a in actions if a['type'] == 'key']
                
                print(f"\n📍 Recorded coordinates:")
                for i, click in enumerate(clicks, 1):
                    print(f"   {i}. ({click['x']}, {click['y']})")
                
                if keys:
                    print(f"\n⌨️  Keyboard actions: {len(keys)}")
                    
            else:
                print("\n❌ No actions recorded")
        except Exception as e:
            print(f"\n❌ Error saving: {e}")
        
        sys.exit(0)
    
    signal.signal(signal.SIGINT, stop_recording)
    
    # Start recording for the rest of the workflow
    print("\n🔴 Recording started for remaining workflow...")
    print("Continue with: Next button → Size input → Confirmations → Back")
    print("Press Ctrl+C when back at main screen")
    
    try:
        automation.start_recording()
        while automation.recording:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    record_and_click()
