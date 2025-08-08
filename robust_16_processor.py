#!/usr/bin/env python3

import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from batch_processor import BatchProcessor

class Robust16Processor:
    def __init__(self):
        self.processor = BatchProcessor()
        self.max_retries = 3
        self.results = {}
        
    def process_specific_image(self, image_num, max_attempts=3):
        """Process a specific image number with retry logic."""
        print(f"\n🎯 === PROCESSING IMAGE #{image_num} ===")
        
        # Calculate position for this image (1-indexed to 0-indexed)
        row = (image_num - 1) // 4
        col = (image_num - 1) % 4
        
        for attempt in range(1, max_attempts + 1):
            print(f"🔄 Attempt {attempt}/{max_attempts} for Image #{image_num}")
            print(f"📍 Setting position: Row {row + 1}, Column {col + 1}")
            
            try:
                # Set exact position for this image
                self.processor.navigator.save_state(row, col)
                
                # Navigate to gallery
                print("📂 Navigating to gallery...")
                if not self.processor.navigator.navigate_to_gallery():
                    print(f"❌ Attempt {attempt}: Failed to navigate to gallery")
                    time.sleep(2)
                    continue
                
                # Select the specific image
                print(f"🖱️  Selecting Image #{image_num}...")
                if not self.processor.navigator.select_next_image():
                    print(f"❌ Attempt {attempt}: Failed to select image")
                    time.sleep(2)
                    continue
                
                # Wait for selection
                time.sleep(1.5)
                
                # Run workflow
                print(f"⚙️  Running workflow for Image #{image_num}...")
                if not self.processor.run_core_workflow():
                    print(f"❌ Attempt {attempt}: Core workflow failed")
                    time.sleep(3)
                    continue
                
                # Success!
                print(f"✅ Image #{image_num} completed successfully!")
                self.results[image_num] = "SUCCESS"
                return True
                
            except Exception as e:
                print(f"❌ Attempt {attempt}: Exception occurred: {e}")
                time.sleep(3)
                continue
        
        # All attempts failed
        print(f"❌ Image #{image_num} FAILED after {max_attempts} attempts")
        self.results[image_num] = "FAILED"
        return False
    
    def run_all_16_images(self):
        """Process all 16 images with robust error handling."""
        print("🚀 Starting Robust 16-Image Processing")
        print("=" * 50)
        
        start_time = time.time()
        successful = 0
        failed = 0
        
        # Process each image individually
        for image_num in range(1, 17):
            print(f"\n📊 Progress: {image_num-1}/16 completed")
            
            if self.process_specific_image(image_num):
                successful += 1
                print(f"✅ Image #{image_num}: SUCCESS")
            else:
                failed += 1
                print(f"❌ Image #{image_num}: FAILED")
                
                # Ask user if they want to continue
                print(f"\n⚠️  Image #{image_num} failed. Do you want to:")
                print("1. Continue to next image")
                print("2. Retry this image")
                print("3. Stop processing")
                
                try:
                    choice = input("Enter choice (1/2/3): ").strip()
                    if choice == "2":
                        # Retry this image
                        image_num -= 1  # Will be incremented by loop
                        failed -= 1    # Don't count this failure yet
                        continue
                    elif choice == "3":
                        print("🛑 Processing stopped by user")
                        break
                    # Default: continue to next image
                except:
                    print("🔄 Continuing to next image...")
            
            # Small delay between images
            time.sleep(1)
        
        # Final summary
        total_time = time.time() - start_time
        print(f"\n📊 FINAL SUMMARY")
        print("=" * 30)
        print(f"✅ Successful images: {successful}")
        print(f"❌ Failed images: {failed}")
        print(f"📈 Success rate: {successful/16*100:.1f}%")
        print(f"⏰ Total time: {total_time/60:.1f} minutes")
        
        # Detailed results
        print(f"\n📋 Detailed Results:")
        for i in range(1, 17):
            status = self.results.get(i, "NOT_PROCESSED")
            print(f"Image #{i:2d}: {status}")
        
        return successful == 16

def main():
    processor = Robust16Processor()
    
    print("🤖 Robust 16-Image Processor")
    print("=" * 35)
    print("This will process images 1-16 with:")
    print("• Individual image processing")
    print("• Automatic retry on failures") 
    print("• Robust error recovery")
    print("• Detailed progress tracking")
    
    input("\nPress Enter to start processing...")
    
    processor.run_all_16_images()

if __name__ == "__main__":
    main()
