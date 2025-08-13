#!/usr/bin/env python3

import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

class GalleryNavigator:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        
        # Grid layout configuration - 4 images per row
        self.images_per_row = 4
        self.base_x = 426  # From your recording: first image x-coordinate
        self.base_y = 179  # From your recording: first image y-coordinate
        
        # Calculate spacing based on 4-images-per-row layout
        # Assuming standard spacing in the gallery grid
        self.spacing_x = 72  # Horizontal spacing between images
        self.spacing_y = 80  # Vertical spacing between rows
        
        # State file to track current position
        self.state_file = "gallery_state.json"
        
    def load_state(self):
        """Load current gallery position state."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                return state.get('current_row', 0), state.get('current_col', 0)
            except:
                return 0, 0
        return 0, 0
    
    def save_state(self, row, col):
        """Save current gallery position state."""
        state = {
            'current_row': row,
            'current_col': col,
            'last_updated': time.time()
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def reset_state(self):
        """Reset to first image (0,0)."""
        self.save_state(0, 0)
        print("🔄 Gallery state reset to first image")
    
    def calculate_image_position(self, row, col):
        """Calculate x,y coordinates for given row/column."""
        x = self.base_x + (col * self.spacing_x)
        y = self.base_y + (row * self.spacing_y)
        return x, y
    
    def select_next_image(self):
        """Select the next image in sequence (left-to-right, top-to-bottom)."""
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
        
        # Load current position
        current_row, current_col = self.load_state()
        
        print(f"📍 Current position: Row {current_row + 1}, Column {current_col + 1}")
        
        # Calculate coordinates for current image
        x, y = self.calculate_image_position(current_row, current_col)
        
        print(f"🎯 Clicking image at ({x}, {y}) - Gallery position Row {current_row + 1}, Col {current_col + 1}")
        
        try:
            # Click the image
            print(f"🖱️  Executing click at coordinates ({x}, {y})")
            self.automation.click(x, y)
            print("✅ Image click executed - waiting for selection response...")
            time.sleep(1.2)  # Slowed 20% for stability
            
            # Move to next position
            next_col = current_col + 1
            next_row = current_row
            
            # If we've reached the end of a row, move to next row
            if next_col >= self.images_per_row:
                next_col = 0
                next_row += 1
            
            # Save new position for next time
            self.save_state(next_row, next_col)
            
            print(f"✅ Selected image at Row {current_row + 1}, Column {current_col + 1}")
            print(f"📋 Next image will be: Row {next_row + 1}, Column {next_col + 1}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error selecting image: {e}")
            return False
    
    def select_specific_image(self, row, col):
        """Select a specific image by row/column (0-indexed)."""
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
        
        print(f"🎯 Selecting specific image: Row {row + 1}, Column {col + 1}")
        
        x, y = self.calculate_image_position(row, col)
        
        try:
            self.automation.click(x, y)
            time.sleep(1.2)  # Slowed 20% for stability
            
            # Update state to this position + 1 for next sequential call
            next_col = col + 1
            next_row = row
            if next_col >= self.images_per_row:
                next_col = 0
                next_row += 1
                
            self.save_state(next_row, next_col)
            
            print(f"✅ Selected image at ({x}, {y})")
            return True
            
        except Exception as e:
            print(f"❌ Error selecting image: {e}")
            return False
    
    def navigate_to_gallery(self):
        """Navigate to the gallery/recents view if not already there."""
        if not self.automation.focus_window():
            print("❌ Could not find Liene Photo HD window")
            return False
        
        print("📂 Navigating to gallery...")
        
        try:
            # Click Canvas button (from your recording)
            canvas_x, canvas_y = 517, 130
            self.automation.click(canvas_x, canvas_y)
            time.sleep(1.2)  # Slowed 20% for stability
            
            # Click Upload button (from your recording)
            upload_x, upload_y = 32, 210
            self.automation.click(upload_x, upload_y)
            time.sleep(1.8)  # Slowed 20% for stability
            
            print("✅ Successfully navigated to gallery")
            return True
            
        except Exception as e:
            print(f"❌ Error navigating to gallery: {e}")
            return False
    
    def show_grid_preview(self, rows=3, cols=4):
        """Show a preview of the grid positions without clicking."""
        print(f"\n📋 Gallery Grid Preview ({rows} rows × {cols} columns):")
        print("=" * 50)
        
        for row in range(rows):
            for col in range(cols):
                x, y = self.calculate_image_position(row, col)
                image_num = (row * cols) + col + 1
                print(f"Image {image_num:2d}: Row {row + 1}, Col {col + 1} → ({x:3.0f}, {y:3.0f})")
        
        print("=" * 50)
        current_row, current_col = self.load_state()
        current_image = (current_row * cols) + current_col + 1
        print(f"🎯 Next image to select: #{current_image} (Row {current_row + 1}, Col {current_col + 1})")

def main():
    navigator = GalleryNavigator()
    
    print("🖼️  Gallery Navigator")
    print("=" * 30)
    print("Choose an action:")
    print("1. Navigate to gallery")
    print("2. Select next image in sequence")
    print("3. Select specific image (row, col)")
    print("4. Show grid preview")
    print("5. Reset position to first image")
    print("6. Show current state")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == "1":
        navigator.navigate_to_gallery()
    elif choice == "2":
        navigator.select_next_image()
    elif choice == "3":
        try:
            row = int(input("Enter row (1-based): ")) - 1
            col = int(input("Enter column (1-based): ")) - 1
            navigator.select_specific_image(row, col)
        except ValueError:
            print("❌ Invalid input. Please enter numbers.")
    elif choice == "4":
        navigator.show_grid_preview()
    elif choice == "5":
        navigator.reset_state()
    elif choice == "6":
        row, col = navigator.load_state()
        print(f"📍 Current state: Row {row + 1}, Column {col + 1}")
        print(f"🎯 Next image coordinates: {navigator.calculate_image_position(row, col)}")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
