import time
import subprocess
import json
from typing import Optional, Dict, Tuple, Any
import Quartz
import pyautogui

def find_iphone_window(title: str = "iPhone Mirroring") -> Optional[Any]:
    try:
        script = f'''
        tell application "System Events"
            set windowList to {{}}
            repeat with proc in application processes
                try
                    repeat with win in windows of proc
                        if name of win contains "{title}" then
                            return {{name of proc, name of win, position of win, size of win}}
                        end if
                    end repeat
                end try
            end repeat
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            return parse_applescript_result(result.stdout.strip())
        
    except Exception as e:
        print(f"Error finding window: {e}")
    
    return None

def parse_applescript_result(result: str) -> Dict[str, Any]:
    parts = result.split(', ')
    if len(parts) >= 6:
        return {
            'app': parts[0],
            'title': parts[1],
            'x': int(parts[2]),
            'y': int(parts[3]),
            'width': int(parts[4]),
            'height': int(parts[5])
        }
    return None

def get_window_bounds(window_info: Dict[str, Any]) -> Dict[str, int]:
    return {
        'x': window_info['x'],
        'y': window_info['y'],
        'width': window_info['width'],
        'height': window_info['height']
    }

def activate_window(app_name: str) -> None:
    script = f'''
    tell application "{app_name}"
        activate
    end tell
    '''
    subprocess.run(['osascript', '-e', script])
    time.sleep(0.5)

def wait_for_element(automation_obj, template_path: str, 
                    confidence: float = 0.8, timeout: float = 10.0) -> Optional[Tuple[int, int]]:
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        element = automation_obj.find_element(template_path, confidence)
        if element:
            return element
        time.sleep(0.5)
    
    return None

def safe_click(x: int, y: int, delay: float = 0.1) -> None:
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(x, y, duration=0.2)
    time.sleep(delay)
    pyautogui.click()
    pyautogui.moveTo(current_x, current_y, duration=0.1)

def load_config(config_path: str = "config/default.json") -> Dict[str, Any]:
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_default_config()

def get_default_config() -> Dict[str, Any]:
    return {
        "window_title": "iPhone Mirroring",
        "default_delay": 0.1,
        "swipe_duration": 0.5,
        "screenshot_confidence": 0.8,
        "element_timeout": 10.0,
        "failsafe": True
    }

def save_config(config: Dict[str, Any], config_path: str = "config/default.json") -> None:
    import os
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def get_screen_size() -> Tuple[int, int]:
    return pyautogui.size()

def is_retina_display() -> bool:
    main_display = Quartz.CGMainDisplayID()
    return Quartz.CGDisplayScreenSize(main_display).width < 400

def adjust_for_retina(x: int, y: int) -> Tuple[int, int]:
    if is_retina_display():
        return x * 2, y * 2
    return x, y