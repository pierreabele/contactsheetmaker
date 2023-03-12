from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageTk
from os import listdir
from os.path import isfile, join
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
import sv_ttk

root = tk.Tk()
root.title("Contact Sheet Maker")
sv_ttk.set_theme("dark")

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

### parameters -- change things here if you know what you're doing

film_formats = ("35mm", "6x4.5", "6x6", "6x7")
format_sizes = {"35mm": (360, 240), "6x6": (560, 560), "6x4.5": (415, 560), "6x7": (690, 560)} # in tenths of millimeters

main_res = (3543, 2362) # resolution of 30cm x 20cm photographic paper at 300 DPI
preview_res = (900,600)

spacing_x = 30
spacing_y = 75
verbose = False
default_outname = "contactsheet"

def getpath():
    path = askdirectory(title='Select Folder')  # shows dialog box and return the path
    if path.endswith("/"):
        pass
    else:
        path = path + "/"
    pathtext.set(path)


def make_contactsheet(path, fformat="35mm", preview=False):

    filenames = [f for f in sorted(listdir(path)) if isfile(join(path, f))]

    a = format_sizes[fformat][0]
    b = format_sizes[fformat][1]

    fformat_ratio = a / b

    lat_res = round(a * main_res[0] / 3000)

    if fformat=="35mm":
        shape = [7, 6]
    elif fformat=="6x4.5":
        shape = [6, 3]
    elif fformat == "6x7":
        shape = [4, 3]
    else:
        shape = [4, 3]


    offset_x = (main_res[0] - shape[0] * lat_res - (shape[0] - 1) * spacing_x) // 2
    offset_y = (main_res[1] - shape[1] * (b * lat_res // a) - (shape[1] - 1) * spacing_y) // 2

    def rotate_crop_resize(img, lr=lat_res):

        x, y = img.size

        if fformat_ratio==1.0:
            if y==x:
                img4 = img.resize((lr, lr))
            else:
                img4 = img.crop(box=(0, 0, min((x, y)), min((x, y)))).resize((lr, lr))
        else:
            if y > x:
                img2 = img.transpose(method=Image.Transpose.ROTATE_90)
                x, y = img2.size
            else:
                img2 = img
            if x / y == fformat_ratio:
                img3 = img2
            else:
                if x / y < fformat_ratio:
                    img3 = img2.crop(box=(0, 0, (x // a) * a, (x // a) * b))
                else:
                    img3 = img2.crop(box=(0, 0, (y // b) * a, (y // b) * b))
            img4 = img3.resize((lr, b * lr // a))

        return img4

    canvas = Image.new("RGB", main_res, (0, 0, 0))
    fonta = ImageFont.truetype("cour.ttf", 40)
    fontb = ImageFont.truetype("cour.ttf", 40)
    draw = ImageDraw.Draw(canvas)

    pos_list = [
        (offset_x + (i % shape[0]) * (lat_res + spacing_x), offset_y + i // shape[0] * (b * lat_res // a + spacing_y))
        for i in range(shape[0] * shape[1])]

    count = 0

    for filename in filenames:

        if filename.endswith(".jpg") or filename.endswith(".JPG"):
            pass
        else:
            print("Found file", filename, ", which is not a JPEG file.")
            continue

        if default_outname in filename:
            continue

        raw_image = Image.open(path + filename)
        image = rotate_crop_resize(raw_image)
        if verbose:
            print("Found Image", filename, "with size", raw_image.size, "rotated, cropped and resized to", image.size)
        pos = pos_list[count]
        draw.text((pos[0] + spacing_x // 2, pos[1] + b * lat_res // a + spacing_y // 6), text=str(count), fill='white',
                  font=fontb)
        canvas.paste(image, box=pos)
        count += 1
        assert count <= shape[0] * shape[1]

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")
    day = now.strftime("%d")

    text = (photographer.get() + " | " + camera.get() + " | " + film_stock.get() + " | " + note.get() + " | " +
            "digital contact sheet made on " + month + " " + day + ", " + year)

    draw.text((offset_x, 45), text=text, fill='white', font=fonta)

    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    outname = default_outname + dt_string

    if not preview:
        canvas.save(path + outname + ".jpg", format='JPEG', subsampling=0, quality=100)
        return 0
    else:
        return canvas


def make_preview(path, fformat="35mm"):
    global preview_photoimg
    preview_img = make_contactsheet(path, fformat, preview=True).resize(preview_res, Image.Resampling.LANCZOS)
    preview_photoimg = ImageTk.PhotoImage(preview_img)
    preview_canvas_label.configure(image=preview_photoimg)

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 1 * screen_width // 2
window_height = 4 * screen_height // 5

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(True, True)

pathtext=tk.StringVar()
photographer = tk.StringVar()
camera = tk.StringVar()
film_stock = tk.StringVar()
note = tk.StringVar()

film_format = tk.StringVar()

ipadding = {'ipadx': 0, 'ipady': 0}
padding = {'padx': 6, 'pady': 2}

pathButton = ttk.Button(root, text="Select Folder", command=getpath)
pathButton.grid(**padding, **ipadding, row=0, column=0)
pathLabel = ttk.Label(root, textvariable=pathtext)
pathLabel.grid(**padding, **ipadding, row=0, column=1)

format_dropdown_label = ttk.Label(root, text="Choose film format:")
format_dropdown_label.grid(**padding, **ipadding, row=0, column=2)
format_dropdown = ttk.OptionMenu(root, film_format, film_formats[0], *film_formats)
format_dropdown.grid(**padding, **ipadding, row=0, column=3, sticky='we')

photographer_label = ttk.Label(root, text="Name of the photographer:")
photographer_label.grid(**padding, **ipadding, row=1, column=0)
photographer_entry = ttk.Entry(root, textvariable=photographer)
photographer_entry.grid(**padding, **ipadding, row=1, column=1, columnspan=3, sticky='we')

camera_label = ttk.Label(root, text="Name of the camera model:")
camera_label.grid(**padding, **ipadding, row=2, column=0)
camera_entry = ttk.Entry(root, textvariable=camera)
camera_entry.grid(**padding, **ipadding, row=2, column=1, columnspan=3, sticky='we')

film_stock_label = ttk.Label(root, text="Film stock:")
film_stock_label.grid(**padding, **ipadding, row=3, column=0)
film_stock_entry = ttk.Entry(root, textvariable=film_stock)
film_stock_entry.grid(**padding, **ipadding, row=3, column=1, columnspan=3, sticky='we')

note_label = ttk.Label(root, text="Add a note, like time and place:")
note_label.grid(**padding, **ipadding, row=4, column=0)
note_entry = ttk.Entry(root, textvariable=note)
note_entry.grid(**padding, **ipadding, row=4, column=1, columnspan=3, sticky='we')

previewButton = ttk.Button(root, text="Preview", command=(lambda: make_preview(pathtext.get(), fformat=film_format.get())))
previewButton.grid(**padding, **ipadding, row=5, column=0, columnspan=4, sticky='we')

mainButton = ttk.Button(root, text="Save", command=(lambda: make_contactsheet(pathtext.get(), fformat=film_format.get())))
mainButton.grid(**padding, **ipadding, row=7, column=0, columnspan=4, sticky='we')

preview_canvas = ImageTk.PhotoImage(Image.new("RGB", preview_res, (0, 0, 0)))
preview_canvas_label = ttk.Label(root, image=preview_canvas)
preview_canvas_label.grid(**padding, **ipadding, row=6, column=0, columnspan=4)

root.mainloop()