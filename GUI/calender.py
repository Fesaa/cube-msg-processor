import tkinter as tk
import tkcalendar as tkc
from tkinter.messagebox import showerror

from GUI.baseclasses import CustomButton

class CalenderWindow(tk.Toplevel):

    def __init__(self, master, options, argument, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.geometry('400x400')
        self.title('Select your date')
        self.configure(background='#C0C0C0')

        self.options = options
        self.argument = argument

        frame_one = tk.Frame(self)
        frame_one.pack(pady=30)


        self.cal = tkc.Calendar(frame_one, selectmode="day", showweeknumbers=False, date_patern='yyyy-mm-dd',
                                normalforeground='#003366', selectforeground='red', weekendforeground='#002851',
                                foreground='#004c26', )
        self.cal.pack(pady=20)

        CustomButton(self, self.options, text='Choose this date', bg='#C0C0C0', command=self.callback).pack(pady=20)
    
    def on_window_close(self):
        self.destroy()
    
    def callback(self):
        date = self.cal.get_date().split('/')
        date = f'20{date[2] if int(date[2]) > 9 else f"0{date[2]}"}-{date[0] if int(date[0]) > 9 else f"0{date[0]}"}-{date[1] if int(date[1]) > 9 else f"0{date[1]}"}'
        if (self.argument == 'StartDate' and date < ( '9999-99-99' if self.options['EndDate'] == 'End Date' else self.options['EndDate'])) or \
            (self.argument == 'EndDate' and date > ( '0000-00-00' if self.options['StartDate'] == 'First Date' else self.options['StartDate'])):
            self.options[self.argument] = date
            self.destroy()
        elif self.argument == 'StartDate':
            showerror(title='Invalid date', message="Your start date must be before your end date!")
        elif self.argument == 'EndDate':
            showerror(title='Invalid date', message="Your end date must be before your start date!")




