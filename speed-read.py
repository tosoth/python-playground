import time
import pyperclip
import tkinter as tk

# Initialize the speed factor and pause flag
speed_factor = 1.2
paused = False

# Function to display words one by one
def display_words(words):
    global paused
    for word in words:
        while paused:
            root.update()
            time.sleep(0.1)
        label.config(text=word)
        root.update()
        if ',' in word:
            time.sleep(0.5 * speed_factor)  # Longer pause for comma
        elif '.' in word:
            time.sleep(1 * speed_factor)  # Longer pause for period
        elif len(word)>6:
            time.sleep((0.2+0.02*(len(word)-6)) * speed_factor)  # Longer pause for period
        else:
            time.sleep(0.2 * speed_factor)  # Regular pause

# Function to get text from clipboard and start displaying words
def start_speed_read(event=None):
    text = pyperclip.paste()
    words = text.split()
    display_words(words)

# Function to increase the speed
def increase_speed(event=None):
    global speed_factor
    speed_factor = max(0.1, speed_factor - 0.1)  # Decrease the factor to increase speed

# Function to decrease the speed
def decrease_speed(event=None):
    global speed_factor
    speed_factor += 0.1  # Increase the factor to decrease speed
    print(0.2 * speed_factor)

# Function to pause/resume the word playing
def toggle_pause(event=None):
    global paused
    paused = not paused

# Function to exit the application
def exit_app(event=None):
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Speed Read App")

# Set a fixed window size
window_width = 800
window_height = 200
root.geometry(f"{window_width}x{window_height}")

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness
except:
    pass

# Create a label to display the words
# label = tk.Label(root, font=("Helvetica", 48))
label = tk.Label(root, font=("Amazon Amber", 48))
label.pack(pady=20)

# Create a button to start the speed reading
start_button = tk.Button(root, text="Start Speed Reading", command=start_speed_read)
start_button.pack(pady=20)

# Bind Ctrl+V to start_speed_read function
root.bind('<Control-v>', start_speed_read)

# Bind "+" to increase_speed function
root.bind('<plus>', increase_speed)

# Bind "-" to decrease_speed function
root.bind('<minus>', decrease_speed)

# Bind "spacebar" to toggle_pause function
root.bind('<space>', toggle_pause)

# Bind "enter" to start_speed_read function
root.bind('<Return>', start_speed_read)

# Bind "ESC" to exit_app function
root.bind('<Escape>', exit_app)

# Run the application
root.mainloop()
