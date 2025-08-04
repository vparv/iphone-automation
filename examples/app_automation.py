#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iphone_automation import iPhoneAutomation
import time

def open_messages_app(automation):
    print("Opening Messages app...")
    
    center_x = automation.window_bounds['width'] // 2
    bottom_y = automation.window_bounds['height'] - 50
    
    automation.swipe(center_x, bottom_y, center_x, 100, duration=0.3)
    time.sleep(1)
    
    print("Typing 'Messages' in search...")
    automation.type_text("Messages")
    time.sleep(1)
    
    automation.click(center_x, 200)
    time.sleep(2)

def send_message(automation, contact_name, message):
    print(f"Sending message to {contact_name}...")
    
    automation.click(automation.window_bounds['width'] - 50, 100)
    time.sleep(1)
    
    automation.type_text(contact_name)
    time.sleep(1)
    
    automation.click(automation.window_bounds['width'] // 2, 200)
    time.sleep(1)
    
    message_y = automation.window_bounds['height'] - 100
    automation.click(automation.window_bounds['width'] // 2, message_y)
    time.sleep(0.5)
    
    automation.type_text(message)
    time.sleep(0.5)
    
    automation.click(automation.window_bounds['width'] - 50, message_y)
    print("Message sent!")

def navigate_settings(automation):
    print("Opening Settings app...")
    
    automation.hotkey('cmd', 'space')
    time.sleep(0.5)
    automation.type_text("Settings")
    time.sleep(1)
    automation.press_key('enter')
    time.sleep(2)
    
    print("Scrolling through settings...")
    center_x = automation.window_bounds['width'] // 2
    center_y = automation.window_bounds['height'] // 2
    
    for i in range(3):
        automation.scroll(center_x, center_y, clicks=-5)
        time.sleep(1)

def main():
    print("iPhone App Automation Demo")
    print("=" * 40)
    
    automation = iPhoneAutomation()
    
    print("Looking for iPhone Mirroring window...")
    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        return
    
    print("Window found and focused!")
    time.sleep(1)
    
    while True:
        print("\nChoose an action:")
        print("1. Open Messages app")
        print("2. Send a test message")
        print("3. Navigate Settings")
        print("4. Custom automation")
        print("0. Exit")
        
        choice = input("\nEnter choice (0-4): ")
        
        if choice == '0':
            break
        elif choice == '1':
            open_messages_app(automation)
        elif choice == '2':
            contact = input("Enter contact name: ")
            message = input("Enter message: ")
            send_message(automation, contact, message)
        elif choice == '3':
            navigate_settings(automation)
        elif choice == '4':
            print("\nCustom automation example:")
            print("You can add your own automation sequences here")
            x = int(input("Enter X coordinate: "))
            y = int(input("Enter Y coordinate: "))
            automation.click(x, y)
        else:
            print("Invalid choice")
        
        time.sleep(1)
    
    print("\nAutomation completed!")

if __name__ == "__main__":
    main()