import tkinter as tk
from screeninfo import get_monitors

# Ensure the Amazon Ember font is installed on your system

# Get the screen dimensions
screen = get_monitors()[0]
screen_width = screen.width
screen_height = screen.height

# Calculate the dimensions for the edit box (75% of the screen)
edit_box_width = int(screen_width * 0.75)
edit_box_height = int(screen_height * 0.75)

# Create the main application window
root = tk.Tk()
root.title("Edit Box Window")

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness
except:
    pass

# Set the size and position of the window
root.geometry(f"{edit_box_width}x{edit_box_height}+{int(screen_width * 0.125)}+{int(screen_height * 0.125)}")

# Function to close the application
def close_app(event):
    root.quit()

# Bind the 'Escape' key to the close_app function
root.bind('<Escape>', close_app)

# Create a text widget (edit box) with Amazon Ember font and word wrapping
text_widget = tk.Text(root, font=("Amazon Ember", 24), fg="light green", bg="dark green", wrap=tk.WORD)
text_widget.pack(expand=True, fill=tk.BOTH)

scrollbar = tk.Scrollbar(text_widget, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

# Function to insert clipboard text into the text widget
def insert_clipboard_text():
    try:
        clipboard_text = root.clipboard_get()
        text_widget.insert(tk.END, clipboard_text)
    except tk.TclError:
        text_widget.insert(tk.END, "Clipboard is empty or does not contain text")

# Insert clipboard text when the application starts
insert_clipboard_text()

# Run the application
root.mainloop()

