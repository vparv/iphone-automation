#!/usr/bin/env python3

import subprocess
import sys
import time
import re
import json
import os
from typing import Optional, Tuple, List, Dict, Any


def run(cmd: list[str]) -> str:
    out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
    return out.stdout


def adb(*args: str) -> str:
    return run(["adb", *args])


def ensure_device() -> None:
    out = adb("devices").strip().splitlines()
    lines = [ln for ln in out if "\t" in ln]
    if not lines:
        print("No devices attached. Connect your Android and run again.")
        sys.exit(1)
    status = lines[0].split("\t", 1)[1]
    if status != "device":
        print(f"Device status is '{status}'. Authorize device and retry.")
        sys.exit(1)


def get_screen_size() -> Tuple[int, int]:
    out = adb("shell", "wm", "size")
    # e.g., Physical size: 1080x2400
    m = re.search(r"Physical size:\s*(\d+)x(\d+)", out)
    if not m:
        # Fallback
        m = re.search(r"(\d+)x(\d+)", out)
    if not m:
        raise RuntimeError("Unable to determine screen size")
    return int(m.group(1)), int(m.group(2))


def find_touch_device() -> Tuple[Optional[str], int, int]:
    """Return (device_path, max_x, max_y) for touchscreen input device.
    If not found, returns (None, 0, 0) to allow fallback parsing across all devices.
    """
    out = adb("shell", "getevent", "-pl")
    blocks = out.split("add device")
    chosen = None
    max_x = max_y = None
    for b in blocks:
        if "/dev/input/event" not in b:
            continue
        devm = re.search(r"(/dev/input/event\d+)", b)
        if not devm:
            continue
        dev = devm.group(1)
        # Heuristic: must expose ABS_MT_POSITION_X and ABS_MT_POSITION_Y
        has_x = re.search(r"0035\s+VALUE\s+0,\s*min\s*\d+,\s*max\s*(\d+)", b)
        has_y = re.search(r"0036\s+VALUE\s+0,\s*min\s*\d+,\s*max\s*(\d+)", b)
        if has_x and has_y:
            mx = int(has_x.group(1))
            my = int(has_y.group(1))
            chosen = dev
            max_x, max_y = mx, my
            # Prefer the first matching touchscreen
            break
    if not chosen or max_x is None or max_y is None:
        # Fallback: let recorder parse all devices and assume raw ~ screen px
        return None, 0, 0
    return chosen, max_x, max_y


def scale(raw_x: int, raw_y: int, max_x: int, max_y: int, w: int, h: int) -> Tuple[int, int]:
    # Some devices report max exactly equal to width/height; otherwise scale
    sx = w / max_x if max_x else 1.0
    sy = h / max_y if max_y else 1.0
    x = max(0, min(w - 1, int(raw_x * sx)))
    y = max(0, min(h - 1, int(raw_y * sy)))
    return x, y


def record_events(dev: Optional[str], max_x: int, max_y: int, w: int, h: int) -> Dict[str, Any]:
    print("\n🔴 Recording started on Android. Perform your workflow on the device.")
    print("   Press Ctrl+C here to stop.")
    start = time.time()
    last_action_time = start
    actions: List[Dict[str, Any]] = []

    # Touch state
    current_x = current_y = None
    start_x = start_y = None
    touching = False
    down_time = None
    moved_distance2 = 0
    last_xy = None

    # Start getevent reader
    cmd = ["adb", "shell", "getevent", "-lt"]
    if dev:
        cmd.append(dev)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    try:
        for line in proc.stdout:
            # Example: [  3532.123456] /dev/input/event2: 0003 0035 00000567
            m = re.search(r"\[\s*(\d+\.\d+)\]\s+([^:]+):\s+([0-9a-f]{4})\s+([0-9a-f]{4})\s+([0-9a-f]{8})", line, re.IGNORECASE)
            if not m:
                continue
            t_s = float(m.group(1))
            etype = int(m.group(3), 16)
            code = int(m.group(4), 16)
            value_hex = m.group(5).lower()
            value = int(value_hex, 16)

            if etype == 0x0003:  # EV_ABS
                if code == 0x0035:  # ABS_MT_POSITION_X
                    current_x = value
                elif code == 0x0036:  # ABS_MT_POSITION_Y
                    current_y = value
                elif code == 0x0039:  # ABS_MT_TRACKING_ID (start/end of contact)
                    if value_hex != "ffffffff" and not touching:
                        touching = True
                        down_time = t_s
                        moved_distance2 = 0
                        last_xy = None
                        start_x = current_x
                        start_y = current_y
                    elif value_hex == "ffffffff" and touching:
                        touching = False
                        up_time = t_s
                        if start_x is not None and start_y is not None and current_x is not None and current_y is not None:
                            sx, sy = scale(start_x, start_y, max_x, max_y, w, h)
                            ex, ey = scale(current_x, current_y, max_x, max_y, w, h)
                            duration_ms = int(max(1, (up_time - (down_time or up_time)) * 1000))
                            if (sx - ex) ** 2 + (sy - ey) ** 2 < 20 * 20:
                                actions.append({
                                    "type": "tap",
                                    "x": ex,
                                    "y": ey,
                                    "delay": round((t_s - last_action_time), 3)
                                })
                            else:
                                actions.append({
                                    "type": "swipe",
                                    "x1": sx,
                                    "y1": sy,
                                    "x2": ex,
                                    "y2": ey,
                                    "duration_ms": duration_ms,
                                    "delay": round((t_s - last_action_time), 3)
                                })
                            last_action_time = t_s
                            start_x = start_y = None
            elif etype == 0x0001 and code == 0x014a:  # EV_KEY BTN_TOUCH
                if value == 1 and not touching:
                    touching = True
                    down_time = t_s
                    # Reset motion metrics
                    moved_distance2 = 0
                    last_xy = None
                    start_x = current_x
                    start_y = current_y
                elif value == 0 and touching:
                    touching = False
                    up_time = t_s
                    if start_x is not None and start_y is not None and current_x is not None and current_y is not None:
                        sx, sy = scale(start_x, start_y, max_x, max_y, w, h)
                        ex, ey = scale(current_x, current_y, max_x, max_y, w, h)
                        duration_ms = int(max(1, (up_time - (down_time or up_time)) * 1000))
                        # Decide tap vs swipe by movement threshold
                        if (sx - ex) ** 2 + (sy - ey) ** 2 < 20 * 20:
                            # tap
                            actions.append({
                                "type": "tap",
                                "x": ex,
                                "y": ey,
                                "delay": round((t_s - last_action_time), 3)
                            })
                        else:
                            actions.append({
                                "type": "swipe",
                                "x1": sx,
                                "y1": sy,
                                "x2": ex,
                                "y2": ey,
                                "duration_ms": duration_ms,
                                "delay": round((t_s - last_action_time), 3)
                            })
                        last_action_time = t_s
                        start_x = start_y = None
            elif etype == 0x0000 and code == 0:  # EV_SYN SYN_REPORT
                # Track movement between SYN frames to estimate swipe motion
                if touching and current_x is not None and current_y is not None:
                    cx, cy = current_x, current_y
                    if last_xy is not None:
                        dx = cx - last_xy[0]
                        dy = cy - last_xy[1]
                        moved_distance2 += dx * dx + dy * dy
                    last_xy = (cx, cy)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            proc.terminate()
        except Exception:
            pass

    return {
        "started_at": start,
        "actions": actions,
        "screen": {"width": w, "height": h},
    }


def save_recording(data: Dict[str, Any]) -> str:
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(os.path.dirname(__file__), "recordings")
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"android_session_{ts}.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n💾 Saved recording to {json_path}")
    # Also generate a simple playback script
    py_path = os.path.join(out_dir, f"android_session_{ts}.py")
    generate_playback(py_path, data)
    print(f"🐍 Playback script: {py_path}")
    return json_path


def generate_playback(path: str, data: Dict[str, Any]) -> None:
    lines = [
        "#!/usr/bin/env python3",
        "import subprocess, time, sys",
        "def adb(*args): subprocess.run(['adb', *args], check=True)",
        "def tap(x,y): adb('shell','input','tap',str(x),str(y))",
        "def swipe(x1,y1,x2,y2,ms): adb('shell','input','swipe',str(x1),str(y1),str(x2),str(y2),str(ms))",
        "def main():",
    ]
    added = False
    for a in data.get("actions", []):
        d = a.get("delay", 0)
        if d and d > 0:
            lines.append(f"    time.sleep({d})")
            added = True
        if a["type"] == "tap":
            lines.append(f"    tap({a['x']}, {a['y']})")
            added = True
        elif a["type"] == "swipe":
            lines.append(f"    swipe({a['x1']}, {a['y1']}, {a['x2']}, {a['y2']}, {a['duration_ms']})")
            added = True
    if not added:
        lines.append("    pass")
    lines += [
        "if __name__ == '__main__':",
        "    main()",
    ]
    with open(path, "w") as f:
        f.write("\n".join(lines))


def main():
    ensure_device()
    w, h = get_screen_size()
    dev, max_x, max_y = find_touch_device()
    print(f"Using touch device: {dev} (maxX={max_x}, maxY={max_y}), screen={w}x{h}")
    rec = record_events(dev, max_x, max_y, w, h)
    save_recording(rec)


if __name__ == "__main__":
    main()


