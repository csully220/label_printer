
from tkinter import Tk, W, E, filedialog, StringVar, LabelFrame, Listbox
from tkinter.ttk import Frame, Button, Entry, Style, Label
import os, stat, time
from BPL_utils import *


class CableLabelGUI(Frame): 
    def __init__(self): 
        super().__init__() 
        self.initUI()

    def initUI(self):

        self.dir_name = ""
        
        os.chdir(r"C:\Users\Csullivan\Documents\AutoCAD Publish")
        self.master.title("Cable Label Print Utility")
        Style().configure("TButton", padding=(3, 5, 3, 5), font='serif 10')

        self.columnconfigure(0, pad=3)
        self.rowconfigure(0, pad=3)
        
        grp = LabelFrame(self.master, text="Print to Brady printer from CSV or XML")
        grp.grid(row=0, column=0)
        grp.config(padx=50, pady=20)

        grp2 = LabelFrame(self.master, text="Print directly from XML")
        grp2.grid(row=1, column=0)
        grp2.config(padx=50, pady=20)

        self.lbls_csv = StringVar()
        self.lbls_csv.set(r".\sample.txt")

        self.lbls_xml = StringVar()
        self.lbls_xml.set(r".\sample.xml")

        # Choose file buttons
        btn_csv_file = Button(grp, text="Choose CSV File", command=self.choose_csv_file)
        btn_csv_file.grid(row=0, column=0)
        label_csv = Label(grp, textvariable = self.lbls_csv, width=40)
        label_csv.grid(row=0, column=1)
        
        btn_print_all = Button(grp, text="Print All", command=self.print_xml_files)
        btn_print_all.grid(row=1, column=0)
        #label_xml = Label(grp, textvariable = self.lbls_xml, width=40)
        #label_xml.grid(row=1, column=1)

        btn_xml_file = Button(grp2, text="Print XML File", command=self.print_xml_file)
        btn_xml_file.grid(row=0, column=0)

        self.lstbx_log = Listbox(grp, selectmode="extended")
        self.lstbx_log.grid(row=0, column=2)

        
    def choose_csv_file(self):
        filepath = filedialog.askopenfilename()
        fp_csv_sp = ntpath.split(filepath)
        filename = fp_csv_sp[1]
        self.dir_name = filename.split(".")
        self.dir_name = self.dir_name[0]
        self.lbls_csv.set(filename)
        #print(dir_name)
        if(not os.path.isdir(self.dir_name)):
            os.mkdir(self.dir_name)
        #print(filename)
        
        GenerateXMLinFives(self.dir_name, filename)
        self.lstbx_log.insert("end", "Saved to " + filepath)
        self.lstbx_log.insert("end", "Ready to print...")
        

    def print_xml_files(self):
        if(self.dir_name):
            files = os.listdir(self.dir_name)
            for f in files:
                SendToBP33(f, False)
                self.lstbx_log.insert("end", "Sent " + f + " to printer")
                time.sleep(7)
            self.lstbx_log.insert("end", "Done printing")

    def print_xml_file(self):
        filepath = filedialog.askopenfilename()
        SendToBP33(filepath, False)

def main():
    root = Tk() 
    #root.geometry("640x800")
    app = CableLabelGUI() 
    app.mainloop()

main()
