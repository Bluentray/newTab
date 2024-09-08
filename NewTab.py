# i want create a script that uses opencv , adb
# my environment is on my android phone in termux, kail linux, venv
# the task is to open package app com.android.chrome
# use opencv to template match a image to click on
# image name newTab.png


import cv2
import numpy as np
import subprocess
import os

def open_chrome():
    """Open the Chrome app using Android's Activity Manager via Termux."""
    os.system("am start -n com.android.chrome/com.google.android.apps.chrome.Main")
    print("Chrome app launched.")

def take_screenshot():
    """Capture the screen using Termux's screencap command and return the image."""
    screencap_command = ["screencap", "-p", "/storage/emulated/0/screen.png"]
    subprocess.run(screencap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Load the screenshot as a cv2 image
    screen_img = cv2.imread("/storage/emulated/0/screen.png", cv2.IMREAD_COLOR)
    if screen_img is None:
        print("Failed to capture screen.")
        return None
    
    return screen_img

def template_match_and_click(template_path):
    """Use OpenCV to find the 'new tab' button and click on it."""
    screen_img = take_screenshot()
    if screen_img is None:
        return

    # Load the template image (newTab.png)
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"Failed to load template image: {template_path}")
        return
    
    # Convert both images to grayscale for template matching
    screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # Perform template matching
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust this threshold value if necessary
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= threshold:
        print(f"Template matched with max value: {max_val}")
        h, w = template_gray.shape
        click_x = max_loc[0] + w // 2
        click_y = max_loc[1] + h // 2
        print(f"Clicking at ({click_x}, {click_y})")

        # Simulate a tap at the found coordinates using input tap
        tap_command = ["input", "tap", str(click_x), str(click_y)]
        subprocess.run(tap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Tapped on {click_x}, {click_y}")
    else:
        print(f"Template not found. Max value: {max_val}")

def main():
    # Path to the newTab.png image stored in Android's internal storage
    template_path = "/storage/emulated/0/myproject/newTab/newTab.png"
    
    # Launch Chrome using am
    open_chrome()
    
    # Perform template matching and click the new tab button
    template_match_and_click(template_path)

if __name__ == "__main__":
    main()
