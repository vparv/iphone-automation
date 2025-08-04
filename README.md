# iPhone Mirroring Automation

A Python-based automation tool for interacting with the iPhone Mirroring app on macOS.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Grant accessibility permissions:
   - Go to System Settings > Privacy & Security > Accessibility
   - Add Terminal (or your IDE) to the allowed apps

## Usage

```python
from iphone_automation import iPhoneAutomation

# Initialize automation
automation = iPhoneAutomation()

# Find and focus iPhone Mirroring window
automation.focus_window()

# Perform actions
automation.click(x=100, y=200)
automation.swipe(start_x=200, start_y=300, end_x=200, end_y=100)
automation.type_text("Hello from automation!")
```

## Examples

See the `examples/` directory for sample scripts.