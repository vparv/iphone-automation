# iPhone/Mobile Automation Scripts

A comprehensive automation toolkit for macOS, iOS, and Android platforms targeting photo processing workflows.

## 🍎 macOS - Liene Photo HD

### Core Scripts

#### 1. Automated Loop Script (with Sessions)
**File:** `recordings/liene_session_20250808_205800_loop20.py`
- **Purpose:** Automated photo processing with 28 loops (configurable)
- **Features:** Variable gallery positions, timing optimizations, size input (166)
- **Usage:**
```bash
# Default 28 loops
python3 recordings/liene_session_20250808_205800_loop20.py

# Custom loop count
python3 recordings/liene_session_20250808_205800_loop20.py 32
```

#### 2. Record New Automation
**For IOS:** `examples/record_automation.py`
**For MacOS Liene**: python3 record_liene_workflow.py
- **Purpose:** Record manual interactions for automation replay
- **Features:** Interactive recording, auto-save, immediate replay option
- **Usage:**
```bash
python3 examples/record_automation.py
# Choose option 1: Record new session
# Perform actions in Liene Photo HD
# Press Ctrl+C to stop recording
```

### Requirements
- macOS with iPhone Mirroring or Liene Photo HD app
- Python 3.7+
- Dependencies: `pip install -r requirements.txt`

---

## 📱 iOS - iPhone Mirroring

### Core Script

#### Optimized Loop Replay
**File:** `replay_loop.py`
- **Purpose:** Replay recorded sessions in tight loops with minimal overhead
- **Features:** 100 loops (configurable), 1-second pauses, progress tracking
- **Target Recording:** `recordings/session_20250812_211057.json`

**Recording Details:**
- **Actions per loop:** 4 (3 clicks + 1 key press)
- **Duration:** ~4.37 seconds per loop
- **Total time for 100 loops:** ~9 minutes

**Usage:**
```bash
# Run 100 loops with 1s pause
python3 replay_loop.py -f recordings/session_20250812_211057.json -n 100 -d 1

# Custom configuration
python3 replay_loop.py --file path/to/recording.json --loops 50 --delay 0.5
```

**Actions in Loop:**
1. Click (195, 315) - Start action
2. Click (109, 938) - +2.49s
3. Click (313, 590) - +1.38s  
4. Key press 'c' - +0.5s

### Requirements
- macOS with iPhone Mirroring app active
- Target iPhone app running and visible
- Python 3.7+ with automation dependencies

---

## 🤖 Android - Enhanced Gallery Automation

### Core Script

#### Gallery Loop (Most Enhanced)
**File:** `android/gallery_loop.py`
- **Purpose:** Advanced Android automation with gallery navigation and drag operations
- **Features:** 
  - 20 predefined gallery positions (4×5 grid)
  - Retry logic for reliable taps
  - Drag sequences with motion events
  - Optional post-drag workflow
  - Configurable start index and loop count

**Key Features:**
- **Grid Positions:** 4 columns × 5 rows = 20 positions
- **Retry Taps:** Handles stale UI overlays with offset attempts
- **Drag Operations:** Precision motion events with timing control
- **Flexible Execution:** Start from any position, run partial sets

**Usage:**
```bash
# Run all 20 positions
python3 android/gallery_loop.py

# Start from position 5
python3 android/gallery_loop.py 5

# Run only position 10 (start=10, count=1)
python3 android/gallery_loop.py 10 1
```

**Workflow Steps:**
1. **Navigation:** Tap app entry points
2. **Gallery Selection:** Smart retry on calculated grid positions
3. **Processing:** Fixed workflow taps with optimized timing
4. **Drag Operations:** Dual drag sequence with motion events
5. **Cleanup:** Optional post-processing and loop reset

**Grid Coordinates:**
- **X positions:** [170, 400, 630, 940]
- **Y positions:** [360, 620, 880, 1140, 1400]
- **Total positions:** 20 (automatically calculated)

### Alternative Android Scripts

#### Simple Sequence
**File:** `android/sequence_01.py`
- **Purpose:** Basic 5-step automation with drag operations
- **Usage:** `python3 android/sequence_01.py [pause_seconds]`

#### Touch Recording
**File:** `android/record_touch.py`
- **Purpose:** Record and replay touch sequences
- **Features:** Real-time recording, JSON export, Python script generation

### Requirements
- Android device with USB debugging enabled
- ADB installed and device authorized
- Target app installed and accessible
- Python 3.7+

```bash
# Verify ADB connection
adb devices

# Should show: device_id    device
```

---

## ⚡ Quick Commands (Copy & Paste)

### macOS - Liene Photo HD
```bash
# START LIENE HD RECORDING (creates new automation)
python3 /Users/alandweck/Eng/iphone-automation/examples/record_automation.py

# Run the main loop script (28 loops default)
python3 /Users/alandweck/Eng/iphone-automation/recordings/liene_session_20250808_205800_loop20.py

# Run with custom loop count (e.g., 50 loops)
python3 /Users/alandweck/Eng/iphone-automation/recordings/liene_session_20250808_205800_loop20.py 50

# RECORD LIENE WORKFLOW (specific to Liene app)
python3 /Users/alandweck/Eng/iphone-automation/record_liene_workflow.py
```

### iOS - iPhone Mirroring  
```bash
# START IPHONE RECORDING (creates new recording)
python3 /Users/alandweck/Eng/iphone-automation/examples/record_automation.py

# Run 100 loops with 1s pause (optimized, ~9 minutes total)
python3 /Users/alandweck/Eng/iphone-automation/replay_loop.py -f /Users/alandweck/Eng/iphone-automation/recordings/session_20250812_211057.json -n 100 -d 1

# Run 50 loops with 0.5s pause
python3 /Users/alandweck/Eng/iphone-automation/replay_loop.py -f /Users/alandweck/Eng/iphone-automation/recordings/session_20250812_211057.json -n 50 -d 0.5
```

### Android - Enhanced Gallery
```bash
# START ANDROID RECORDING (creates new touch recording)
python3 /Users/alandweck/Eng/iphone-automation/android/record_touch.py

# Run all 20 gallery positions (most enhanced script)
python3 /Users/alandweck/Eng/iphone-automation/android/gallery_loop.py

# Start from position 5, run all remaining
python3 /Users/alandweck/Eng/iphone-automation/android/gallery_loop.py 5

# Run only position 10 (start=10, count=1)
python3 /Users/alandweck/Eng/iphone-automation/android/gallery_loop.py 10 1

# Simple sequence (5 steps with drag)
python3 /Users/alandweck/Eng/iphone-automation/android/sequence_01.py
```

## 🚀 Quick Start Guide

### 1. macOS/iOS Setup
```bash
cd /Users/alandweck/Eng/iphone-automation
pip install -r requirements.txt

# For recording new automations
python3 examples/record_automation.py

# For running existing loops
python3 replay_loop.py -f recordings/session_20250812_211057.json -n 100 -d 1
```

### 2. Android Setup
```bash
# Enable USB debugging on Android device
# Connect device and authorize computer

cd /Users/alandweck/Eng/iphone-automation/android

# Verify connection
adb devices

# Run enhanced gallery automation
python3 gallery_loop.py
```

---

## 📁 Directory Structure

```
iphone-automation/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── replay_loop.py              # iOS optimized loop script
├── examples/
│   └── record_automation.py    # macOS recording tool
├── recordings/
│   ├── session_20250812_211057.json          # iOS target recording
│   └── liene_session_20250808_205800_loop20.py # macOS loop script
└── android/
    ├── gallery_loop.py         # Enhanced Android automation
    ├── sequence_01.py          # Simple Android sequence
    └── record_touch.py         # Android recording tool
```

---

## 🛠️ Troubleshooting

### macOS/iOS Issues
- **Window not found:** Ensure target app is open and visible
- **Actions fail:** Check window focus and app responsiveness
- **Recording issues:** Verify click coordinates are within app bounds

### Android Issues
- **Device not found:** Check `adb devices` and USB debugging
- **Tap accuracy:** Use `--pointer` flag to debug coordinate accuracy
- **App crashes:** Reduce automation speed with longer pauses

### Performance Tips
- **iOS:** Use `replay_loop.py` for minimal overhead looping
- **Android:** Use `gallery_loop.py` retry logic for reliability
- **macOS:** Record shorter sequences for faster playback

---

## 📝 Notes

- All scripts include configurable timing and loop counts
- Coordinate systems are platform-specific (check documentation)
- Recording tools generate both JSON data and Python scripts
- Enhanced scripts include error handling and retry logic
- Progress tracking available for long-running automations

For detailed usage of individual scripts, run them with `--help` or check inline documentation.