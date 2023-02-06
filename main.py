from tkinter import *
from tkinter import filedialog, messagebox
import customtkinter
from PIL import Image, ImageDraw, ImageFont
import os
from tkinter.colorchooser import askcolor
from pathlib import Path

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.title("Image watermark generator")
window.geometry("470x320")
window.resizable(False, False)


def select_folder():
    """Selects folder's path."""
    folder_directory = filedialog.askdirectory()
    if entry_saving_directory.get() != "":
        entry_saving_directory.delete(0, "end")
    entry_saving_directory.insert(END, folder_directory)


def select_image():
    """Selects image's path."""
    filetypes = (
        ("Image files", ["*.png", "*.jpg"]),
        ("All files", "*.*")
    )
    filename = filedialog.askopenfilename(title="Select image", initialdir="/", filetypes=filetypes)

    if entry_image_path.get() != "":
        entry_image_path.delete(0, "end")
    entry_image_path.insert(END, filename)


def popup_window(image):
    """Shows pop-up window with file name input."""

    def save(image):
        """Saves image to the specified destination."""
        image_extension = entry_image_path.get()[-3:]
        saving_directory = entry_saving_directory.get()
        filename = entry_filename.get()
        path = Path(f"{saving_directory}/{filename}.{image_extension}")
        if entry_filename.get() == "":
            messagebox.showinfo(title="Empty file name", message="Please provide file name.")
        else:
            if path.is_file():
                msg_box = messagebox.askquestion("File already exists",
                                                 "This file name already exists at that location. "
                                                 "Would you like to replace it?",
                                                 icon="warning")
                if msg_box == "no":
                    filename_window.grab_release()
                    filename_window.destroy()
                    popup_window(image)
                    return
            try:
                image.save(f"{saving_directory}/{filename}.{image_extension}")
                image.show()
                filename_window.grab_release()
                filename_window.destroy()
            except (ValueError, OSError):
                messagebox.showerror("Invalid File Name", "Sorry, you've provided unsupported characters in your "
                                                          "file name. Please try again.")

    filename_window = customtkinter.CTkToplevel(window)
    filename_window.grab_set()
    filename_window.geometry("250x170")
    filename_window.title("Save As...")
    filename_window.resizable(False, False)

    frame_toplevel = customtkinter.CTkFrame(master=filename_window)
    frame_toplevel.pack(pady=40, padx=40, fill="both")

    entry_filename = customtkinter.CTkEntry(frame_toplevel, width=150, height=3, placeholder_text="File Name")
    entry_filename.pack(pady=10, padx=12)

    button_save = customtkinter.CTkButton(frame_toplevel, text="Save", command=lambda: save(image),
                                          width=80, height=20)
    button_save.pack(pady=(0, 10), padx=12, side=TOP)


def generate():
    """Generates image with specified watermark text."""
    image_path = entry_image_path.get()
    image_extension = image_path[-3:]
    saving_directory = entry_saving_directory.get()
    watermark_text = entry_watermark.get()

    if not os.path.exists(image_path):
        messagebox.showinfo(
            title="Error",
            message="Sorry, this image path doesn't exist."
        )
    elif image_extension != "jpg" and image_extension != "png":
        messagebox.showinfo(
            title="Error",
            message="Sorry, this file extension is not supported. Try '.jpg' or '.png.'"
        )
    elif not os.path.isdir(saving_directory):
        messagebox.showinfo(
            title="Error",
            message="Sorry, this saving directory doesn't exist."
        )
    elif watermark_text == "":
        messagebox.showinfo(
            title="Error",
            message="Please provide text for watermark."
        )
    else:
        image = Image.open(entry_image_path.get())
        image_width, image_height = image.size

        draw = ImageDraw.Draw(image)
        watermark_text = entry_watermark.get()

        font = ImageFont.truetype("arial.ttf", 36)
        text_dimensions = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_dimensions[-2]
        text_height = text_dimensions[-1]

        margin = 10
        text_x = image_width - text_width - margin
        text_y = image_height - text_height - margin

        messagebox.showinfo(title="Watermark Color", message="Please choose watermark color.")

        colors = askcolor(title="Watermark Color Picker")
        draw.text((text_x, text_y), watermark_text, font=font, fill=colors[1])

        popup_window(image)


frame = customtkinter.CTkFrame(master=window)
frame.grid(column=0, row=0, pady=60, padx=60)

label_title = customtkinter.CTkLabel(frame, text="Watermark Generator", font=("Roboto", 24))
label_title.grid(column=0, row=0, pady=12, padx=10, columnspan=2)

entry_image_path = customtkinter.CTkEntry(frame, width=300, height=3, placeholder_text="Image path")
entry_image_path.grid(column=0, row=1, padx=(10, 0))
button_browse_img = customtkinter.CTkButton(frame, text="...", command=select_image, width=20, height=5)
button_browse_img.grid(column=1, row=1, padx=8)

entry_saving_directory = customtkinter.CTkEntry(frame, width=300, height=3, placeholder_text="Saving directory")
entry_saving_directory.grid(column=0, row=2, padx=(10, 0), pady=(12, 0))
button_browse_folder = customtkinter.CTkButton(frame, text="...", command=select_folder, width=20, height=5)
button_browse_folder.grid(column=1, row=2, padx=8, pady=(12, 0))

entry_watermark = customtkinter.CTkEntry(frame, width=150, height=3, placeholder_text="Watermark text")
entry_watermark.grid(column=0, row=3, pady=12, padx=10, columnspan=2)

button_generate = customtkinter.CTkButton(frame, text="Generate", width=80, height=20, command=generate)
button_generate.grid(column=0, row=4, pady=(0, 12), columnspan=2)

window.mainloop()
