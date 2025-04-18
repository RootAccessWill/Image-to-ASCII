import tkinter as tk
from tkinter import filedialog
import subprocess
import sys
import threading
from io import StringIO

class GuiOutputRedirector:
    """
    A class to redirect stdout and stderr to a Tkinter Text widget.
    """
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Auto-scroll to the bottom

    def flush(self):
        pass  # Needed for compatibility with Python's file-like objects

def select_input_file():
    input_file = filedialog.askopenfilename(title="Select Input File")
    if input_file:
        input_path_label.config(text=input_file)

def select_output_folder():
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if output_folder:
        output_path_label.config(text=output_folder)

def convert():
    input_path = input_path_label.cget("text")
    output_path = output_path_label.cget("text")
    if input_path and output_path:
        output_text.delete(1.0, tk.END)  # Clear any previous output
        # Run the conversion in a separate thread to avoid freezing the GUI
        threading.Thread(target=run_conversion, args=(input_path, output_path)).start()
    else:
        output_text.insert(tk.END, "Please specify both input and output paths.\n")

def run_conversion(input_path, output_path):
    try:
        # Call the separate Python script
        subprocess.run(
            ["python", "Image_converter.py", input_path, output_path],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        print("Conversion completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Image Converter")

# Input file selection
tk.Label(root, text="Input File:").grid(row=0, column=0, padx=10, pady=10)
input_path_label = tk.Label(root, text="", bg="white", anchor="w", width=40)
input_path_label.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

# Output folder selection
tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10)
output_path_label = tk.Label(root, text="", bg="white", anchor="w", width=40)
output_path_label.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

# Convert button
tk.Button(root, text="Convert", command=convert).grid(row=2, column=1, pady=20)

# Output display
output_text = tk.Text(root, height=10, width=60, bg="white")
output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Redirect stdout and stderr to the Text widget
sys.stdout = GuiOutputRedirector(output_text)
sys.stderr = GuiOutputRedirector(output_text)

# Run the application
root.mainloop()