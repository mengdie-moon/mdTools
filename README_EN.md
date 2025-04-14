# mdTools

English|[中文](README.md)

mdTools is a versatile open-source utility library written in Python, designed to provide convenient development tools and improve development efficiency. This library integrates multiple commonly used functions to greatly simplify repetitive work in the development process, helping developers focus more on implementing core business logic.

## Use Cases

1. **Rapid Development Scenarios**
   - Need to quickly implement basic functions without reinventing the wheel
   - Similar utility functions are frequently needed across multiple projects
   - Want to uniformly manage and maintain commonly used tool code

2. **Automation Testing and Scripting**
   - Need to simulate user operations for automated testing
   - Batch processing of files and data
   - Need screenshot recording or automated UI testing

3. **Desktop Application Development**
   - Need mouse and keyboard control
   - Need to create user interaction interfaces and prompts
   - Need screen capture and image processing

## Features

The library contains four main modules(Not updated yet):

1. **Main Tools (mdTools_main)**

2. **Mouse Operation (mdTools_mouse)**

3. **Popup Windows (mdTools_popup)**

4. **Screenshot (mdTools_screenshot)**

## Installation

There is currently no installation method available (due to the inability to input API when uploading Pypi on Windows). If anyone knows a solution and wants to help me, please contact me` 3257053519@qq.com `)

## Usage Example

```python
from mdTools import mdTools

# Create tool instance
tool = mdTools()

# Generate random password
password = tool.randomPassword(length=12, isNumber=True, isStr=True, isNotation=True)
print(f"Generated password: {password}")

# Base64 encoding
encoded = tool.base64_encode("Hello World")
print(f"Base64 encoded result: {encoded}")

# Mouse operations
tool.mouse_move(100, 100)  # Move mouse to specified position
tool.mouse_click()         # Click mouse

# Show message box
tool.MPopup_messagebox("Operation successful", "Prompt", "info")

# Take screenshot
tool.md_screenshot(0, 0, 800, 600, "screenshot.png")
```

## Requirements

- Python >= 3.6
- Operating System: Windows/Linux/MacOS

## License

Apache License 2.0

## Author Information

- Author: MengDie
- Email: 3257053519@qq.com
- Author's note: Originally intended to upload pypi, but later encountered an error and uploaded it to GitHub