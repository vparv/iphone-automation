#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

class EnhancedGridCalibration:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        self.tested_coordinates = []
        self.step_history = []
        
    def test_coordinate_fast(self, coords, description, step_number):
        """Test a coordinate with fast, smooth progression."""
        x, y = coords
        
        print(f"\n🎯 Step {step_number}: {description}")
        print(f"   Coordinate: ({x}, {y})")
        
        # Store step in history
        step_info = {
            'step': step_number,
            'coords': (x, y),
            'description': description,
            'status': 'pending'
        }
        self.step_history.append(step_info)
        
        # Quick countdown for user to prepare
        print("   Clicking in: 3", end="", flush=True)
        time.sleep(0.5)
        print("...2", end="", flush=True)
        time.sleep(0.5)
        print("...1", end="", flush=True)
        time.sleep(0.5)
        print("...CLICK!", flush=True)
        
        # Perform the click
        self.automation.click(x, y)
        
        # Fast verification
        print("   ✅ Click executed!")
        
        while True:
            print(f"\n   Options:")
            print(f"   [1] ✅ Correct - Continue")
            print(f"   [2] ❌ Wrong - Adjust coordinates")
            print(f"   [3] 🔄 Replay this step")
            print(f"   [4] ⏪ Replay last 2 steps")
            print(f"   [5] 📋 Show step history")
            
            choice = input("   Choice (1-5): ").strip()
            
            if choice == "1":
                step_info['status'] = 'correct'
                self.tested_coordinates.append((coords, description, 'correct'))
                print(f"   ✅ {description} verified!")
                return coords
                
            elif choice == "2":
                return self.adjust_coordinates(coords, description, step_number)
                
            elif choice == "3":
                print(f"   🔄 Replaying step {step_number}...")
                return self.test_coordinate_fast(coords, description, step_number)
                
            elif choice == "4":
                return self.replay_last_steps(step_number)
                
            elif choice == "5":
                self.show_step_history()
                continue
                
            else:
                print("   ❌ Invalid choice. Please enter 1-5.")
    
    def adjust_coordinates(self, original_coords, description, step_number):
        """Allow user to adjust both X and Y coordinates."""
        x, y = original_coords
        
        print(f"\n🔧 Adjusting coordinates for: {description}")
        print(f"   Current: ({x}, {y})")
        
        while True:
            print(f"\n   Adjustment options:")
            print(f"   [1] Change X coordinate only")
            print(f"   [2] Change Y coordinate only") 
            print(f"   [3] Change both X and Y coordinates")
            print(f"   [4] Manual click mode (click where it should be)")
            print(f"   [5] Cancel adjustment")
            
            adj_choice = input("   Choice (1-5): ").strip()
            
            if adj_choice == "1":
                new_x = self.get_coordinate_input("X", x)
                if new_x is not None:
                    new_coords = (new_x, y)
                    return self.test_adjusted_coordinate(new_coords, description, step_number)
                    
            elif adj_choice == "2":
                new_y = self.get_coordinate_input("Y", y)
                if new_y is not None:
                    new_coords = (x, new_y)
                    return self.test_adjusted_coordinate(new_coords, description, step_number)
                    
            elif adj_choice == "3":
                new_x = self.get_coordinate_input("X", x)
                if new_x is None:
                    continue
                new_y = self.get_coordinate_input("Y", y)
                if new_y is None:
                    continue
                new_coords = (new_x, new_y)
                return self.test_adjusted_coordinate(new_coords, description, step_number)
                
            elif adj_choice == "4":
                return self.manual_click_mode(description, step_number)
                
            elif adj_choice == "5":
                print("   🚫 Adjustment cancelled")
                return original_coords
                
            else:
                print("   ❌ Invalid choice. Please enter 1-5.")
    
    def get_coordinate_input(self, axis, current_value):
        """Get a coordinate input with validation."""
        while True:
            try:
                new_val = input(f"   Enter new {axis} coordinate (current: {current_value}): ").strip()
                if not new_val:
                    print("   🚫 No change made")
                    return None
                return int(new_val)
            except ValueError:
                print("   ❌ Please enter a valid number")
    
    def test_adjusted_coordinate(self, new_coords, description, step_number):
        """Test the adjusted coordinate."""
        x, y = new_coords
        print(f"\n   🧪 Testing adjusted coordinate: ({x}, {y})")
        
        # Quick test
        print("   Testing in: 2", end="", flush=True)
        time.sleep(0.5)
        print("...1", end="", flush=True)
        time.sleep(0.5)
        print("...CLICK!", flush=True)
        
        self.automation.click(x, y)
        
        result = input("   ✅ Is this correct now? (y/n): ").lower().strip()
        if result == 'y':
            self.tested_coordinates.append((new_coords, description, 'adjusted'))
            print(f"   ✅ {description} updated to ({x}, {y})")
            return new_coords
        else:
            print("   🔄 Let's try again...")
            return self.adjust_coordinates(new_coords, description, step_number)
    
    def manual_click_mode(self, description, step_number):
        """Let user manually click to set coordinates."""
        print(f"\n   👆 Manual Click Mode for: {description}")
        print("   Click exactly where the coordinate should be...")
        
        # Start recording to capture the click
        self.automation.start_recording()
        input("   Press Enter after you've clicked the correct location...")
        actions = self.automation.stop_recording()
        
        # Extract the last click
        click_actions = [a for a in actions if a['type'] == 'click']
        if click_actions:
            new_coords = (click_actions[-1]['x'], click_actions[-1]['y'])
            print(f"   📍 Captured coordinate: {new_coords}")
            
            confirm = input("   Use this coordinate? (y/n): ").lower().strip()
            if confirm == 'y':
                self.tested_coordinates.append((new_coords, description, 'manual'))
                return new_coords
        
        print("   ❌ No valid click captured, returning to adjustment menu...")
        return self.adjust_coordinates((0, 0), description, step_number)
    
    def replay_last_steps(self, current_step):
        """Replay the last 2 steps."""
        if len(self.step_history) < 2:
            print("   ❌ Not enough steps to replay")
            return None
            
        print(f"\n   ⏪ Replaying last 2 steps...")
        
        # Get the last 2 steps
        recent_steps = self.step_history[-2:]
        
        for step_info in recent_steps:
            print(f"\n   🔄 Replaying: {step_info['description']}")
            coords = self.test_coordinate_fast(
                step_info['coords'], 
                step_info['description'], 
                step_info['step']
            )
            step_info['coords'] = coords  # Update with any changes
            
        return recent_steps[-1]['coords']
    
    def show_step_history(self):
        """Display the history of tested steps."""
        print(f"\n   📋 Step History:")
        if not self.step_history:
            print("   No steps recorded yet")
            return
            
        for step in self.step_history:
            status_emoji = "✅" if step['status'] == 'correct' else "🔄"
            print(f"   {status_emoji} Step {step['step']}: {step['description']} - {step['coords']}")
    
    def test_workflow_buttons_fast(self):
        """Test workflow buttons with enhanced speed and features."""
        print("🚀 Enhanced Workflow Button Calibration")
        print("=" * 45)
        
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
            
        print("✅ Window focused!")
        print("\n🎯 Fast Testing Mode:")
        print("   - Auto-countdown before each click")
        print("   - Quick verification options")
        print("   - Replay functionality available")
        
        # Workflow coordinates to test
        workflow_coords = [
            ((530, 114), "Canvas button"),
            ((30, 195), "Upload button"),
            ((520, 647), "Use it button"),
            ((232, 636), "Next button"),
            ((1000, 447), "Size input area"),
            ((1000, 120), "First confirmation button"),
            ((900, 125), "Second confirmation button"),
            ((25, 47), "Back button")
        ]
        
        verified_coords = {}
        
        for i, (coords, description) in enumerate(workflow_coords, 1):
            result_coords = self.test_coordinate_fast(coords, description, i)
            verified_coords[description] = result_coords
            
            # Optional pause between steps
            if i < len(workflow_coords):
                continue_choice = input(f"\n   Continue to next step? (y/n/p for pause): ").lower().strip()
                if continue_choice == 'n':
                    break
                elif continue_choice == 'p':
                    pause_time = input("   Pause duration in seconds (default 5): ").strip()
                    try:
                        pause_time = int(pause_time) if pause_time else 5
                        print(f"   ⏸️  Pausing for {pause_time} seconds... (great time for ads! 📺)")
                        time.sleep(pause_time)
                    except ValueError:
                        time.sleep(5)
        
        # Summary
        self.display_final_summary(verified_coords)
        return True
    
    def test_grid_positions_fast(self, num_positions=6):
        """Test grid positions with enhanced features."""
        print("\n🔲 Enhanced Grid Position Testing")
        print("=" * 35)
        
        # Grid configuration
        base_x, base_y = 404, 180
        spacing_x, spacing_y = 77, 70
        images_per_row = 4
        
        verified_coords = {}
        
        for i in range(1, num_positions + 1):
            # Calculate grid position
            index = i - 1
            row = index // images_per_row
            col = index % images_per_row
            
            # Calculate coordinates
            x = base_x + (col * spacing_x)
            y = base_y + (row * spacing_y)
            
            description = f"Image {i} (Row {row+1}, Col {col+1})"
            result_coords = self.test_coordinate_fast((x, y), description, i)
            verified_coords[f"image_{i}"] = result_coords
        
        # Calculate new spacing based on verified coordinates
        self.calculate_improved_spacing(verified_coords)
        return True
    
    def calculate_improved_spacing(self, grid_coords):
        """Calculate improved spacing from verified coordinates."""
        print(f"\n📐 Improved Spacing Calculation")
        print("=" * 35)
        
        if len(grid_coords) < 2:
            print("❌ Need at least 2 grid positions for spacing calculation")
            return
            
        # Extract coordinates for calculation
        coords_list = [(k, v) for k, v in grid_coords.items()]
        
        # Calculate horizontal spacing
        horizontal_spacings = []
        for i in range(len(coords_list)):
            for j in range(i+1, len(coords_list)):
                # Parse image numbers
                img1_num = int(coords_list[i][0].split('_')[1])
                img2_num = int(coords_list[j][0].split('_')[1])
                
                # Check if same row
                row1 = (img1_num - 1) // 4
                row2 = (img2_num - 1) // 4
                
                if row1 == row2 and abs(img1_num - img2_num) == 1:
                    x1, y1 = coords_list[i][1]
                    x2, y2 = coords_list[j][1]
                    spacing = abs(x2 - x1)
                    horizontal_spacings.append(spacing)
        
        if horizontal_spacings:
            avg_h_spacing = sum(horizontal_spacings) / len(horizontal_spacings)
            print(f"📊 Average horizontal spacing: {avg_h_spacing:.1f}px")
        
        # Find base coordinates (image 1)
        if 'image_1' in grid_coords:
            base_x, base_y = grid_coords['image_1']
            print(f"📍 Verified base coordinates: ({base_x}, {base_y})")
    
    def display_final_summary(self, coords_dict):
        """Display final summary with copy-paste ready code."""
        print(f"\n🎉 Calibration Complete!")
        print("=" * 50)
        
        print(f"\n📊 Summary:")
        print(f"   ✅ Total coordinates tested: {len(coords_dict)}")
        print(f"   🔧 Adjustments made: {len([c for c in self.tested_coordinates if c[2] == 'adjusted'])}")
        print(f"   👆 Manual clicks: {len([c for c in self.tested_coordinates if c[2] == 'manual'])}")
        
        print(f"\n🔧 Updated Coordinate Configuration:")
        print("```python")
        print("# Updated coordinates from calibration")
        print("coordinates = {")
        for desc, coords in coords_dict.items():
            key = desc.lower().replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
            print(f"    '{key}': {coords},")
        print("}")
        print("```")
        
        # Save to file
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"calibration_results_{timestamp}.py"
        
        with open(filename, 'w') as f:
            f.write("# Calibration Results\n")
            f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("coordinates = {\n")
            for desc, coords in coords_dict.items():
                key = desc.lower().replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
                f.write(f"    '{key}': {coords},\n")
            f.write("}\n")
        
        print(f"\n💾 Results saved to: {filename}")

if __name__ == "__main__":
    calibrator = EnhancedGridCalibration()
    
    print("🚀 Enhanced Grid Calibration Tool")
    print("=" * 40)
    print("Features:")
    print("   ⚡ Fast progression with countdown")
    print("   🔄 Replay last 2 steps") 
    print("   📋 Step history tracking")
    print("   🔧 X/Y coordinate adjustment")
    print("   👆 Manual click mode")
    print("   ⏸️  Optional pauses (ad breaks!)")
    
    print("\nChoose test mode:")
    print("1. Test workflow buttons")
    print("2. Test grid positions")
    print("3. Test both")
    
    choice = input("\nChoice (1-3): ").strip()
    
    if choice == "1":
        calibrator.test_workflow_buttons_fast()
    elif choice == "2":
        num = input("How many grid positions to test? (default 6): ").strip()
        try:
            num = int(num) if num else 6
        except ValueError:
            num = 6
        calibrator.test_grid_positions_fast(num)
    elif choice == "3":
        calibrator.test_workflow_buttons_fast()
        if input("\nContinue to grid testing? (y/n): ").lower().strip() == 'y':
            num = input("How many grid positions to test? (default 6): ").strip()
            try:
                num = int(num) if num else 6
            except ValueError:
                num = 6
            calibrator.test_grid_positions_fast(num)
    else:
        print("Invalid choice, starting workflow button test...")
        calibrator.test_workflow_buttons_fast()
