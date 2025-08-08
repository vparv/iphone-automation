#!/usr/bin/env python3

import sys
import os
import time
import subprocess
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gallery_navigator import GalleryNavigator

class BatchProcessor:
    def __init__(self):
        self.navigator = GalleryNavigator()
        self.core_script = "recordings/liene_workflow_20250808_044610.py"
        self.max_images = 20  # Default maximum images to process
        self.delay_between_cycles = 1.2  # Seconds to wait between cycles (slowed 20% for stability)
        
    def run_core_workflow(self):
        """Run the core workflow script."""
        print("🔄 Running core workflow...")
        try:
            result = subprocess.run([
                sys.executable, self.core_script
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Core workflow completed successfully")
                return True
            else:
                print(f"❌ Core workflow failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Core workflow timed out")
            return False
        except Exception as e:
            print(f"❌ Error running core workflow: {e}")
            return False
    
    def setup_initial_state(self, reset_position=True):
        """Setup the initial state for batch processing."""
        print("🚀 Setting up batch processing...")
        
        if reset_position:
            # Reset gallery position to start from first image
            self.navigator.reset_state()
        else:
            # Keep current gallery position
            row, col = self.navigator.load_state()
            print(f"📍 Keeping current position: Row {row + 1}, Column {col + 1}")
        
        # Navigate to gallery
        if not self.navigator.navigate_to_gallery():
            print("❌ Failed to navigate to gallery")
            return False
        
        print("✅ Initial setup completed")
        return True
    
    def process_single_cycle(self, cycle_num):
        """Process a single image through the complete cycle."""
        print(f"\n🔄 === CYCLE {cycle_num} ===")
        print(f"⏰ Timestamp: {time.strftime('%H:%M:%S')}")
        
        # Step 0: Ensure we're at the gallery (except for first cycle)
        if cycle_num > 1:
            print(f"🔄 Step 0: Ensuring we're back at gallery for cycle {cycle_num}...")
            if not self.navigator.navigate_to_gallery():
                print("❌ Failed to navigate back to gallery")
                return False
            print("✅ Back at gallery - ready for next image selection")
            time.sleep(1.0)  # Extra wait to ensure gallery is loaded
        
        # Step 1: Select next image from gallery
        print(f"📸 Step 1: Selecting next image from gallery...")
        print(f"🔍 Looking for next image in sequence...")
        if not self.navigator.select_next_image():
            print("❌ Failed to select image")
            return False
        
        # Wait for UI to respond
        print(f"⏳ Waiting {self.delay_between_cycles}s for UI response between steps...")
        time.sleep(self.delay_between_cycles)
        
        # Step 2: Run core workflow
        print(f"⚙️  Step 2: Running core workflow on selected image...")
        print(f"🚀 Launching core automation script...")
        if not self.run_core_workflow():
            print("❌ Core workflow failed")
            # Try to recover by going back to gallery
            print("🔄 Attempting recovery - navigating back to gallery...")
            self.navigator.navigate_to_gallery()
            return False
        
        # Step 3: Verify we're ready for next cycle
        print(f"🔍 Step 3: Preparing for next cycle...")
        time.sleep(self.delay_between_cycles)
        
        print(f"✅ Cycle {cycle_num} completed successfully!")
        print(f"⏰ Cycle end time: {time.strftime('%H:%M:%S')}")
        return True
    
    def run_batch_processing(self, num_images=None, reset_position=True):
        """Run the complete batch processing cycle."""
        if num_images is None:
            num_images = self.max_images
        
        print(f"🎬 Starting Batch Processing")
        print(f"📊 Target: {num_images} images")
        if not reset_position:
            row, col = self.navigator.load_state()
            print(f"📍 Starting from: Row {row + 1}, Column {col + 1}")
        print("=" * 40)
        
        # Initial setup
        if not self.setup_initial_state(reset_position):
            return False
        
        successful_cycles = 0
        failed_cycles = 0
        
        for cycle in range(1, num_images + 1):
            try:
                if self.process_single_cycle(cycle):
                    successful_cycles += 1
                else:
                    failed_cycles += 1
                    print(f"⚠️  Cycle {cycle} failed, continuing...")
                    
                    # Try to recover by navigating back to gallery
                    print("🔄 Attempting recovery...")
                    if not self.navigator.navigate_to_gallery():
                        print("❌ Recovery failed, stopping batch processing")
                        break
                        
            except KeyboardInterrupt:
                print(f"\n⏹️  Batch processing stopped by user at cycle {cycle}")
                break
            except Exception as e:
                print(f"❌ Unexpected error in cycle {cycle}: {e}")
                failed_cycles += 1
        
        # Final summary
        print(f"\n📊 Batch Processing Summary")
        print("=" * 30)
        print(f"✅ Successful cycles: {successful_cycles}")
        print(f"❌ Failed cycles: {failed_cycles}")
        total_cycles = successful_cycles + failed_cycles
        if total_cycles > 0:
            print(f"📈 Success rate: {successful_cycles/total_cycles*100:.1f}%")
        else:
            print("📈 Success rate: N/A (no cycles completed)")
        
        return successful_cycles > 0
    
    def run_interactive_mode(self):
        """Run in interactive mode for testing."""
        print("🎮 Interactive Batch Processor")
        print("=" * 35)
        
        while True:
            print("\nChoose an action:")
            print("1. Setup initial state")
            print("2. Select next image")
            print("3. Run core workflow")
            print("4. Process single cycle")
            print("5. Run batch processing")
            print("6. Show grid preview")
            print("7. Reset gallery position")
            print("8. Exit")
            
            choice = input("\nEnter choice (1-8): ").strip()
            
            if choice == "1":
                self.setup_initial_state()
            elif choice == "2":
                self.navigator.select_next_image()
            elif choice == "3":
                self.run_core_workflow()
            elif choice == "4":
                cycle_num = len([f for f in os.listdir('.') if f.startswith('cycle_')]) + 1
                self.process_single_cycle(cycle_num)
            elif choice == "5":
                try:
                    num = int(input("Enter number of images to process: "))
                    self.run_batch_processing(num)
                except ValueError:
                    print("❌ Invalid number")
            elif choice == "6":
                self.navigator.show_grid_preview()
            elif choice == "7":
                self.navigator.reset_state()
            elif choice == "8":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")

def main():
    processor = BatchProcessor()
    
    print("🤖 Liene Photo HD Batch Processor")
    print("=" * 40)
    print("This script coordinates between:")
    print("📸 Gallery Navigator (selects images)")
    print("⚙️  Core Workflow (processes images)")
    print()
    
    if len(sys.argv) > 1:
        # Command line mode
        try:
            num_images = int(sys.argv[1])
            processor.run_batch_processing(num_images)
        except ValueError:
            print("❌ Invalid number of images")
    else:
        # Interactive mode
        processor.run_interactive_mode()

if __name__ == "__main__":
    main()
