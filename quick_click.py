#!/usr/bin/env python3
import sys
sys.path.append('.')
from iphone_automation import iPhoneAutomation

automation = iPhoneAutomation()
automation.window_title = 'Liene Photo HD'
automation.focus_window()
automation.click(634, 829)  # Use it button
print('Clicked Use it button')
