import cv2
import numpy as np
import subprocess
import os

def open_chrome(ip_address):
    """Open the Chrome app using ADB."""
    package_name = "com.android.chrome"
    adb_open_command = ["adb", "-s", ip_address, "shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"]
    subprocess.run(adb_open_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Chrome app launched.")

def take_screenshot(ip_address):
    """Capture the screen using ADB and return the image."""
    screenshot_path = "/storage/emulated/0/screen.png"
    adb_screencap_command = ["adb", "-s", ip_address, "shell", "screencap", screenshot_path]
    subprocess.run(adb_screencap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Pull the screenshot from the device to the local file system
    adb_pull_command = ["adb", "-s", ip_address, "pull", screenshot_path, "/home/kali/screen.png"]
    subprocess.run(adb_pull_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Load the screenshot as a cv2 image
    screen_img = cv2.imread("/home/kali/screen.png", cv2.IMREAD_COLOR)
    if screen_img is None:
        print("Failed to capture screen.")
        return None
    
    return screen_img

def template_match_and_click(ip_address, template_path):
    """Use OpenCV to find the 'new tab' button and click on it."""
    screen_img = take_screenshot(ip_address)
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

        # Simulate a tap at the found coordinates using ADB
        adb_tap_command = ["adb", "-s", ip_address, "shell", "input", "tap", str(click_x), str(click_y)]
        subprocess.run(adb_tap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Tapped on {click_x}, {click_y}")
    else:
        print(f"Template not found. Max value: {max_val}")

def main():
    # Replace this with your actual device IP or identifier
    device_ip_address = "192.168.1.239:5555"
    
    # Path to the newTab.png image stored in Android's internal storage
    template_path = "/storage/emulated/0/myproject/newTab/newTab.png"
    
    # Connect to the device over ADB
    adb_connect_command = ["adb", "connect", device_ip_address]
    subprocess.run(adb_connect_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Launch Chrome using ADB
    open_chrome(device_ip_address)
    
    # Perform template matching and click the new tab button
    template_match_and_click(device_ip_address, template_path)

if __name__ == "__main__":
    main()
