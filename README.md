# ContactSheetMaker
Makes digital contact sheets from JPG files.

ContactSheetMaker currently supports the following film formats:

- 35mm / 135 format
- 6x4.5
- 6x6
- 6x7

It generates an output file with dimensions 3543 by 2362, which represents a sheet of 20cm x 30cm photographic paper at 300 DPI.

## Installation

You need a Python installation, in which the following Python packages have to be installed:

- ``pillow``
- ``tkinter``
- ``sv_ttk`` ([Sun Valley Theme for tkinter](https://github.com/rdbende/Sun-Valley-ttk-theme) by rdbende)
- ``pyinstaller`` (optional)

Then run the following command within the project directory:

Windows:
```
python .\src\main.pyw
```

Linux/MacOS (not tested):
```
python3 ./src/main.pyw
```

Or, if you want to produce a standalone binary, run 

```
python -m PyInstaller ./src/main.pyw --onefile --collect-data sv_ttk --icon ./ico/csmicon4.ico --name ContactSheetMaker
```
