import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Initialize global variables
input_folder = ""
output_folder = ""

# Function to adjust images (Convert all non-transparent pixels to white)
def adjust_image(image):
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    norm = cv2.normalize(grayscale, None, alpha=100, beta=255, norm_type=cv2.NORM_MINMAX)
    _, white_mask = cv2.threshold(norm, 1, 255, cv2.THRESH_BINARY)
    white_image = np.full_like(image, 255)
    final = cv2.bitwise_and(white_image, white_image, mask=white_mask)
    return final

# Function to process images with a progress bar
def process_images():
    global input_folder, output_folder

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Please select both input and output folders!")
        return

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    total_images = len(image_files)

    if total_images == 0:
        messagebox.showwarning("Warning", "No valid images found in the input folder.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Reset progress bar
    progress_bar["maximum"] = total_images
    progress_bar["value"] = 0
    progress_label.config(text="Processing images...")  
    root.update_idletasks()

    for i, filename in enumerate(image_files, 1):
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        if image is None:
            continue

        if image.shape[-1] == 4:  # Handle PNG transparency
            alpha_channel = image[:, :, 3]
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
            edited_image = adjust_image(image)
            edited_image = cv2.merge([edited_image, alpha_channel])
        else:
            edited_image = adjust_image(image)

        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, edited_image)

        # Update progress bar
        progress_bar["value"] = i
        progress_label.config(text=f"Processed {i}/{total_images} images")
        root.update_idletasks()

    messagebox.showinfo("Success", "Logos have been edited and saved!")
    progress_label.config(text="Processing Complete")

# GUI Functions to select folders
def select_input_folder():
    global input_folder
    input_folder = filedialog.askdirectory()
    input_label.config(text=f"Input: {input_folder}")

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    output_label.config(text=f"Output: {output_folder}")

# Initialize GUI
root = tk.Tk()
root.title("Logo Editor")
root.geometry("400x300")
root.resizable(False, False)

# Widgets
tk.Label(root, text="Anshi Logo Editor ", font=("Arial", 14, "bold")).pack(pady=10)

input_label = tk.Label(root, text="Input: Not Selected", wraplength=350)
input_label.pack()
tk.Button(root, text="Select Input Folder", command=select_input_folder).pack(pady=5)

output_label = tk.Label(root, text="Output: Not Selected", wraplength=350)
output_label.pack()
tk.Button(root, text="Select Output Folder", command=select_output_folder).pack(pady=5)

tk.Button(root, text="Edit Logos", command=process_images, bg="lightblue").pack(pady=10)

# Progress Bar
progress_label = tk.Label(root, text="")
progress_label.pack()
progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=5)

# Run GUI
root.mainloop()
