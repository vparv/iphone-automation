#!/usr/bin/env python3

import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gallery_navigator import GalleryNavigator

def debug_sequence():
    """Debug the gallery navigation sequence."""
    navigator = GalleryNavigator()
    
    print("🔍 Debug Gallery Navigation Sequence")
    print("=" * 45)
    
    # Reset to start fresh
    navigator.reset_state()
    
    # Show initial state
    row, col = navigator.load_state()
    print(f"📍 Initial state: Row {row + 1}, Column {col + 1}")
    
    # Test sequence of 5 selections
    for i in range(1, 6):
        print(f"\n--- Selection {i} ---")
        
        # Load state before selection
        row, col = navigator.load_state()
        x, y = navigator.calculate_image_position(row, col)
        
        print(f"🔢 State BEFORE: Row {row + 1}, Col {col + 1}")
        print(f"📍 Calculated coordinates: ({x}, {y})")
        
        # Make the selection (without actually clicking)
        print(f"🎯 Would click at ({x}, {y})")
        
        # Simulate the state update that should happen
        next_col = col + 1
        next_row = row
        if next_col >= 4:  # 4 images per row
            next_col = 0
            next_row += 1
        
        navigator.save_state(next_row, next_col)
        
        # Load state after selection
        new_row, new_col = navigator.load_state()
        print(f"🔢 State AFTER: Row {new_row + 1}, Col {new_col + 1}")
        
        time.sleep(1)
    
    print(f"\n📊 Final Summary:")
    print("Expected sequence:")
    print("1. Row 1, Col 1 → (426, 179)")
    print("2. Row 1, Col 2 → (498, 179)")  
    print("3. Row 1, Col 3 → (570, 179)")
    print("4. Row 1, Col 4 → (642, 179)")
    print("5. Row 2, Col 1 → (426, 259)")

if __name__ == "__main__":
    debug_sequence()
