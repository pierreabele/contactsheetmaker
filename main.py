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

### parameters -- change things here if you know what you're doing

main_res = (3543, 2362) # resolution of 30cm x 20cm photographic paper at 300 DPI
lat_res = 426 # 24mm x 36mm negative at 300 DPI is roughly 426 pixels of lateral resolution
shape = [7, 6]
spacing_x = 30
spacing_y = 75
verbose = False
default_outname = "contactsheet"

offset_x = (main_res[0] - shape[0] * (lat_res) - (shape[0] - 1) * spacing_x)//2
offset_y = (main_res[1] - shape[1] * (2 * lat_res // 3) - (shape[1] - 1) * spacing_y)//2

def getpath():
    path = askdirectory(title='Select Folder')  # shows dialog box and return the path
    path = path + "/"
    pathtext.set(path)


def make_contactsheet(path):
    filenames = [f for f in sorted(listdir(path)) if isfile(join(path, f))]

    def rotate_crop_resize(img, lr=lat_res):
        x, y = img.size
        if y > x:
            img2 = img.transpose(method=Image.Transpose.ROTATE_90)
            x, y = img2.size
        else:
            img2 = img
        if x / y == 1.5:
            img3 = img2
        else:
            if x / y < 1.5:
                img3 = img2.crop(box=(0, 0, (x // 3) * 3, (x // 3) * 2))
            else:
                img3 = img2.crop(box=(0, 0, (y // 2) * 3, (y // 2) * 2))
        img4 = img3.resize((lr, 2 * lr // 3))
        return img4

    canvas = Image.new("RGB", main_res, (0, 0, 0))
    fonta = ImageFont.truetype("cour.ttf", 40)
    fontb = ImageFont.truetype("cour.ttf", 40)
    draw = ImageDraw.Draw(canvas)

    assert len(filenames) < shape[0] * shape[1]
    pos_list = [
        (offset_x + (i % shape[0]) * (lat_res + spacing_x), offset_y + i // shape[0] * (2 * lat_res // 3 + spacing_y))
        for i in range(shape[0] * shape[1])]

    count = 0

    for filename in filenames:
        raw_image = Image.open(path + filename)
        image = rotate_crop_resize(raw_image)
        if verbose:
            print("Found Image", filename, "with size", raw_image.size, "rotated, cropped and resized to", image.size)
        pos = pos_list[count]
        draw.text((pos[0] + spacing_x // 2, pos[1] + 2 * lat_res // 3 + spacing_y // 6), text=str(count), fill='white',
                  font=fontb)
        canvas.paste(image, box=pos)
        count += 1

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")
    day = now.strftime("%d")

    text = (photographer.get() + " | " + camera.get() + " | " + film_stock.get() + " | " + note.get() + " | " +
            "digital contact sheet made on " + month + " " + day + ", " + year)

    draw.text((offset_x, 45), text=text, fill='white', font=fonta)

    if default_outname + ".jpg" in filenames:
        print("There already exists a contact sheet.")
        outname = default_outname
    else:
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        outname = default_outname + dt_string

    canvas.show()
    canvas.save(path + outname + ".jpg", format='JPEG', subsampling=0, quality=100)

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

mainButton = ttk.Button(root, text="Make a Contact Sheet!", command=(lambda: make_contactsheet(pathtext.get())))
mainButton.pack()

root.mainloop()
