import win32print
import tkinter as tk
from tkinter import filedialog
import ntpath

root = tk.Tk()
root.withdraw()

fn_bpl = filedialog.askopenfilename()

#fn_bpl = 'test4.xml'
f_bpl = open(fn_bpl, "rb")
printers = win32print.EnumPrinters(2)
for p in printers:
    if p[3] == 'BBP33':
        printer_name = p[2]
        print('Found ' + printer_name)
if (printer_name):
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
      hJob = win32print.StartDocPrinter (hPrinter, 1, ("Cable labels", None, "RAW"))
      try:
        win32print.StartPagePrinter (hPrinter)
        win32print.WritePrinter (hPrinter, f_bpl.read())
        win32print.EndPagePrinter (hPrinter)
      finally:
        win32print.EndDocPrinter (hPrinter)
    finally:
      win32print.ClosePrinter (hPrinter)
f_bpl.close()
