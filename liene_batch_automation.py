#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iphone_automation import iPhoneAutomation

def calculate_grid_position(image_number, images_per_row=4):
    """
    Calculate grid position for a given image number.
    
    Args:
        image_number: 1-based image number (1, 2, 3, ...)
        images_per_row: Number of images per row (default: 4)
    
    Returns:
        tuple: (row, col) where both are 0-based
    """
    # Convert to 0-based indexing
    index = image_number - 1
    row = index // images_per_row
    col = index % images_per_row
    return row, col

def get_image_coordinates(row, col, base_x=404, base_y=180, spacing_x=77, spacing_y=70):
    """
    Calculate actual click coordinates for grid position.
    
    Args:
        row: 0-based row number
        col: 0-based column number
        base_x: X coordinate of first image (top-left)
        base_y: Y coordinate of first image (top-left)
        spacing_x: Horizontal spacing between images
        spacing_y: Vertical spacing between images
    
    Returns:
        tuple: (x, y) coordinates
    """
    x = base_x + (col * spacing_x)
    y = base_y + (row * spacing_y)
    return x, y

def run_single_loop(automation, image_number):
    """
    Execute one complete loop of the workflow for a specific image.
    
    Args:
        automation: iPhoneAutomation instance
        image_number: 1-based image number to process
    """
    print(f"\n--- Processing Image {image_number} ---")
    
    # Calculate grid position
    row, col = calculate_grid_position(image_number)
    image_x, image_y = get_image_coordinates(row, col)
    
    print(f"Grid position: Row {row+1}, Column {col+1}")
    print(f"Click coordinates: ({image_x}, {image_y})")
    
    # WORKFLOW STEP 1: Click Canvas button
    print("1. Clicking Canvas button...")
    automation.click(530, 114)  # Canvas button (+ Canvas)
    time.sleep(1.5)
    
    # WORKFLOW STEP 2: Click Upload in sidebar
    print("2. Clicking Upload...")
    automation.click(30, 195)  # Upload button in left sidebar
    time.sleep(2.0)  # Wait for image picker to load
    
    # WORKFLOW STEP 3: Select specific image from grid (VARIABLE PART)
    print(f"3. Selecting image at position ({image_x}, {image_y})...")
    automation.click(image_x, image_y)
    time.sleep(1.5)
    
    # WORKFLOW STEP 4: Click "Use it" button
    print("4. Clicking 'Use it' button...")
    automation.click(520, 647)  # "Use it" button (moved up 40px)
    time.sleep(3.0)  # Wait for processing
    
    # WORKFLOW STEP 5: Click "Next" button
    print("5. Clicking 'Next' button...")
    automation.click(232, 636)  # "Next" button
    time.sleep(2.0)
    
    # WORKFLOW STEP 6: Handle any additional steps (sizing, etc.)
    # Based on your recording, there were some input fields and confirmations
    print("6. Handling final steps...")
    
    # Click somewhere to focus (if needed)
    automation.click(1000, 447)  # Size input area
    time.sleep(0.5)
    
    # Clear and enter size (from your recording: backspace, backspace, 1, 6, 6)
    automation.press_key('backspace')
    automation.press_key('backspace')
    automation.type_text('166')
    automation.press_key('enter')
    time.sleep(1.0)
    
    # Final confirmation clicks
    automation.click(1000, 120)  # Some confirmation button
    time.sleep(0.5)
    automation.click(900, 125)   # Another confirmation
    time.sleep(1.0)
    
    # Navigate back to start (click back arrow or home)
    automation.click(25, 47)     # Back arrow to return to main screen
    time.sleep(2.0)
    
    print(f"✅ Image {image_number} completed!")

def liene_batch_automation():
    """
    Main function to run batch automation for Liene Photo HD.
    """
    print("🎨 Liene Photo HD Batch Automation")
    print("=" * 50)
    
    # Set default to 10 images (no user input required)
    total_images = 10
    
    # Calculate grid information
    images_per_row = 4
    total_rows = (total_images + images_per_row - 1) // images_per_row  # Ceiling division
    last_row_images = total_images % images_per_row or images_per_row
    
    print(f"\n📊 Batch Information:")
    print(f"   Total images: {total_images}")
    print(f"   Grid layout: {images_per_row} images per row")
    print(f"   Total rows needed: {total_rows}")
    print(f"   Last row will have: {last_row_images} images")
    
    # Initialize automation
    automation = iPhoneAutomation()
    automation.window_title = "Liene Photo HD"
    
    print(f"\n🔍 Looking for '{automation.window_title}' window...")
    if not automation.focus_window():
        print(f"❌ Error: Could not find '{automation.window_title}' window")
        print("Make sure Liene Photo HD is running and visible")
        return False
    
    print("✅ Window found and focused!")
    
    # Auto-start without confirmation
    print(f"\n🚀 Starting automated processing of {total_images} images...")
    
    # Process each image
    start_time = time.time()
    
    for image_num in range(1, total_images + 1):
        try:
            run_single_loop(automation, image_num)
            
            # Progress update
            remaining = total_images - image_num
            if remaining > 0:
                print(f"📈 Progress: {image_num}/{total_images} completed. {remaining} remaining.")
                time.sleep(1)  # Brief pause between loops
            
        except KeyboardInterrupt:
            print(f"\n⏸️ Automation stopped by user at image {image_num}")
            break
        except Exception as e:
            print(f"❌ Error processing image {image_num}: {e}")
            
            # Ask user what to do
            while True:
                choice = input("Continue with next image? (y/n): ").lower().strip()
                if choice in ['y', 'yes']:
                    break
                elif choice in ['n', 'no']:
                    return False
                else:
                    print("Please enter 'y' or 'n'")
    
    # Summary
    elapsed_time = time.time() - start_time
    print(f"\n🎉 Batch automation completed!")
    print(f"⏱️ Total time: {elapsed_time:.1f} seconds")
    print(f"📊 Average time per image: {elapsed_time/total_images:.1f} seconds")
    
    return True

if __name__ == "__main__":
    liene_batch_automation()
