
from tkinter import *
from tkinter import filedialog, messagebox
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.title("Image watermark generator")
window.config(padx=50, pady=50)


def select_image():
    filetypes = (
        ('Image files', ['*.png', '*.jpg']),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Select image',
        initialdir='/',
        filetypes=filetypes)

    # messagebox.showinfo(
    #     title='Selected image',
    #     message=filename
    # )
    if entry_directory.get() != "":
        entry_directory.delete(0, "end")
    entry_directory.insert(END, filename)


def generate():
    pass


label_browse = customtkinter.CTkLabel(window, text="Browse for image:")
label_browse.grid(column=1, row=1)
entry_directory = customtkinter.CTkEntry(window, width=300, height=3)
entry_directory.grid(column=1, row=2)
button_browse = customtkinter.CTkButton(window, text="Browse...", command=select_image, width=20, height=5)
button_browse.grid(column=2, row=2)

label_watermark = customtkinter.CTkLabel(window, text="Provide text for watermark:")
label_watermark.grid(column=1, row=3)
entry_watermark = customtkinter.CTkEntry(window, width=200, height=3)
entry_watermark.grid(column=1, row=4)

button_generate = customtkinter.CTkButton(window, text="Generate", width=20, height=5, command=generate)
button_generate.grid(column=2, row=5)
button_exit = customtkinter.CTkButton(window, text="Exit", width=20, height=5, command=window.destroy)
button_exit.grid(column=3, row=5)

window.mainloop()
