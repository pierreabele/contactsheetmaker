# ContactSheetMaker
Makes digital contact sheets from JPG files.

ContactSheetMaker currently supports the following film formats:

- 35mm / 135 format
- 6x4.5
- 6x6
- 6x7

It generates an output file with dimensions 3543 by 2362, which represents a sheet of 20cm x 30cm photographic paper at 300 DPI.
## Installation
### Windows
A Windows executable is provided with ``dist/ContactSheetMaker.exe``.

### Building from source
If you want to build the program yourself, you will need a Python installation, in which the following modules have to be installed:
- pillow
- tkinter
- sv_ttk ([Sun Valley Theme for tkinter](https://github.com/rdbende/Sun-Valley-ttk-theme) by rdbende)

as well as ``pyinstaller``. Then run the following command within the project directory:

```
pyinstaller main.pyw --onefile --collect-data sv_ttk --icon csmicon4.ico --name ContactSheetMaker
```
