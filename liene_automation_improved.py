#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

class ImprovedLienePhotoAutomation:
    def __init__(self):
        self.automation = iPhoneAutomation()
        self.automation.window_title = "Liene Photo HD"
        
        # Grid configuration - updated based on recorded session analysis
        self.grid_config = {
            'base_x': 404,        # First image X coordinate
            'base_y': 180,        # First image Y coordinate  
            'spacing_x': 77,      # Horizontal spacing between images
            'spacing_y': 70,      # Vertical spacing between rows
            'images_per_row': 4   # Number of images per row
        }
        
        # Workflow coordinates - based on recorded session
        self.coordinates = {
            'canvas_button': (530, 114),      # Canvas button (+ Canvas)
            'upload_button': (30, 195),       # Upload button in sidebar
            'use_it_button': (525, 710),      # "Use it" button
            'next_button': (232, 636),        # "Next" button  
            'size_input': (1000, 447),        # Size input area
            'confirm_button_1': (1000, 120),  # First confirmation
            'confirm_button_2': (900, 125),   # Second confirmation
            'back_button': (25, 47)           # Back arrow to return to main
        }
        
        # Timing configuration (adaptive)
        self.timing = {
            'click_delay': 1.5,
            'upload_wait': 2.0,
            'processing_wait': 3.0,
            'navigation_wait': 2.0,
            'input_delay': 0.5
        }
        
    def calculate_grid_position(self, image_number):
        """Calculate grid position for a given image number (1-based)."""
        index = image_number - 1  # Convert to 0-based
        row = index // self.grid_config['images_per_row']
        col = index % self.grid_config['images_per_row']
        return row, col
    
    def get_image_coordinates(self, row, col):
        """Calculate actual click coordinates for grid position."""
        x = self.grid_config['base_x'] + (col * self.grid_config['spacing_x'])
        y = self.grid_config['base_y'] + (row * self.grid_config['spacing_y'])
        return x, y
    
    def verify_window_focus(self):
        """Ensure window is focused and bounds are current."""
        if not self.automation.focus_window():
            raise Exception(f"Could not find '{self.automation.window_title}' window")
        print("✅ Window focused and ready")
        return True
    
    def click_with_verification(self, x, y, description="", wait_time=None):
        """Click with logging and optional wait time."""
        if wait_time is None:
            wait_time = self.timing['click_delay']
            
        print(f"   Clicking {description} at ({x}, {y})")
        self.automation.click(x, y)
        time.sleep(wait_time)
    
    def execute_workflow_step(self, step_name, coord_key, wait_time=None, description=""):
        """Execute a standard workflow step."""
        coords = self.coordinates[coord_key]
        desc = description or coord_key.replace('_', ' ').title()
        print(f"{step_name}: {desc}...")
        self.click_with_verification(coords[0], coords[1], desc, wait_time)
    
    def process_single_image(self, image_number):
        """
        Execute one complete loop of the workflow for a specific image.
        
        Args:
            image_number: 1-based image number to process
        """
        print(f"\n{'='*20} Processing Image {image_number} {'='*20}")
        
        # Calculate grid position
        row, col = self.calculate_grid_position(image_number)
        image_x, image_y = self.get_image_coordinates(row, col)
        
        print(f"Grid position: Row {row+1}, Column {col+1}")
        print(f"Target coordinates: ({image_x}, {image_y})")
        
        try:
            # STEP 1: Click Canvas button
            self.execute_workflow_step("Step 1", "canvas_button", 
                                     self.timing['click_delay'], "Canvas button")
            
            # STEP 2: Click Upload in sidebar  
            self.execute_workflow_step("Step 2", "upload_button",
                                     self.timing['upload_wait'], "Upload button")
            
            # STEP 3: Select specific image from grid (CRITICAL STEP)
            print(f"Step 3: Selecting image at grid position ({image_x}, {image_y})...")
            self.click_with_verification(image_x, image_y, f"Image {image_number}", 
                                       self.timing['click_delay'])
            
            # STEP 4: Click "Use it" button
            self.execute_workflow_step("Step 4", "use_it_button",
                                     self.timing['processing_wait'], "Use it button")
            
            # STEP 5: Handle sizing and confirmations
            print("Step 5: Handling size input and confirmations...")
            
            # Click size input area
            self.click_with_verification(self.coordinates['size_input'][0], 
                                       self.coordinates['size_input'][1],
                                       "Size input area", self.timing['input_delay'])
            
            # Clear and enter size value
            print("   Entering size value: 166")
            self.automation.press_key('backspace')
            self.automation.press_key('backspace') 
            self.automation.type_text('166')
            self.automation.press_key('enter')
            time.sleep(1.0)
            
            # Confirmation clicks
            self.execute_workflow_step("Step 5a", "confirm_button_1", 0.5, "First confirmation")
            self.execute_workflow_step("Step 5b", "confirm_button_2", 1.0, "Second confirmation")
            
            # STEP 6: Navigate back to start
            self.execute_workflow_step("Step 6", "back_button",
                                     self.timing['navigation_wait'], "Back to main")
            
            print(f"✅ Image {image_number} completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error processing image {image_number}: {e}")
            return False
    
    def run_batch_automation(self, total_images=10, start_image=1):
        """
        Run batch automation for multiple images.
        
        Args:
            total_images: Number of images to process
            start_image: Starting image number (for resuming)
        """
        print("🎨 Improved Liene Photo HD Batch Automation")
        print("=" * 60)
        
        # Verify setup
        print(f"\n📊 Batch Configuration:")
        print(f"   Total images: {total_images}")
        print(f"   Starting from: {start_image}")
        print(f"   Grid layout: {self.grid_config['images_per_row']} images per row")
        
        # Focus window
        print(f"\n🔍 Looking for '{self.automation.window_title}' window...")
        self.verify_window_focus()
        
        # Process images
        print(f"\n🚀 Starting automated processing...")
        start_time = time.time()
        successful_images = 0
        
        for image_num in range(start_image, start_image + total_images):
            try:
                if self.process_single_image(image_num):
                    successful_images += 1
                    
                # Progress update
                remaining = (start_image + total_images) - image_num - 1
                if remaining > 0:
                    print(f"\n📈 Progress: {image_num}/{start_image + total_images - 1} completed. {remaining} remaining.")
                    time.sleep(1)  # Brief pause between loops
                
            except KeyboardInterrupt:
                print(f"\n⏸️ Automation stopped by user at image {image_num}")
                break
            except Exception as e:
                print(f"❌ Critical error at image {image_num}: {e}")
                
                # Ask user what to do
                choice = input("Continue with next image? (y/n/r for retry): ").lower().strip()
                if choice == 'r':
                    print("🔄 Retrying current image...")
                    continue
                elif choice != 'y':
                    break
        
        # Summary
        elapsed_time = time.time() - start_time
        print(f"\n🎉 Batch automation completed!")
        print(f"✅ Successfully processed: {successful_images}/{total_images} images")
        print(f"⏱️ Total time: {elapsed_time:.1f} seconds")
        if successful_images > 0:
            print(f"📊 Average time per image: {elapsed_time/successful_images:.1f} seconds")
        
        return successful_images == total_images

if __name__ == "__main__":
    automation = ImprovedLienePhotoAutomation()
    
    # Run automation for 10 images
    automation.run_batch_automation(total_images=10)
