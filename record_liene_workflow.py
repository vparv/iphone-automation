#!/usr/bin/env python3

import sys
import os
import time
import signal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

class LieneWorkflowRecorder:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        
    def record_single_workflow(self):
        """Record a single complete workflow for one image."""
        print("🎬 Liene Photo HD Workflow Recorder")
        print("=" * 45)
        print("This will record a single complete workflow from start to finish.")
        print("Make sure Liene Photo HD is open and ready.")
        
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
            
        print("✅ Window found and focused!")
        
        print("\n📋 Workflow Steps to Record:")
        print("1. Click Canvas button (+ Canvas)")
        print("2. Click Upload in sidebar")
        print("3. Select FIRST image in grid (top-left)")
        print("4. Click 'Use it' button")
        print("5. Click 'Next' button")
        print("6. Handle size input (clear, type 166, press Enter)")
        print("7. Click confirmation buttons")
        print("8. Click back button to return to main screen")
        
        print("\n⚠️  IMPORTANT:")
        print("   - Perform actions slowly and deliberately")
        print("   - Wait for UI responses between clicks")
        print("   - Select the FIRST (top-left) image in the grid")
        print("   - Complete the entire workflow in one session")
        
        input("\nPress Enter when ready to start recording...")
        
        # Give 5 seconds to position before recording starts
        print("\n⏳ Starting recording in 5 seconds... Position yourself now!")
        time.sleep(5)
        
        # Set up signal handler for stopping recording
        def signal_handler(signum, frame):
            print("\n\n⏹️  Stopping recording...")
            actions = self.automation.stop_recording()
            
            if actions:
                # Save with timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"recordings/liene_workflow_{timestamp}.json"
                
                # Create recordings directory if needed
                os.makedirs("recordings", exist_ok=True)
                self.automation.save_recording(filename)
                
                # Generate Python script
                script_content = self.automation.generate_script(actions, f"liene_workflow_{timestamp}")
                script_filename = f"recordings/liene_workflow_{timestamp}.py"
                
                with open(script_filename, 'w') as f:
                    f.write(script_content)
                
                print(f"\n✅ Recording saved:")
                print(f"   📁 JSON: {filename}")
                print(f"   🐍 Script: {script_filename}")
                
                # Analyze the recording
                self.analyze_recording(actions)
            
            # Final 5-second delay before exit
            print("\n⏳ Finishing in 5 seconds...")
            time.sleep(5)
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Start recording
        print("\n🔴 Recording started! Perform your workflow now.")
        print("   Press Ctrl+C in this terminal when finished.")
        self.automation.start_recording()
        
        # Keep running until stopped
        try:
            while self.automation.recording:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
    
    def analyze_recording(self, actions):
        """Analyze the recorded actions to extract coordinates."""
        print("\n📊 Recording Analysis")
        print("=" * 25)
        
        click_actions = [action for action in actions if action['type'] == 'click']
        
        if len(click_actions) < 3:
            print("⚠️  Recording seems incomplete - expected more clicks")
            return
        
        print(f"Total click actions recorded: {len(click_actions)}")
        print("\n📍 Key Coordinates Detected:")
        
        # Try to identify key workflow coordinates
        for i, action in enumerate(click_actions):
            x, y = action['x'], action['y']
            
            # Attempt to identify the click based on typical coordinates
            if i == 0:
                print(f"   Canvas button: ({x}, {y})")
            elif i == 1:
                print(f"   Upload button: ({x}, {y})")
            elif i == 2:
                print(f"   First image (grid): ({x}, {y}) ⭐ KEY COORDINATE")
            elif 'Use it' in str(action) or y > 600:
                print(f"   Use it button: ({x}, {y})")
            elif y > 600:
                print(f"   Next button: ({x}, {y})")
            else:
                print(f"   Step {i+1}: ({x}, {y})")
        
        # Extract grid base coordinates
        if len(click_actions) >= 3:
            grid_click = click_actions[2]  # Assuming 3rd click is the grid
            print(f"\n🎯 Recommended Grid Base Coordinates:")
            print(f"   base_x = {grid_click['x']}")
            print(f"   base_y = {grid_click['y']}")
    
    def record_grid_calibration(self):
        """Record clicks on multiple grid positions for spacing calculation."""
        print("🔲 Grid Calibration Recorder")
        print("=" * 35)
        print("This will help determine accurate grid spacing.")
        
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
            
        print("✅ Window found and focused!")
        print("\n📋 Instructions:")
        print("1. Navigate to the image grid (Canvas > Upload)")
        print("2. I'll ask you to click specific grid positions")
        print("3. Click each position accurately")
        
        input("\nPress Enter when you're at the image grid...")
        
        positions_to_test = [
            (1, 1, "Top-left (1st image)"),
            (1, 2, "Top row, 2nd image"),
            (1, 3, "Top row, 3rd image"),
            (1, 4, "Top row, 4th image"),
            (2, 1, "Second row, 1st image"),
            (2, 2, "Second row, 2nd image")
        ]
        
        recorded_positions = []
        
        for row, col, description in positions_to_test:
            print(f"\n📍 Click: {description}")
            input("   Press Enter when ready to click...")
            
            # Record a single click
            self.automation.start_recording()
            input("   Click the position now, then press Enter...")
            actions = self.automation.stop_recording()
            
            if actions and actions[-1]['type'] == 'click':
                x, y = actions[-1]['x'], actions[-1]['y']
                recorded_positions.append((row, col, x, y, description))
                print(f"   ✅ Recorded: ({x}, {y})")
            else:
                print("   ❌ No click recorded")
        
        # Calculate spacing
        self.calculate_grid_spacing(recorded_positions)
    
    def calculate_grid_spacing(self, positions):
        """Calculate grid spacing from recorded positions."""
        print("\n📐 Grid Spacing Analysis")
        print("=" * 30)
        
        if len(positions) < 2:
            print("❌ Need at least 2 positions to calculate spacing")
            return
        
        # Find horizontal spacing (same row, different columns)
        horizontal_pairs = [(p1, p2) for p1 in positions for p2 in positions 
                          if p1[0] == p2[0] and p1[1] != p2[1]]
        
        if horizontal_pairs:
            p1, p2 = horizontal_pairs[0]
            spacing_x = abs(p2[2] - p1[2]) / abs(p2[1] - p1[1])
            print(f"Horizontal spacing: {spacing_x:.1f}px")
        
        # Find vertical spacing (same column, different rows)
        vertical_pairs = [(p1, p2) for p1 in positions for p2 in positions 
                        if p1[1] == p2[1] and p1[0] != p2[0]]
        
        if vertical_pairs:
            p1, p2 = vertical_pairs[0]
            spacing_y = abs(p2[3] - p1[3]) / abs(p2[0] - p1[0])
            print(f"Vertical spacing: {spacing_y:.1f}px")
        
        # Find base coordinates (top-left position)
        base_position = min(positions, key=lambda p: (p[0], p[1]))
        if base_position:
            print(f"Base coordinates: ({base_position[2]}, {base_position[3]})")
            
        print("\n🔧 Recommended Configuration:")
        if horizontal_pairs and vertical_pairs:
            print(f"   base_x = {base_position[2]}")
            print(f"   base_y = {base_position[3]}")
            print(f"   spacing_x = {int(spacing_x)}")
            print(f"   spacing_y = {int(spacing_y)}")

if __name__ == "__main__":
    recorder = LieneWorkflowRecorder()
    
    print("🎬 Liene Photo HD Workflow Recorder")
    print("=" * 40)
    print("Choose recording mode:")
    print("1. Record complete workflow (recommended)")
    print("2. Record grid calibration only")
    
    choice = input("\nEnter choice (1/2): ").strip()
    
    if choice == "2":
        recorder.record_grid_calibration()
    else:
        recorder.record_single_workflow()
