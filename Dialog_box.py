import subprocess
import tkinter as tk
from tkinter import filedialog

def select_input_file():
    input_file = filedialog.askopenfilename(title="Select Input File")
    if input_file:
        input_path_label.config(text=input_file)

def select_output_folder():
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if output_folder:
        output_path_label.config(text=output_folder)

# Changed to call second script

def convert():
    input_path = input_path_label.cget("text")
    output_path = output_path_label.cget("text")
    if input_path and output_path:
        try:
            # Call the separate Python script
            subprocess.run(
                ["python", "Image_converter.py", input_path, output_path],
                check=True
            )
            print("Conversion completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
    else:
        print("Please specify both input and output paths.")


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

# Run the application
root.mainloop()