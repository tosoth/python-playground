import tkinter as tk
from tkhtmlview import HTMLLabel
import webview

import datetime
import os
import sys
import re

from pystardict import Dictionary

dicts_dir = 'C:\\Users\\2346318\\coding'
dict1 = Dictionary(os.path.join(dicts_dir, 'Collins5'))

# List to store the search history
search_history = []

def fix_bold_space(html_string):
    """
    Replaces "</b> <b>" with "</b>&nbsp;<b>" in an HTML string.

    Args:
        html_string (str): The HTML string to modify.

    Returns:
        str: The modified HTML string.
    """
    return re.sub(r"</b> <b>", r" ", html_string)

def modernize_font_tags(html_snippet):
    """Replaces <FONT COLOR="..."> with <span style="color: ...">."""
    pattern = r'<FONT COLOR="([^"]*)">(.*?)</FONT>'
    replacement = r'<span style="color: \1">\2</span>'
    return re.sub(pattern, replacement, html_snippet, flags=re.IGNORECASE)

# Define the function to display HTML content
def show_html_content(event=None):
    global the_word, html_label
    the_word = input_box.get()

    html_content = modernize_font_tags(dict1.dict[the_word])

    html_content = fix_bold_space(html_content)

    if 'html_label' in globals():
        html_label.pack_forget()  # Remove the old HTMLLabel widget

    html_label = HTMLLabel(root, html=html_content)
    html_label.pack()

    window = webview.create_window('HTML Viewer', html=html_content)
    
    input_box.select_range(0, tk.END)
    input_box.icursor(tk.END)

    word = the_word
    # Append the searched word to the search history
    if word not in search_history:
        search_history.append(word)
        # Save the updated search history to the file
        with open('history-word-list.txt', 'a') as file:
            file.write(word + '\n')

def exit_app(event=None):
    root.destroy()

def select_all_in_input_box(event=None):
    """Selects all text in the input_box."""
    input_box.select_range(0, tk.END)
    input_box.icursor(tk.END) # Places the cursor at the end of the selected text

# Create the main window
root = tk.Tk()
root.title("Collins5 stardict app")

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness
except:
    pass

input_box = tk.Entry(root, width=50)
input_box.pack(pady=10)

# Create a button to trigger the HTML display
button = tk.Button(root, text="Start", command=show_html_content)
button.pack(pady=20)

# Bind the Enter key to the button click event
root.bind('<Return>', show_html_content)
root.bind('<Escape>', exit_app)

# Bind a click on the root window to select all in the input box
root.bind("<Button-1>", select_all_in_input_box)

# Set focus to the input box when the app starts
input_box.focus_set()

# Run the application
root.mainloop()
