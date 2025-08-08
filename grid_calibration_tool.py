#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

class GridCalibrationTool:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        
    def test_click_coordinates(self, coordinates_list, description_list):
        """Test a list of coordinates by clicking them with visual feedback."""
        print("🎯 Grid Calibration Tool")
        print("=" * 40)
        
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
            
        print("✅ Window focused!")
        print("\nTesting coordinates...")
        print("Watch the screen to verify clicks are hitting the right targets.")
        
        for i, (coords, desc) in enumerate(zip(coordinates_list, description_list)):
            x, y = coords
            print(f"\n{i+1}. Testing {desc} at ({x}, {y})")
            input("   Press Enter to click this coordinate...")
            
            self.automation.click(x, y)
            time.sleep(0.5)
            
            result = input("   Did the click hit the correct target? (y/n): ").lower().strip()
            if result != 'y':
                print(f"   ❌ Coordinate ({x}, {y}) needs adjustment for {desc}")
                new_x = input(f"   Enter correct X coordinate (current: {x}): ").strip()
                new_y = input(f"   Enter correct Y coordinate (current: {y}): ").strip()
                
                if new_x and new_y:
                    try:
                        new_x, new_y = int(new_x), int(new_y)
                        print(f"   📝 Suggested update: {desc} = ({new_x}, {new_y})")
                    except ValueError:
                        print("   ❌ Invalid coordinates entered")
            else:
                print(f"   ✅ {desc} coordinate verified!")
        
        print("\n🎉 Calibration test completed!")
        return True
    
    def test_grid_positions(self, num_positions=6):
        """Test the first few grid positions to verify spacing."""
        print("\n🔲 Testing Grid Positions")
        print("=" * 30)
        
        # Grid configuration from the improved automation
        base_x, base_y = 404, 180
        spacing_x, spacing_y = 77, 70
        images_per_row = 4
        
        coordinates = []
        descriptions = []
        
        for i in range(1, num_positions + 1):
            # Calculate grid position
            index = i - 1
            row = index // images_per_row
            col = index % images_per_row
            
            # Calculate coordinates
            x = base_x + (col * spacing_x)
            y = base_y + (row * spacing_y)
            
            coordinates.append((x, y))
            descriptions.append(f"Image {i} (Row {row+1}, Col {col+1})")
        
        return self.test_click_coordinates(coordinates, descriptions)
    
    def test_workflow_buttons(self):
        """Test all the workflow button coordinates."""
        print("\n🔘 Testing Workflow Buttons")
        print("=" * 30)
        
        # Button coordinates from the improved automation
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
        
        coordinates = [coord for coord, _ in workflow_coords]
        descriptions = [desc for _, desc in workflow_coords]
        
        return self.test_click_coordinates(coordinates, descriptions)
    
    def run_full_calibration(self):
        """Run complete calibration of all coordinates."""
        print("🚀 Starting Full Calibration")
        print("=" * 50)
        print("This tool will help you verify and adjust all click coordinates.")
        print("Make sure Liene Photo HD is open and ready.")
        
        input("\nPress Enter to continue...")
        
        # Test workflow buttons first
        if input("\nTest workflow buttons? (y/n): ").lower().strip() == 'y':
            self.test_workflow_buttons()
        
        # Test grid positions
        if input("\nTest grid positions? (y/n): ").lower().strip() == 'y':
            num_positions = input("How many grid positions to test? (default: 6): ").strip()
            try:
                num_positions = int(num_positions) if num_positions else 6
            except ValueError:
                num_positions = 6
            
            self.test_grid_positions(num_positions)
        
        print("\n✅ Calibration completed!")
        print("Use the suggested coordinates to update your automation scripts.")

if __name__ == "__main__":
    tool = GridCalibrationTool()
    tool.run_full_calibration()
