from PIL import Image, ImageFont, ImageDraw, ImageOps
from os import listdir
from os.path import isfile, join
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory

root = tk.Tk()
root.title("Contact Sheet Maker")

window_width = 800
window_height = 600

def getpath():
    path = askdirectory(title='Select Folder')  # shows dialog box and return the path
    path = path + "/"
    pathtext.set(path)

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.iconbitmap('./csmicon2.ico')

pathtext=tk.StringVar()
photographer = tk.StringVar()
camera = tk.StringVar()
film_stock = tk.StringVar()
note = tk.StringVar()

pathButton = ttk.Button(root, text="Select Folder", command=getpath)
pathButton.pack()
pathLabel = ttk.Label(root, textvariable=pathtext)
pathLabel.pack()

photographer_label = ttk.Label(root, text="Name of the photographer:")
photographer_label.pack(fill='x', expand=True)
photographer_entry = ttk.Entry(root, textvariable=photographer)
photographer_entry.pack(fill='x', expand=True)

camera_label = ttk.Label(root, text="Name of the camera model:")
camera_label.pack(fill='x', expand=True)
camera_entry = ttk.Entry(root, textvariable=camera)
camera_entry.pack(fill='x', expand=True)

film_stock_label = ttk.Label(root, text="Film stock:")
film_stock_label.pack(fill='x', expand=True)
film_stock_entry = ttk.Entry(root, textvariable=film_stock)
film_stock_entry.pack(fill='x', expand=True)

note_label = ttk.Label(root, text="Add a note, like time and place:")
note_label.pack(fill='x', expand=True)
note_entry = ttk.Entry(root, textvariable=note)
note_entry.pack(fill='x', expand=True)

root.mainloop()



# path = askdirectory(title='Select Folder') # shows dialog box and returns the path
# path = path + "/"
# print(path)