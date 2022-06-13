from GUI.calender import CalenderWindow
from GUI.baseclasses import CustomButton

class CustomBoolButton(CustomButton):

    def __init__(self, master, options, argument, selected: bool = False,  *args, **kwargs):
        super().__init__(master, options, *args, **kwargs)
        
        self.argument = argument
        self.selected = selected

        self.configure(fg='green' if self.selected else 'red')

        self['command'] = self.callback
    
    def callback(self):
        self.selected = not self.selected
        self.options[self.argument] = self.selected
        self.configure(fg='green' if self.selected else 'red')

class CustomDateButton(CustomButton):

    def __init__(self, master, options, argument, *args, **kwargs):
        super().__init__(master, options, *args, **kwargs)

        self.argument = argument

        self['command'] = self.callback
    
    def callback(self):
        w = CalenderWindow(self.master, self.options, self.argument)