import win32print
import tkinter as tk
from tkinter import filedialog
import ntpath
import os

root = tk.Tk()
root.withdraw()

xml_opening = '<?xml version="1.0"?>\n<bpl-document>\n'
xml_defaults = '    <defaults>\n        <document units="inches" />\n        <printer tear-or-cut-between="after-job" />\n    </defaults>\n'
xml_labels = '    <labels>\n'
xml_label = '        <label copies="1" width="2" height="3.75" offset-x="0.094" offset-y="-0.19" orientation="portrait" >\n'

# Get the filename containing label information.
#fn_csv = input('Enter filename: ')
#fn_csv = 'A02055_A.txt'
print("Select the CSV file exported from AutoCAD containing label information...")
fp_csv = filedialog.askopenfilename()
fp_csv_sp = ntpath.split(fp_csv)
fn_csv = fp_csv_sp[1]
os.chdir(fp_csv_sp[0])

# Create a BPL file for writing to
fn_bpl = fn_csv.split('.')
fn_bpl = fn_bpl[0] + '.xml'

f_bpl = open(fn_bpl, "w")

# BPL Document opening tags
f_bpl.write(xml_opening)
f_bpl.write(xml_defaults)

# Open the CSV file and parse labels
num_lines = sum(1 for line in open(fn_csv))
print(str(int(num_lines/3)) + ' labels found for printing.')
f_csv = open(fn_csv, "r")

# Start labels
f_bpl.write(xml_labels)

for i in range(num_lines):

    # Start label
    f_bpl.write(xml_label)
    label = f_csv.readline()
    lines = label.split(',')

    # Write text tag for each of the three lines
    txt_height = ['1.8', '2.06', '2.32']
    for i in range(len(lines)):
        line = lines[i].strip().strip("'")
        f_bpl.write('            <text position-x="0" position-y="0" align="center" bold="true" font-name="Courier New" >\n')
        f_bpl.write('                <text-sizing>\n                    <manual height="' + txt_height[i] + '" width="2" font-size="9" />\n                </text-sizing>\n')
        f_bpl.write('                <datasource>\n                    <static-text value="' + line + '" />\n                </datasource>\n')
        f_bpl.write('            </text>\n')

    # Close the label tag
    f_bpl.write('        </label>\n')

# Close labels and document tags
f_bpl.write('    </labels>\n')
f_bpl.write('</bpl-document>')

f_bpl.close()

print('Generated ' + fn_bpl + '.')

printers = win32print.EnumPrinters(2)
for p in printers:
    if p[3] == 'BBP33':
        printer_name = p[2]
        print('Found printer ' + printer_name)

if (printer_name):
    cont = input('Use ' + printer_name + ' to print labels? [y/n]\n')
    if (cont == 'y'):
        f_bpl = open(fn_bpl, "rb")
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
    else:
        print('Aborted')
