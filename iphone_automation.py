import pyautogui
import time
import cv2
import numpy as np
import json
from typing import Optional, Tuple, List, Dict, Any
from utils import find_iphone_window, get_window_bounds, wait_for_element, activate_window
from Quartz import CGEventCreateScrollWheelEvent, CGEventPost, kCGHIDEventTap, CGPointMake
from pynput import mouse, keyboard
from datetime import datetime

class iPhoneAutomation:
    def __init__(self, failsafe: bool = True):
        pyautogui.FAILSAFE = failsafe
        pyautogui.PAUSE = 0.1
        
        self.window_bounds = None
        self.window_title = "iPhone Mirroring"
        self.app_name = None
        
        # Recording system
        self.recording = False
        self.recorded_actions = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Scroll aggregation for continuous scroll detection
        self.scroll_buffer = []
        self.last_scroll_time = 0
        self.scroll_timeout = 0.5  # Time to wait before ending a scroll sequence
        
    def focus_window(self) -> bool:
        window = find_iphone_window(self.window_title)
        if window:
            self.window_bounds = get_window_bounds(window)
            self.app_name = window['app']
            activate_window(window['app'])
            return True
        return False
    
    def _ensure_focus(self) -> None:
        """Ensure the iPhone Mirroring window is focused before performing actions"""
        if self.app_name:
            activate_window(self.app_name)
    
    def _to_absolute_coords(self, x: int, y: int) -> Tuple[int, int]:
        if not self.window_bounds:
            raise Exception("Window not focused. Call focus_window() first.")
        
        abs_x = self.window_bounds['x'] + x
        abs_y = self.window_bounds['y'] + y
        return abs_x, abs_y
    
    def click(self, x: int, y: int, button: str = 'left', clicks: int = 1) -> None:
        self._ensure_focus()
        abs_x, abs_y = self._to_absolute_coords(x, y)
        pyautogui.click(abs_x, abs_y, button=button, clicks=clicks)
        
    def double_click(self, x: int, y: int) -> None:
        self.click(x, y, clicks=2)
        
    def right_click(self, x: int, y: int) -> None:
        self.click(x, y, button='right')
        
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, 
              duration: float = 0.5) -> None:
        self._ensure_focus()
        start_abs = self._to_absolute_coords(start_x, start_y)
        end_abs = self._to_absolute_coords(end_x, end_y)
        
        pyautogui.mouseDown(start_abs[0], start_abs[1], button='left')
        pyautogui.moveTo(end_abs[0], end_abs[1], duration=duration)
        pyautogui.mouseUp(button='left')
        
    def scroll(self, x: int, y: int, clicks: int = -3, smooth: bool = True) -> None:
        """
        Vertical scroll at the specified position.
        
        Args:
            x, y: Position to scroll at (relative to window)
            clicks: Number of scroll clicks (negative = down, positive = up)
            smooth: If True, use smooth scrolling with delays
        """
        self._ensure_focus()
        abs_x, abs_y = self._to_absolute_coords(x, y)
        
        # Move mouse to the scroll position
        pyautogui.moveTo(abs_x, abs_y)
        
        if smooth:
            # Use scroll with small increments to simulate smooth scrolling
            increment = 1 if clicks > 0 else -1
            for _ in range(abs(clicks)):
                pyautogui.scroll(increment)
                time.sleep(0.02)  # Smaller delay for smoother motion
        else:
            # Direct scroll for faster operation
            pyautogui.scroll(clicks)
    
    def hscroll(self, x: int, y: int, clicks: int = -3, smooth: bool = True) -> None:
        """
        Horizontal scroll at the specified position.
        
        Args:
            x, y: Position to scroll at (relative to window)
            clicks: Number of scroll clicks (negative = right, positive = left)
            smooth: If True, use smooth scrolling with delays
        """
        self._ensure_focus()
        abs_x, abs_y = self._to_absolute_coords(x, y)
        
        # Move mouse to the scroll position
        pyautogui.moveTo(abs_x, abs_y)
        
        if smooth:
            # Use scroll with small increments to simulate smooth scrolling
            increment = 1 if clicks > 0 else -1
            for _ in range(abs(clicks)):
                pyautogui.hscroll(increment)
                time.sleep(0.02)  # Smaller delay for smoother motion
        else:
            # Direct scroll for faster operation
            pyautogui.hscroll(clicks)
    
    def two_finger_scroll(self, x: int, y: int, distance: int = 100, 
                         direction: str = 'up', duration: float = 0.3) -> None:
        """
        Simulate a two-finger scroll gesture using swipe.
        
        Args:
            x, y: Center position for the scroll
            distance: How far to scroll in pixels
            direction: 'up', 'down', 'left', or 'right'
            duration: How long the scroll gesture takes
        """
        if direction == 'up':
            self.swipe(x, y, x, y - distance, duration)
        elif direction == 'down':
            self.swipe(x, y, x, y + distance, duration)
        elif direction == 'left':
            self.swipe(x, y, x - distance, y, duration)
        elif direction == 'right':
            self.swipe(x, y, x + distance, y, duration)
    
    def native_scroll(self, x: int, y: int, delta_x: int = 0, delta_y: int = -5, 
                     repeat: int = 1) -> None:
        """
        Perform native macOS scroll using CGEvent.
        
        Args:
            x, y: Position to scroll at (relative to window)
            delta_x: Horizontal scroll amount (negative = right, positive = left)
            delta_y: Vertical scroll amount (negative = down, positive = up)
            repeat: Number of times to repeat the scroll event
        """
        self._ensure_focus()
        abs_x, abs_y = self._to_absolute_coords(x, y)
        
        # Move mouse to position
        pyautogui.moveTo(abs_x, abs_y)
        
        # Repeat scroll events for more noticeable effect
        for _ in range(repeat):
            # Create and post scroll event
            # Note: For continuous scrolling, we need to use pixel delta (1) not line delta (0)
            event = CGEventCreateScrollWheelEvent(None, 1, 2, delta_y, delta_x)
            CGEventPost(kCGHIDEventTap, event)
            if repeat > 1:
                time.sleep(0.05)  # Small delay between repeated events
    
    def continuous_scroll(self, x: int, y: int, direction: str = 'down', 
                         duration: float = 1.0, speed: int = 5) -> None:
        """
        Perform continuous scrolling for a duration.
        
        Args:
            x, y: Position to scroll at
            direction: 'up', 'down', 'left', or 'right'
            duration: How long to scroll
            speed: Scroll speed (1-10)
        """
        self._ensure_focus()
        abs_x, abs_y = self._to_absolute_coords(x, y)
        pyautogui.moveTo(abs_x, abs_y)
        
        # Set scroll deltas based on direction with enhanced horizontal values
        delta_x, delta_y = 0, 0
        if direction == 'down':
            delta_y = -speed
        elif direction == 'up':
            delta_y = speed
        elif direction == 'right':
            delta_x = -speed * 2  # Enhanced horizontal scrolling
        elif direction == 'left':
            delta_x = speed * 2   # Enhanced horizontal scrolling
        
        # Perform continuous scrolling with variable delay for horizontal
        start_time = time.time()
        delay = 0.005 if direction in ['left', 'right'] else 0.01
        
        while time.time() - start_time < duration:
            event = CGEventCreateScrollWheelEvent(None, 1, 2, delta_y, delta_x)
            CGEventPost(kCGHIDEventTap, event)
            time.sleep(delay)  # Faster events for horizontal scrolling
    
    def enhanced_horizontal_scroll(self, x: int, y: int, direction: str = 'left', 
                                  distance: int = 20, smoothness: int = 10) -> None:
        """
        Enhanced horizontal scrolling with better control.
        
        Args:
            x, y: Position to scroll at
            direction: 'left' or 'right'
            distance: Total scroll distance
            smoothness: Number of scroll events to break the distance into
        """
        self._ensure_focus()
        abs_x, abs_y = self._to_absolute_coords(x, y)
        pyautogui.moveTo(abs_x, abs_y)
        
        # Calculate delta per event
        delta_per_event = distance // smoothness
        delta_x = delta_per_event if direction == 'left' else -delta_per_event
        
        # Perform smooth horizontal scrolling
        for _ in range(smoothness):
            event = CGEventCreateScrollWheelEvent(None, 1, 2, 0, delta_x)
            CGEventPost(kCGHIDEventTap, event)
            time.sleep(0.02)  # Small delay for smoothness
    
    def keyboard_scroll(self, direction: str = 'down', method: str = 'arrow') -> None:
        """
        Scroll using keyboard shortcuts.
        
        Args:
            direction: 'up' or 'down'
            method: 'arrow', 'page', or 'space'
        """
        self._ensure_focus()
        
        if method == 'arrow':
            key = 'down' if direction == 'down' else 'up'
            pyautogui.press(key)
        elif method == 'page':
            if direction == 'down':
                pyautogui.hotkey('fn', 'down')  # Page Down
            else:
                pyautogui.hotkey('fn', 'up')    # Page Up
        elif method == 'space':
            if direction == 'down':
                pyautogui.press('space')
            else:
                pyautogui.hotkey('shift', 'space')
    
    # Recording and Playback Methods
    def start_recording(self) -> None:
        """Start recording manual interactions."""
        if self.recording:
            print("Already recording!")
            return
        
        if not self.window_bounds:
            print("Window not focused. Call focus_window() first.")
            return
            
        self.recording = True
        self.recorded_actions = []
        self.start_time = time.time()
        
        print(f"🔴 Recording started at {datetime.now().strftime('%H:%M:%S')}")
        print("Perform your manual interactions in the iPhone Mirroring window...")
        print("Press Ctrl+C to stop recording")
        
        # Start listening for mouse events
        self.mouse_listener = mouse.Listener(
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        self.mouse_listener.start()
        
        # Start listening for keyboard events
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press
        )
        self.keyboard_listener.start()
    
    def stop_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return the recorded actions."""
        if not self.recording:
            print("Not currently recording!")
            return []
        
        # Finalize any pending scroll actions
        self._finalize_continuous_scroll()
        
        self.recording = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        print(f"🛑 Recording stopped. Captured {len(self.recorded_actions)} actions")
        return self.recorded_actions
    
    def _is_within_window(self, x: int, y: int) -> bool:
        """Check if coordinates are within the iPhone Mirroring window."""
        if not self.window_bounds:
            return False
        return (self.window_bounds['x'] <= x <= self.window_bounds['x'] + self.window_bounds['width'] and
                self.window_bounds['y'] <= y <= self.window_bounds['y'] + self.window_bounds['height'])
    
    def _to_relative_coords(self, x: int, y: int) -> Tuple[int, int]:
        """Convert absolute coordinates to window-relative coordinates."""
        if not self.window_bounds:
            return x, y
        return x - self.window_bounds['x'], y - self.window_bounds['y']
    
    def _on_click(self, x: int, y: int, button, pressed: bool) -> None:
        """Handle mouse click events during recording."""
        if not self.recording or not self._is_within_window(x, y):
            return
        
        rel_x, rel_y = self._to_relative_coords(x, y)
        
        if pressed:  # Only record mouse down events
            action = {
                'type': 'click',
                'x': rel_x,
                'y': rel_y,
                'button': button.name,
                'timestamp': time.time() - self.start_time
            }
            self.recorded_actions.append(action)
            print(f"📍 Click recorded at ({rel_x}, {rel_y}) with {button.name} button")
    
    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """Handle scroll events during recording - aggregates into continuous scrolls."""
        if not self.recording or not self._is_within_window(x, y):
            return
        
        rel_x, rel_y = self._to_relative_coords(x, y)
        current_time = time.time()
        
        # Check if this is part of a continuous scroll sequence
        if (current_time - self.last_scroll_time) > self.scroll_timeout:
            # New scroll sequence - finalize any previous scroll
            self._finalize_continuous_scroll()
            # Start new scroll buffer
            self.scroll_buffer = []
        
        # Add scroll event to buffer
        scroll_event = {
            'x': rel_x,
            'y': rel_y,
            'dx': dx,
            'dy': dy,
            'timestamp': current_time - self.start_time
        }
        self.scroll_buffer.append(scroll_event)
        self.last_scroll_time = current_time
        
        direction = "horizontal" if abs(dx) > abs(dy) else "vertical"
        print(f"🖱️ {direction.capitalize()} scroll detected at ({rel_x}, {rel_y})")
    
    def _finalize_continuous_scroll(self) -> None:
        """Convert buffered scroll events into a continuous scroll action."""
        if not self.scroll_buffer:
            return
        
        # Calculate total scroll distance and direction
        total_dx = sum(event['dx'] for event in self.scroll_buffer)
        total_dy = sum(event['dy'] for event in self.scroll_buffer)
        
        # Use the position from the first scroll event
        first_event = self.scroll_buffer[0]
        last_event = self.scroll_buffer[-1]
        
        # Calculate duration of the scroll sequence - cap it for gentler scrolling
        duration = last_event['timestamp'] - first_event['timestamp']
        if duration < 0.1:  # Minimum duration
            duration = 0.2
        elif duration > 1.0:  # Maximum duration to prevent overly long scrolls
            duration = 1.0
        
        # Determine primary direction and create continuous scroll action
        if abs(total_dx) > abs(total_dy):
            # Horizontal scroll
            direction = 'left' if total_dx > 0 else 'right'
            speed = min(3, max(1, int(abs(total_dx) / 5)))  # Reduced speed calculation
        else:
            # Vertical scroll
            direction = 'up' if total_dy > 0 else 'down'
            speed = min(3, max(1, int(abs(total_dy) / 5)))  # Reduced speed calculation
        
        action = {
            'type': 'continuous_scroll',
            'x': first_event['x'],
            'y': first_event['y'],
            'direction': direction,
            'duration': round(duration, 2),
            'speed': speed,
            'timestamp': first_event['timestamp']
        }
        
        self.recorded_actions.append(action)
        print(f"📜 Continuous {direction} scroll recorded: {duration:.2f}s at speed {speed}")
        
        # Clear the buffer
        self.scroll_buffer = []
    
    def _on_key_press(self, key) -> None:
        """Handle keyboard events during recording."""
        if not self.recording:
            return
        
        # Stop recording on Ctrl+C
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            return
        
        try:
            key_name = key.char if hasattr(key, 'char') and key.char else key.name
        except AttributeError:
            key_name = str(key)
        
        if key_name and key_name not in ['ctrl_l', 'ctrl_r']:
            action = {
                'type': 'key',
                'key': key_name,
                'timestamp': time.time() - self.start_time
            }
            self.recorded_actions.append(action)
            print(f"⌨️ Key press recorded: {key_name}")
    
    def save_recording(self, filename: str, actions: List[Dict[str, Any]] = None) -> None:
        """Save recorded actions to a JSON file."""
        if actions is None:
            actions = self.recorded_actions
        
        recording_data = {
            'timestamp': datetime.now().isoformat(),
            'window_bounds': self.window_bounds,
            'total_actions': len(actions),
            'actions': actions
        }
        
        with open(filename, 'w') as f:
            json.dump(recording_data, f, indent=2)
        
        print(f"💾 Recording saved to {filename}")
    
    def load_recording(self, filename: str) -> List[Dict[str, Any]]:
        """Load recorded actions from a JSON file."""
        try:
            with open(filename, 'r') as f:
                recording_data = json.load(f)
            
            actions = recording_data.get('actions', [])
            print(f"📁 Loaded {len(actions)} actions from {filename}")
            return actions
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
            return []
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {filename}")
            return []
    
    def replay_recording(self, actions: List[Dict[str, Any]] = None, 
                        speed_multiplier: float = 1.0) -> None:
        """Replay recorded actions."""
        if actions is None:
            actions = self.recorded_actions
        
        if not actions:
            print("❌ No actions to replay!")
            return
        
        if not self.window_bounds:
            print("❌ Window not focused. Call focus_window() first.")
            return
        
        self._ensure_focus()
        print(f"▶️ Starting playback of {len(actions)} actions...")
        
        last_timestamp = 0
        for i, action in enumerate(actions):
            # Wait for the appropriate time delay
            delay = (action['timestamp'] - last_timestamp) / speed_multiplier
            if delay > 0:
                time.sleep(delay)
            
            # Execute the action
            try:
                if action['type'] == 'click':
                    self.click(action['x'], action['y'], button=action.get('button', 'left'))
                    print(f"  {i+1}/{len(actions)}: Click at ({action['x']}, {action['y']})")
                
                elif action['type'] == 'scroll':
                    self.native_scroll(action['x'], action['y'], 
                                     delta_x=action['dx'], delta_y=action['dy'])
                    print(f"  {i+1}/{len(actions)}: Scroll at ({action['x']}, {action['y']})")
                
                elif action['type'] == 'continuous_scroll':
                    self.continuous_scroll(action['x'], action['y'], 
                                         direction=action['direction'],
                                         duration=action['duration'],
                                         speed=action['speed'])
                    print(f"  {i+1}/{len(actions)}: Continuous {action['direction']} scroll "
                          f"for {action['duration']}s at speed {action['speed']}")
                
                elif action['type'] == 'key':
                    pyautogui.press(action['key'])
                    print(f"  {i+1}/{len(actions)}: Key press: {action['key']}")
                
            except Exception as e:
                print(f"❌ Error executing action {i+1}: {e}")
            
            last_timestamp = action['timestamp']
        
        print("✅ Playback completed!")
    
    def generate_script(self, actions: List[Dict[str, Any]] = None, 
                       script_name: str = "generated_automation") -> str:
        """Generate a Python script from recorded actions."""
        if actions is None:
            actions = self.recorded_actions
        
        if not actions:
            return "# No actions recorded"
        
        script_lines = [
            "#!/usr/bin/env python3",
            "",
            "import sys",
            "import os",
            "import time",
            "sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))",
            "",
            "from iphone_automation import iPhoneAutomation",
            "",
            f"def {script_name}():",
            '    """Generated automation script"""',
            "    automation = iPhoneAutomation()",
            "    ",
            "    if not automation.focus_window():",
            '        print("Error: Could not find iPhone Mirroring window")',
            "        return False",
            "    ",
            '    print("Starting automated sequence...")',
            "    "
        ]
        
        last_timestamp = 0
        for i, action in enumerate(actions):
            # Add delay if needed
            delay = action['timestamp'] - last_timestamp
            if delay > 0.1:  # Only add delays longer than 100ms
                script_lines.append(f"    time.sleep({delay:.2f})")
            
            # Add the action
            if action['type'] == 'click':
                button = action.get('button', 'left')
                script_lines.append(f"    automation.click({action['x']}, {action['y']}, button='{button}')")
            
            elif action['type'] == 'scroll':
                script_lines.append(f"    automation.native_scroll({action['x']}, {action['y']}, "
                                  f"delta_x={action['dx']}, delta_y={action['dy']})")
            
            elif action['type'] == 'continuous_scroll':
                script_lines.append(f"    automation.continuous_scroll({action['x']}, {action['y']}, "
                                  f"direction='{action['direction']}', duration={action['duration']}, "
                                  f"speed={action['speed']})")
            
            elif action['type'] == 'key':
                script_lines.append(f"    automation.press_key('{action['key']}')")
            
            last_timestamp = action['timestamp']
        
        script_lines.extend([
            "    ",
            '    print("Automation completed!")',
            "    return True",
            "",
            'if __name__ == "__main__":',
            f"    {script_name}()"
        ])
        
        return "\n".join(script_lines)
        
    def type_text(self, text: str, interval: float = 0.05) -> None:
        pyautogui.typewrite(text, interval=interval)
        
    def press_key(self, key: str) -> None:
        pyautogui.press(key)
        
    def hotkey(self, *keys) -> None:
        pyautogui.hotkey(*keys)
        
    def screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        if region is None and self.window_bounds:
            region = (
                self.window_bounds['x'],
                self.window_bounds['y'],
                self.window_bounds['width'],
                self.window_bounds['height']
            )
        
        screenshot = pyautogui.screenshot(region=region)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def find_element(self, template_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        screenshot = self.screenshot()
        template = cv2.imread(template_path)
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            center_x = max_loc[0] + template.shape[1] // 2
            center_y = max_loc[1] + template.shape[0] // 2
            return center_x, center_y
        
        return None
    
    def click_element(self, template_path: str, confidence: float = 0.8, 
                     timeout: float = 10.0) -> bool:
        element = wait_for_element(self, template_path, confidence, timeout)
        if element:
            self.click(element[0], element[1])
            return True
        return False
    
    def wait(self, seconds: float) -> None:
        time.sleep(seconds)