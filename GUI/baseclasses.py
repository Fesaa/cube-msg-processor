import tkinter as tk

class CustomButton(tk.Button):

    def __init__(self, master, options, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        self.master = master
        self.options = options
        self.configure(highlightbackground='#C0C0C0')