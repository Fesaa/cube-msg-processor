import tkinter as tk
from tkinter.messagebox import showwarning

from GUI.buttons import CustomBoolButton, CustomDateButton
from GUI.explorer import FileExplorer
from GUI.modals import Modal

class App(tk.Tk):

    def __init__(self, options) -> None:
        super().__init__()

        self.options = options

        # Main window setup
        self.title("Cube Msg Processor")
        self.geometry('530x500')
        self.protocol('WM_DELETE_WINDOW', self.on_window_close)
        self.configure(background='#C0C0C0')
    
        # Items, layout managed with grid
        # TO DO: Better layout manager, more dynamic and better colours

        intro_frame = tk.Frame(self)
        intro_frame.grid(row=0, column=0)

        label = tk.Label(intro_frame, background='#C0C0C0', fg='#4A68AB',
                        text='\nVery simply GUI implementation. \nSelect the options you want and press "OK" to continue.\n' \
                            'Closing the window will also start the processing!\n\nBegin with selecting the files you want to process.\nThis option is required!',
                            justify='left')
        label.grid(row=0, column=0)


        file = FileExplorer(self, text='Select your files', options=self.options)
        file.grid(row=1, column=0)

        label = tk.Label(self, background='#C0C0C0', fg='#4A68AB',
                        text="\nEnable or disable certain boolean options by clicking on the button.")
        label.grid(row=2, column=0)

        bool_buttons_frame = tk.Frame(self)
        bool_buttons_frame.grid(row=3, column=0, padx=10)

        r, c = 0, 0

        for i in [('Daily', False), ('ConsecutiveTime', True), ('TotalMessages', True), ('ReplyTimes', False), ('DailyMessages', False),
                 ('RoleDistribution', True), ('HourlyActivity', True), ('Percentages', False), ('UpdateJson', False),
                 ('ShowGraphs', False), ('Accurate', False), ('StaffHelp', False)]:

                button = CustomBoolButton(bool_buttons_frame, options=self.options, text=i[0], argument=i[0], selected=i[1], width=10, height=1)
                button.grid(row=r, column=c)
                r, c = r if c != 3 else r + 1, 0 if c == 3 else c + 1

        label = tk.Label(self, background='#C0C0C0', fg='#4A68AB',
                        text="\nSelect your Start and End date below! These are optional.")
        label.grid(row=4, column=0)

        date_buttons_frame = tk.Frame(self, background='#C0C0C0')
        date_buttons_frame.grid(row=5, column=0)

        r, c = 7, 1

        for i in ['StartDate', 'EndDate']:
           button = CustomDateButton(date_buttons_frame, self.options, i, text=i)
           button.grid(row=r, column=c)
           c += 1
        
        label = tk.Label(self, background='#C0C0C0', fg='#4A68AB',
                        text="\nInput the number based options below! These are also opional.")
        label.grid(row=6, column=0)

        modal_buttons_frame = tk.Frame(self, background='#C0C0C0')
        modal_buttons_frame.grid(row=7, column=0)


        for i in ['IgnoreMessages', 'MinMsg', 'MinTime']:
            modal = Modal(modal_buttons_frame, self.options, i)
            modal.grid(row=r, column=c)
            r += 1

        confirmation_button = tk.Button(self, highlightbackground='#C0C0C0', width=10, height=1, text="CONFIRM", command=self.on_window_close)
        confirmation_button.grid(row=8, column=0)
        
    def on_window_close(self):
        if self.options['FileName'] is not None:
            self.destroy()
        else:
            showwarning(title='Missing required option', message='Missing required option')

    def get_options(self):
        return self.options
        