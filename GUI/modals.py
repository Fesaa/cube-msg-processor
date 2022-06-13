import tkinter as tk
from tkinter.messagebox import showerror

from GUI.baseclasses import CustomButton

class Modal(tk.Frame):

    def __init__(self, master, options, argument, *args, **kwargs):
        super().__init__(master, background='#C0C0C0', *args, **kwargs)

        self.options = options
        self.argument = argument

        self.TextInput = tk.Entry(self, highlightbackground='#C0C0C0', background='white', foreground='black')
        confirm_button = CustomButton(self, self.options, command=self.callback, text=self.argument, background='#C0C0C0', width=10, height=1)
        self.TextInput.grid(column=0, row=0)
        confirm_button.grid(column=1, row=0)

    def callback(self):
        input = self.TextInput.get()

        try:
            argument = float(input)
        except ValueError:
            showerror("Invalid entry", message="Your input must be a number!")
            return 
        
        self.options[self.argument] = argument
