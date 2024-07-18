import os
from PIL import Image
import numpy as np
import svgwrite
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def image_to_svg(image_path, svg_path):
    try:
        # Open the image using PIL
        image = Image.open(image_path).convert('RGBA')
        image_array = np.array(image)
        
        # Create an SVG drawing
        dwg = svgwrite.Drawing(svg_path, profile='tiny')
        
        for y in range(image_array.shape[0]):
            for x in range(image_array.shape[1]):
                r, g, b, a = image_array[y, x]
                if a > 0:  # Only add non-transparent pixels
                    dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill=svgwrite.rgb(r, g, b, '%')))
        
        # Save the SVG file
        dwg.save()
        print(f'Successfully converted {image_path} to {svg_path}')
    except Exception as e:
        print(f'Failed to convert {image_path}: {e}')

def resize_image(image, max_size):
    width, height = image.size
    if width > height:
        if width > max_size:
            height = int((max_size / float(width)) * float(height))
            width = max_size
    else:
        if height > max_size:
            width = int((max_size / float(height)) * float(width))
            height = max_size
    return image.resize((width, height), Image.Resampling.LANCZOS)

def image_to_ico(image_path, ico_path, max_size=100):
    try:
        # Open the image using PIL
        image = Image.open(image_path)
        
        # Resize the image to the maximum size while maintaining aspect ratio
        image = resize_image(image, max_size)
        
        # Save as ICO
        image.save(ico_path, format='ICO')
        print(f'Successfully converted {image_path} to {ico_path}')
    except Exception as e:
        print(f'Failed to convert {image_path}: {e}')

def convert_directory_to_svg(source_dir):
    output_dir = os.path.join(source_dir, 'Converted_to_SVG')
    os.makedirs(output_dir, exist_ok=True)
    
    file_count = 0
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.webp', '.jpg', '.jpeg', '.png', '.tif')):
            image_path = os.path.join(source_dir, filename)
            svg_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.svg')
            print(f'Converting {image_path} to {svg_path}...')
            image_to_svg(image_path, svg_path)
            file_count += 1
    return file_count

def convert_directory_to_ico(source_dir):
    output_dir = os.path.join(source_dir, 'Converted_to_ICO')
    os.makedirs(output_dir, exist_ok=True)
    
    file_count = 0
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.webp', '.jpg', '.jpeg', '.png', '.tif')):
            image_path = os.path.join(source_dir, filename)
            ico_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.ico')
            print(f'Converting {image_path} to {ico_path}...')
            image_to_ico(image_path, ico_path)
            file_count += 1
    return file_count

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    while True:
        source_dir = filedialog.askdirectory(title="Select the directory containing image files")
        if not source_dir:
            messagebox.showinfo("No Directory Selected", "No directory selected. Exiting.")
            return
        
        if not os.path.isdir(source_dir):
            messagebox.showerror("Invalid Directory", "The provided path is not a directory or does not exist.")
            continue
        
        conversion_choice = simpledialog.askstring("Conversion Choice", "Enter 'SVG' to convert to SVG or 'ICO' to convert to ICO:").strip().upper()
        if conversion_choice == 'SVG':
            file_count = convert_directory_to_svg(source_dir)
            message = f"All image files have been converted to SVG and saved in the 'Converted_to_SVG' directory.\nNumber of files processed: {file_count}"
        elif conversion_choice == 'ICO':
            file_count = convert_directory_to_ico(source_dir)
            message = f"All image files have been converted to ICO and saved in the 'Converted_to_ICO' directory.\nNumber of files processed: {file_count}"
        else:
            messagebox.showerror("Invalid Choice", "Invalid conversion choice. Please enter 'SVG' or 'ICO'.")
            continue
        
        run_again = messagebox.askyesno("Conversion Complete", f"{message}\n\nWould you like to run again?")
        
        if not run_again:
            break
    
    root.destroy()

if __name__ == "__main__":
    main()
