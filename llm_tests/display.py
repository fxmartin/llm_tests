#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name: display.py
Author: FX
Date Created: 2025-02-22
Last Modified: 2025-02-22
Description:
    This script provides a wrapper for the colorama library.

Usage:
    This script is meant to be called from another Python script with the following functions:
        - from XXXXXXX.display import Display
        - Example usage
            display = ColoramaWrapper()
            print(display.color_text("Hello in Red!", color="red"))
            print(display.color_text("Bright Yellow on Blue!", color="yellow", background="blue", style="bright"))
            print(display.color_text("Dim Green Text", color="green", style="dim"))

Requirements:
    - Python 3.x
    - Required libraries (colorama)

Notes:
    - Follow PEP 8 for coding style.
    - Ensure comments are updated when code changes.

License:
    MIT License. See LICENSE file for details.
"""

from colorama import Fore, Back, Style, init # Import the colorama library to enable colored text in terminal

class ColoramaWrapper:
    # A class to display messages with colors using the colorama library
    def __init__(self):
        # Initialize colorama (ensures compatibility with Windows terminals)
        init(autoreset=True)

    def color_text(self, text: str, color: str = None, background: str = None, style: str = None) -> str:
        """
        Apply foreground color, background color, and style to the given text.

        Args:
            text (str): The text to style.
            color (str): The foreground color (e.g., "RED", "GREEN").
            background (str): The background color (e.g., "BLACK", "YELLOW").
            style (str): The text style (e.g., "BRIGHT", "DIM").

        Returns:
            str: The styled text.
        """
        styled_text = ""

        # Apply foreground color
        if color and hasattr(Fore, color.upper()):
            styled_text += getattr(Fore, color.upper())

        # Apply background color
        if background and hasattr(Back, background.upper()):
            styled_text += getattr(Back, background.upper())

        # Apply style
        if style and hasattr(Style, style.upper()):
            styled_text += getattr(Style, style.upper())

        # Add the text and reset formatting
        styled_text += text

        return styled_text

    def reset(self) -> str:
        """
        Reset all styles (useful for manual resets).
        
        Returns:
            str: The reset code.
        """
        return Style.RESET_ALL

# Example usage
if __name__ == "__main__":
    wrapper = ColoramaWrapper()

    print(wrapper.color_text("Hello in Red!", color="red"))
    print(wrapper.color_text("Bright Yellow on Blue!", color="yellow", background="blue", style="bright"))
    print(wrapper.color_text("Dim Green Text", color="green", style="dim"))
