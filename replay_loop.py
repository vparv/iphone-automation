#!/usr/bin/env python3

import sys
import os
import time
import argparse

# Ensure we can import iphone_automation from project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from iphone_automation import iPhoneAutomation


def expand_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def replay_in_loop(recording_path: str, loops: int = 100, delay_seconds: float = 1.0) -> bool:
    automation = iPhoneAutomation()

    if not automation.focus_window():
        print("Error: Could not find iPhone Mirroring window")
        print("Make sure iPhone Mirroring is running and visible")
        return False

    actions = automation.load_recording(recording_path)
    if not actions:
        print("No actions loaded; aborting.")
        return False

    print(f"Starting optimized looped playback: {loops} loops, {delay_seconds:.2f}s pause between runs")
    print(f"Loaded {len(actions)} actions per loop")

    # Execute loops with minimal overhead
    for loop_num in range(loops):
        if loop_num % 10 == 0:  # Progress update every 10 loops
            print(f"Loop {loop_num + 1}/{loops}")

        # Execute all actions in sequence without replay_recording overhead
        last_timestamp = 0
        for action in actions:
            # Wait for the appropriate time delay (preserve original timing)
            delay = action['timestamp'] - last_timestamp
            if delay > 0:
                time.sleep(delay)
            
            # Execute the action directly
            try:
                if action['type'] == 'click':
                    automation.click(action['x'], action['y'], button=action.get('button', 'left'))
                
                elif action['type'] == 'scroll':
                    automation.native_scroll(action['x'], action['y'], 
                                           delta_x=action['dx'], delta_y=action['dy'])
                
                elif action['type'] == 'continuous_scroll':
                    automation.continuous_scroll(action['x'], action['y'], 
                                               direction=action['direction'],
                                               duration=action['duration'],
                                               speed=action['speed'])
                
                elif action['type'] == 'key':
                    automation.press_key(action['key'])
                
            except Exception as e:
                print(f"Error in loop {loop_num + 1}, action: {e}")
            
            last_timestamp = action['timestamp']

        # Pause between loops (except after the last one)
        if loop_num < loops - 1:
            time.sleep(delay_seconds)

    print(f"\nAll {loops} loops completed!")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay a recording JSON in a loop")
    parser.add_argument("--file", "-f", required=True, help="Path to recording JSON file")
    parser.add_argument("--loops", "-n", type=int, default=100, help="Number of loops to run")
    parser.add_argument("--delay", "-d", type=float, default=1.0, help="Delay in seconds between loops")

    args = parser.parse_args()
    recording_path = expand_path(args.file)

    if not os.path.isfile(recording_path):
        print(f"Error: Recording file not found: {recording_path}")
        sys.exit(1)

    success = replay_in_loop(recording_path, loops=args.loops, delay_seconds=args.delay)
    sys.exit(0 if success else 2)


if __name__ == "__main__":
    main()


