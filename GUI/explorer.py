import os
from tkinter import filedialog

from GUI.buttons import CustomButton

class FileExplorer(CustomButton):

    def __init__(self, master, options, *args, **kwargs):
        super().__init__(master, options, *args, **kwargs)

        self['command'] = self.callback

    
    def callback(self):
        filenames = filedialog.askopenfilenames(initialdir = os.path.abspath(__file__).removesuffix('GUI/explorer.py') + 'processor/',
                                          title = "Select files to use the processor on",
                                          filetypes = (("csv file","*.csv"),("all files","*.*")))
                                
        filenames = [i.removeprefix(os.path.abspath(__file__).removesuffix('GUI/explorer.py') + 'processor/') for i in filenames]

        if self.options['FileName'] is None:
            self.options['FileName'] = filenames
        else:
            self.options['FileName'].append(filenames)

