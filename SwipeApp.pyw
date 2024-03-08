import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time
from datetime import datetime

# Global variables for swipe counts
right_swipes = 0
left_swipes = 0
total_swipes = 0
running = None
start_time = None

# Function to perform swipes
def perform_swipes():
    global right_swipes, left_swipes, total_swipes
    while running.is_set():  # Check if the stop button was clicked
        subprocess.call("adb shell input touchscreen swipe 100 459 1260 472", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        right_swipes += 1
        total_swipes += 1
        update_labels()
        time.sleep(1)
        subprocess.call("adb shell input touchscreen swipe 100 459 1260 472", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        right_swipes += 1
        total_swipes += 1
        update_labels()
        time.sleep(1)
        subprocess.call("adb shell input touchscreen swipe 640 960 200 960", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        left_swipes += 1
        total_swipes += 1
        update_labels()
        time.sleep(1)

# Function to update labels
def update_labels():
    right_swipes_label.config(text=f"Right Swipes: {right_swipes}")
    left_swipes_label.config(text=f"Left Swipes: {left_swipes}")
    total_swipes_label.config(text=f"Total Swipes: {total_swipes}")

# Function to start swipes
def start_swipes():
    global running, start_time
    running = threading.Event()
    start_time = datetime.now()
    running.set()  # Set the event to indicate that the swipes are running
    swipes_thread = threading.Thread(target=perform_swipes)
    swipes_thread.start()
    update_stopwatch()

# Function to stop swipes
def stop_swipes():
    global running
    running.clear()  # Clear the event to stop the swipes

# Function to update stopwatch
def update_stopwatch():
    if running.is_set():
        current_time = datetime.now()
        elapsed_time = current_time - start_time
        stopwatch_label.config(text=f"Duration: {elapsed_time}")
        stopwatch_label.after(1000, update_stopwatch)

# Function to update date and time
def update_date_time():
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_label.config(text=f"Current Date Time: {current_date_time}")
    date_time_label.after(1000, update_date_time)

# Create main window
root = tk.Tk()
root.title("Touchscreen Swiper")

# Add start button
start_button = tk.Button(root, text="Start Swipes", command=start_swipes, width=15, padx=10, pady=5)
start_button.grid(row=0, column=0, padx=10, pady=10)

# Add stop button
stop_button = tk.Button(root, text="Stop Swipes", command=stop_swipes, width=15, padx=10, pady=5)
stop_button.grid(row=0, column=1, padx=10, pady=10)

# Add labels for swipe counts
right_swipes_label = tk.Label(root, text="Right Swipes: 0", padx=10, pady=5)
right_swipes_label.grid(row=1, column=0, padx=10, pady=5)

left_swipes_label = tk.Label(root, text="Left Swipes: 0", padx=10, pady=5)
left_swipes_label.grid(row=2, column=0, padx=10, pady=5)

total_swipes_label = tk.Label(root, text="Total Swipes: 0", padx=10, pady=5)
total_swipes_label.grid(row=3, column=0, padx=10, pady=5)

# Add label for stopwatch
stopwatch_label = tk.Label(root, text="Duration: 0:00:00", padx=10, pady=5)
stopwatch_label.grid(row=4, column=0, padx=10, pady=5)

# Add label for current date and time
date_time_label = tk.Label(root, text="Current Date Time: ", padx=10, pady=5)
date_time_label.grid(row=5, column=0, padx=10, pady=5)

# Start updating date and time
update_date_time()

# Run the Tkinter event loop
root.mainloop()
