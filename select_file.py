import tkinter as tk
from tkinter import filedialog as fd

def select_file() -> str:
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-alpha",0)
    filetypes = (('MS-Excel Files',('*.xlsx','*.xls')), ('All Files','*.*'))
    filename = fd.askopenfile(
        title = 'Select the spreadsheet with treaty metadata',
        initialdir = '/',
        filetypes = filetypes
    )
    return filename.name



