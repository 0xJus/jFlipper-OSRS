# Flipper-OSRS

## Overview

This very simple Python script automates flipping items in the OSRS Grand Exchange using the OSRS RuneLite client application along with the Flipping CoPilot RuneLite plugin. The script is designed to enhance efficiency by automating the buying and selling process of suggested copilot items to maximize profits.

## Features

- **Automated Item Flipping**: Automatically handles the purchase and sale of items on the Grand Exchange based on parameters set in the Flipping CoPilot plugin. This ensures consistent profit generation without manual intervention.

- **Image and Color Recognition**: Utilizes powerful image recognition libraries (such as OpenCV) to interact with the RuneLite interface, accurately detecting and responding to in-game elements. Color detection is used to verify key actions, ensuring precise execution.

- **CPU Optimization**: The script is optimized to minimize CPU usage by taking screenshots only when necessary. This is particularly beneficial for users with less powerful computers, allowing the script to run efficiently without significant performance impact.

- **User-Friendly GUI**: Includes a simple and intuitive graphical user interface (GUI) built with `tkinter` and `customtkinter`. The GUI allows users to start the script with ease.

- **Customizable Settings**: Users can easily adjust various parameters within the GUI, such as sleep intervals and click delays, allowing for flexible and personalized automation settings.

## Requirements

- **OSRS RuneLite**: [Download RuneLite](https://runelite.net/)
- **Flipping CoPilot RuneLite Plugin**: Install via the RuneLite plugin hub.
- **Python 3.x**: [Download Python](https://www.python.org/)
- **Python Packages**:
  - `pyautogui`
  - `opencv-python`
  - `numpy`

You can install the required packages using pip:

```bash
pip install  -r requirements.txt
```

## Usage

### Setup RuneLite:

1. Install and configure the Flipping CoPilot plugin within RuneLite.
2. Ensure RuneLite is running with the Grand Exchange window open.

### Run the Script

1. Execute the script from the command line:

   ```bash
   python jFlipper.py
   ```

2. **Automation Process**: The script will start monitoring the RuneLite interface, performing automated clicks and keystrokes to buy and sell items based on the configurations in the Flipping CoPilot plugin.

## Important Notes

- **Legal Disclaimer**: Use this script at your own risk. Automating actions in games may violate the terms of service with RuneLite, Flipping CoPilot, and RuneScape, leading to account penalties.
- **Optimization**: Ensure your script is fine-tuned to avoid detection, such as using appropriate sleep intervals and randomizing actions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **RuneLite** for their open-source application.
- The developers of the **Flipping CoPilot** plugin for their amazing contributions to the OSRS community.
