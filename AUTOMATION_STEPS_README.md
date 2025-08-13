# 🤖 Liene Photo HD Automation Steps

## Complete Step-by-Step Workflow with Coordinates

### Pre-Steps (Gallery Navigation)
- **Navigate to Gallery**: Canvas button (517, 130) → Upload button (32, 210)
- **Select Image**: Calculate position based on image number
  - Row = (image_number - 1) ÷ 4
  - Column = (image_number - 1) % 4
  - X = 426 + (column × 72)
  - Y = 179 + (row × 80)

---

## Main Workflow Steps

### Step 1: 🖱️ Click "Use It" Button
- **Coordinates**: (567, 648)
- **Purpose**: Start the image processing workflow
- **Wait Time**: 4.0 seconds
- **What happens**: Opens the AI processing dialog

### Step 2: 🖱️ Click "Next" in AI Background Removal Dialog
- **Coordinates**: (567, 702)
- **Purpose**: Proceed past the "AI remove bg" dialog
- **Wait Time**: 3.0 seconds
- **What happens**: Moves to size input screen

### Step 3: 🖱️ Click Size Input Field
- **Coordinates**: (1024, 443)
- **Purpose**: Focus on the size input field
- **Wait Time**: 2.0 seconds
- **What happens**: Selects the size input area

### Step 4: 🖱️ Click to Clear Existing Size Text
- **Coordinates**: (970, 440)
- **Purpose**: Clear existing text in size field
- **Wait Time**: 1.0 seconds
- **What happens**: Prepares field for new input

### Step 5: ⌨️ Delete Existing Text (First Backspace)
- **Action**: Press 'backspace' key
- **Purpose**: Remove existing characters
- **Wait Time**: 0.2 seconds

### Step 6: ⌨️ Delete Existing Text (Second Backspace)
- **Action**: Press 'backspace' key
- **Purpose**: Remove remaining characters
- **Wait Time**: 0.5 seconds

### Step 7: ⌨️ Type "1" (First Digit of 166)
- **Action**: Press '1' key
- **Purpose**: Start typing "166"
- **Wait Time**: 0.1 seconds

### Step 8: ⌨️ Type "6" (Second Digit of 166)
- **Action**: Press '6' key
- **Purpose**: Continue typing "166"
- **Wait Time**: 0.1 seconds

### Step 9: ⌨️ Type "6" (Third Digit of 166)
- **Action**: Press '6' key
- **Purpose**: Complete typing "166"
- **Wait Time**: 1.0 seconds

### Step 10: ⌨️ Tab to Next Input Field
- **Action**: Press 'tab' key
- **Purpose**: Move to next input field
- **Wait Time**: 0.5 seconds

### Step 11: 🖱️ Click Confirmation Button to Process Image
- **Coordinates**: (963, 559)
- **Purpose**: Confirm the size settings
- **Wait Time**: 3.0 seconds
- **What happens**: Process the image with new size

### Step 12: 🖱️ Click Back Navigation (First Click)
- **Coordinates**: (903, 129)
- **Purpose**: Start navigation back to main screen
- **Wait Time**: 1.0 seconds

### Step 13: 🖱️ Click Back Navigation (Return to Gallery)
- **Coordinates**: (1015, 113)
- **Purpose**: Return to gallery to begin next image
- **Wait Time**: 1.0 seconds

### Step 14: 🖱️ Click at Tracked Position
- **Coordinates**: (1014, 129)
- **Purpose**: Click at user-specified position
- **Wait Time**: 2.0 seconds
- **What happens**: Prepare for final step

### Step 15: 🖱️ Click at New Position
- **Coordinates**: (25, 40)
- **Purpose**: Click at new user-specified coordinates
- **Wait Time**: 2.0 seconds
- **What happens**: **🔄 LOOP BEGINS HERE** - Ready for next image selection

---

## Image Grid Coordinates Reference

### Row 1 (Images 1-4)
- Image 1: (426, 179) - Row 1, Col 1
- Image 2: (498, 179) - Row 1, Col 2  
- Image 3: (570, 179) - Row 1, Col 3
- Image 4: (642, 179) - Row 1, Col 4

### Row 2 (Images 5-8)
- Image 5: (426, 259) - Row 2, Col 1
- Image 6: (498, 259) - Row 2, Col 2
- Image 7: (570, 259) - Row 2, Col 3
- Image 8: (642, 259) - Row 2, Col 4

### Row 3 (Images 9-12)
- Image 9: (426, 339) - Row 3, Col 1
- Image 10: (498, 339) - Row 3, Col 2
- Image 11: (570, 339) - Row 3, Col 3
- Image 12: (642, 339) - Row 3, Col 4

### Row 4 (Images 13-16)
- Image 13: (426, 419) - Row 4, Col 1
- Image 14: (498, 419) - Row 4, Col 2
- Image 15: (570, 419) - Row 4, Col 3
- Image 16: (642, 419) - Row 4, Col 4

---

## Usage Commands

### Run Single Image
```bash
python3 named_step_automation.py <image_number>
```

### Examples
```bash
python3 named_step_automation.py 8    # Process Image #8
python3 named_step_automation.py 12   # Process Image #12
python3 named_step_automation.py 16   # Process Image #16
```

---

## Debugging

When a step fails, you'll see exactly which step name failed:
- Check the coordinates for that specific step
- Verify the UI hasn't changed
- Update coordinates if needed in `named_step_automation.py`

The step names make it easy to identify and fix issues without guessing!
