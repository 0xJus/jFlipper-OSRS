import pyautogui
import pygetwindow as gw
import logging
import time
import cv2
import numpy as np
import keyboard
import sys

# Default values for delays
click_delay = 0.7
sleep_delay = 0.7

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="jFlipper - %(asctime)s: %(message)s",
    datefmt="%I:%M:%S %p",  # 12-hour format with AM/PM
)

window_title = "RuneLite"


def focus_rune_lite():
    """Brings the RuneLite window to the foreground if found."""
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        logging.info(f"Window '{window_title}' found. Bringing it to the foreground.")
        windows[0].activate()
        return True
    logging.warning(f"No window found with the title '{window_title}'.")
    return False


def click(x, y, delay):
    """Moves the mouse to (x, y), waits for the delay, and clicks."""
    pyautogui.moveTo(x, y)
    time.sleep(delay)
    pyautogui.click()


def locate_image(image_path, confidence=0.85, screenshot=None):
    """Locates an image on the screen and returns its top-left corner coordinates."""
    if screenshot is None:
        screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        logging.error(f"Failed to load template image: {image_path}")
        return None

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    return max_loc if max_val >= confidence else None


def click_red(screenshot, click_delay):
    """Searches for and clicks the red-highlighted area."""
    abort_offer_loc = locate_image("images/abortofferfor.png", screenshot=screenshot)

    if abort_offer_loc:
        logging.info(
            "Abort offer suggested action found. Searching for red highlighted area."
        )
        mask = cv2.inRange(screenshot, np.array([35, 40, 115]), np.array([41, 48, 128]))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
                pyautogui.moveTo(cX, cY)
                pyautogui.keyDown("shift")
                click(cX, cY, click_delay)
                pyautogui.keyUp("shift")
                logging.info("Red highlighted area found and shift-clicked.")


def click_blue(screenshot, click_delay):
    """Searches for and clicks the blue-highlighted area."""
    if set_to_suggested_item(
        screenshot, click_delay
    ) or set_to_copilot_price_and_quantity(screenshot, click_delay):
        return

    mask = cv2.inRange(screenshot, np.array([100, 90, 50]), np.array([120, 115, 78]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            pyautogui.moveTo(cX, cY)
            click(cX, cY, click_delay)
            logging.info("Blue highlighted area found and clicked.")


def set_to_copilot_price_and_quantity(screenshot, click_delay):
    """Clicks the 'Set to CoPilot' button if found."""
    loc = locate_image("images/settocopilot.png", screenshot=screenshot)
    if loc:
        click(*loc, click_delay)
        pyautogui.press("enter")
        time.sleep(sleep_delay)
        logging.info("Set to CoPilot button clicked.")
        return True
    return False


def set_to_suggested_item(screenshot, click_delay):
    """Clicks the 'Set to Suggested Item' button if found."""
    loc = locate_image("images/suggesteditem.png", screenshot=screenshot)
    if loc:
        click(*loc, click_delay)
        logging.info("Set to Suggested Item button clicked.")
        return True
    return False


def run_jFlipper(click_delay, sleep_delay):
    """Main script logic to automate flipping tasks in RuneLite."""
    pyautogui.FAILSAFE = True

    if not focus_rune_lite():
        logging.error(
            "RuneLite window not found. Please log in and open the Grand Exchange."
        )
        sys.exit()

    # Define the region to capture screenshots (primary monitor area)
    region = (0, 0, 1919, 890)

    while True:
        if keyboard.is_pressed("space"):
            logging.info("jFlipper script has been stopped.")
            break

        # Check if the Grand Exchange interface is still open
        screenshot = cv2.cvtColor(
            np.array(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR
        )
        if not locate_image("images/ge.png", screenshot=screenshot):
            logging.info("Grand Exchange not open. Exiting script.")
            break

        logging.info("Idling...Waiting for task...")
        screenshot = cv2.cvtColor(
            np.array(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR
        )

        click_red(screenshot, click_delay)
        click_blue(screenshot, click_delay)

        time.sleep(sleep_delay)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            click_delay = float(sys.argv[1])
        except ValueError:
            pass  # Use default value
    if len(sys.argv) > 2:
        try:
            sleep_delay = float(sys.argv[2])
        except ValueError:
            pass  # Use default value

    run_jFlipper(click_delay, sleep_delay)
