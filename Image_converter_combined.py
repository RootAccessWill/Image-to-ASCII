import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import threading
import sys
from PIL import Image


class GuiOutputRedirector:
    """
    Redirects standard output and error to a Tkinter text widget.
    """
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass  # Needed for compatibility with Python's file-like objects


class ImageConverter:
    """
    A class to handle image-to-ASCII conversion.
    """
    def __init__(self, image_path):
        """
        Initializes the ImageConverter with the given image path.
        """
        try:
            self.image = Image.open(image_path)
        except Exception as e:
            raise ValueError(f"Error: Unable to open image. {e}")

    def convert_to_ascii(self, scale_factor):
        """
        Converts the image to ASCII art and returns it as a string.

        Args:
            scale_factor (float): The scaling factor for resizing the image.

        Returns:
            str: The ASCII representation of the image.
        """
        ascii_chars = '~!@#$%^&*()_+|}{":?><,./;[]\\`-= '
        ascii_art = ''

        # Get image dimensions
        width, height = self.image.size

        # Adjust height for ASCII aspect ratio (e.g., 2:1)
        adjusted_height = int(height / 2)
        new_width = int(width * scale_factor)
        new_height = int(adjusted_height * scale_factor)

        # Resize and convert to grayscale
        resized_image = self.image.resize((new_width, new_height))
        grayscale_image = resized_image.convert('L')

        # Convert pixel values to ASCII characters
        ASCII_BUCKET_SIZE = 256 // len(ascii_chars)
        pixel_values = list(grayscale_image.getdata())
        ascii_art_lines = [
            ''.join(ascii_chars[pixel_value // ASCII_BUCKET_SIZE] for pixel_value in pixel_values[i:i + new_width])
            for i in range(0, len(pixel_values), new_width)
        ]
        ascii_art = '\n'.join(ascii_art_lines)

        return ascii_art


def select_input_file():
    """
    Opens a file dialog for the user to select an input image file.
    """
    input_file = filedialog.askopenfilename(title="Select Input File")
    if input_file:
        input_path_label.config(text=input_file)
    else:
        output_text.insert(tk.END, "No input file selected.\n")


def select_output_folder():
    """
    Opens a folder dialog for the user to select an output folder.
    """
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if output_folder:
        output_path_label.config(text=output_folder)
    else:
        output_text.insert(tk.END, "No output folder selected.\n")


def convert():
    """
    Initiates the conversion process in a separate thread.
    """
    input_path = input_path_label.cget("text")
    output_path = output_path_label.cget("text")
    size = size_slider.get() / 100  # Get the scaling factor from the slider (convert to a fraction)

    if input_path and output_path:
        output_text.delete(1.0, tk.END)  # Clear any previous output
        threading.Thread(target=run_conversion, args=(input_path, output_path, size)).start()
    else:
        output_text.insert(tk.END, "Please specify both input and output paths.\n")


def run_conversion(input_path, output_path, scale_factor):
    """
    Performs the image-to-ASCII conversion and writes the result to a file.
    """
    try:
        # Construct the output file path
        output_file = Path(output_path) / (Path(input_path).stem + "_ascii.txt")

        # Convert the image to ASCII
        converter = ImageConverter(input_path)
        ascii_art = converter.convert_to_ascii(scale_factor)

        # Save the ASCII art to a file
        with open(output_file, 'w') as f:
            f.write(ascii_art)

        # Display success message
        root.after(0, lambda: output_text.insert(tk.END, f"ASCII art saved to {output_file}\n"))
    except Exception as e:
        # Capture the exception message
        error_message = str(e)
        root.after(0, lambda: output_text.insert(tk.END, f"An error occurred: {error_message}\n"))


# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Image to ASCII Converter")

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

# ASCII size slider
tk.Label(root, text="Scale Factor (%):").grid(row=2, column=0, padx=10, pady=10)
size_slider = tk.Scale(root, from_=10, to=200, orient=tk.HORIZONTAL, length=300)
size_slider.set(100)  # Default scale factor (100%)
size_slider.grid(row=2, column=1, padx=10, pady=10)

# Convert button
tk.Button(root, text="Convert", command=convert).grid(row=3, column=1, pady=20)

# Output text box
output_text = tk.Text(root, height=10, width=60, bg="white")
output_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Redirect stdout and stderr to the GUI
sys.stdout = GuiOutputRedirector(output_text)
sys.stderr = GuiOutputRedirector(output_text)

# Start the Tkinter main loop
root.mainloop()