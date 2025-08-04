#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation
from utils import load_config, save_config
import time
import cv2

class AdvancedAutomation:
    def __init__(self):
        self.config = load_config()
        self.automation = iPhoneAutomation(failsafe=self.config['failsafe'])
        self.screenshot_count = 0
        
    def save_screenshot(self, name=None):
        screenshot = self.automation.screenshot()
        if name is None:
            name = f"screenshot_{self.screenshot_count}"
        
        os.makedirs(self.config['screenshot_dir'], exist_ok=True)
        filepath = os.path.join(self.config['screenshot_dir'], f"{name}.png")
        cv2.imwrite(filepath, screenshot)
        
        self.screenshot_count += 1
        print(f"Screenshot saved: {filepath}")
        return filepath
    
    def swipe_pattern(self, pattern):
        patterns = {
            'unlock': [(200, 600, 200, 200)],
            'refresh': [(200, 200, 200, 400)],
            'back': [(50, 300, 200, 300)],
            'home': [(200, 650, 200, 600)]
        }
        
        if pattern in patterns:
            for swipe in patterns[pattern]:
                self.automation.swipe(*swipe, duration=self.config['swipe_duration'])
                time.sleep(self.config['default_delay'])
    
    def multi_tap(self, coordinates, delay=0.1):
        for x, y in coordinates:
            self.automation.click(x, y)
            time.sleep(delay)
    
    def type_with_autocorrect(self, text, accept_suggestions=True):
        self.automation.type_text(text)
        time.sleep(0.5)
        
        if accept_suggestions:
            self.automation.press_key('space')
            time.sleep(0.2)
    
    def find_and_click_text(self, text_image_path):
        for attempt in range(self.config['retry_attempts']):
            coords = self.automation.find_element(text_image_path)
            if coords:
                self.automation.click(coords[0], coords[1])
                return True
            
            time.sleep(self.config['retry_delay'])
        
        return False
    
    def scroll_until_found(self, element_path, max_scrolls=10):
        center_x = self.automation.window_bounds['width'] // 2
        center_y = self.automation.window_bounds['height'] // 2
        
        for i in range(max_scrolls):
            if self.automation.find_element(element_path):
                return True
            
            self.automation.scroll(center_x, center_y, clicks=-3)
            time.sleep(0.5)
        
        return False

def demo_advanced_features():
    print("Advanced iPhone Automation Demo")
    print("=" * 40)
    
    adv = AdvancedAutomation()
    
    if not adv.automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return
    
    print("\n1. Taking and saving screenshot...")
    adv.save_screenshot("demo_start")
    
    print("\n2. Performing swipe patterns...")
    print("   - Refresh swipe")
    adv.swipe_pattern('refresh')
    time.sleep(1)
    
    print("\n3. Multi-tap demonstration...")
    print("   - Tapping 3 locations")
    taps = [
        (100, 100),
        (200, 200),
        (300, 300)
    ]
    adv.multi_tap(taps, delay=0.5)
    
    print("\n4. Advanced text input...")
    print("   - Type with autocorrect")
    
    print("\nDemo completed!")
    print(f"Screenshots saved in: {adv.config['screenshot_dir']}")

def interactive_mode():
    adv = AdvancedAutomation()
    
    if not adv.automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return
    
    print("\nInteractive Advanced Automation Mode")
    print("Commands: swipe [pattern], tap [x] [y], type [text], screenshot, quit")
    
    while True:
        cmd = input("\n> ").strip().split()
        
        if not cmd:
            continue
            
        action = cmd[0].lower()
        
        if action == 'quit':
            break
        elif action == 'swipe' and len(cmd) > 1:
            adv.swipe_pattern(cmd[1])
        elif action == 'tap' and len(cmd) > 2:
            x, y = int(cmd[1]), int(cmd[2])
            adv.automation.click(x, y)
        elif action == 'type' and len(cmd) > 1:
            text = ' '.join(cmd[1:])
            adv.type_with_autocorrect(text)
        elif action == 'screenshot':
            adv.save_screenshot()
        else:
            print("Unknown command or invalid syntax")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Advanced iPhone Automation')
    parser.add_argument('--demo', action='store_true', help='Run demo')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    if args.demo:
        demo_advanced_features()
    elif args.interactive:
        interactive_mode()
    else:
        print("Use --demo or --interactive flag")
        parser.print_help()