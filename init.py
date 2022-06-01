from os.path import exists
from colorama import Fore, Style
from typing import Union
import sys, re


ALLOWED_ARGUMENTS = {'Daily': {'type': 'options', 'options': ['True', 'False']},
                    'ConsecutiveTime': {'type': 'options', 'options': ['True', 'False']},
                    'TotalMessages': {'type': 'options', 'options': ['True', 'False']},
                    'SaveGraphs': {'type': 'options', 'options': ['True', 'False']},
                    'ShowExplanation': {'type': 'options', 'options': ['True', 'False']},
                    'ShowGraphs': {'type': 'options', 'options': ['True', 'False']},
                    'ReplyTimes': {'type': 'options', 'options': ['True', 'False']},
                    'IgnoreMessages': {'type': 'options', 'options': [str(i) for i in range(10)]},
                    'DailyStaffMessages': {'type': 'options', 'options': ['True', 'False']},
                    'StartDate': {'type': 'Regex Check', 'Regex String': r'^\d{4}[\-\/\s]?((((0[13578])|(1[02]))[\-\/\s]?(([0-2][0-9])|(3[01])))|(((0[469])|(11))[\-\/\s]?(([0-2][0-9])|(30)))|(02[\-\/\s]?[0-2][0-9]))$', 'Example': '2022-02-12'}
                    }

DEFAULT_ARGUMENTS = {'Daily': True,
                     'ConsecutiveTime': False,
                     'TotalMessages': True,
                     'SaveGraphs': False,
                     'ShowExplanation': True,
                     'ShowGraphs': True,
                     'ReplyTimes': False,
                     'IgnoreMessages': 2,
                     'DailyStaffMessages': False,
                     'StartDate': 'First Date'
                    }

ARGUMENT_EXPLAIN = {'Daily': f'{Fore.CYAN}Daily{Style.RESET_ALL}: Adds a graphs to your figure with the total amount of messages per day.\nMinimum of {Fore.MAGENTA}10{Style.RESET_ALL} messages are needed to be displayed on the graph.\nDefaults to{Fore.GREEN} True {Style.RESET_ALL}',
                    'ConsecutiveTime': f'{Fore.CYAN}ConsecutiveTime{Style.RESET_ALL}: Adds a graph to your figure with the total time spend by ' \
                                       f'a staff member in staff help. \nTime is added to the total if more than 5 messages have been send without ' \
                                       f'5 messages by an other staff member between two messages.\nMinimum of {Fore.MAGENTA}30min {Style.RESET_ALL} is needed to be displayed on the graph.\nDefaults to{Fore.RED} False {Style.RESET_ALL}',
                    'TotalMessages': f'{Fore.CYAN}TotalMessages{Style.RESET_ALL}: Adds a graph to your figure with the total messages send in staff help per staff member. \nDefaults to{Fore.GREEN} True {Style.RESET_ALL}',
                    'SaveGraphs': f"{Fore.CYAN}SaveGraphs{Style.RESET_ALL}: Save your figure to a .png in your cwd. \nDefaults to{Fore.RED} False {Style.RESET_ALL}",
                    'ShowExplanation': f"{Fore.CYAN}ShowExplanation{Style.RESET_ALL}: Shows an explanation about your chosen options. \nDefaults to{Fore.GREEN} True {Style.RESET_ALL}",
                    'ShowGraphs': f'{Fore.CYAN}ShowGraph{Style.RESET_ALL}: Shows your graph after making it.\nDefaults to{Fore.GREEN} True {Style.RESET_ALL} ',
                    'ReplyTimes': f'{Fore.CYAN}ReplyTimes{Style.RESET_ALL}: Adds a graphs to your figure with the average waiting time per time slots of one hour.\nDefaults to{Fore.RED} False {Style.RESET_ALL}',
                    'IgnoreMessages': f'{Fore.CYAN}IgnoreMessages{Style.RESET_ALL}: amount of non staff messages have to be send before we start counting wait time. This to take thank you messages into account.\nDefaults to{Fore.GREEN} 2 {Style.RESET_ALL} ',
                    'DailyStaffMessages': f'{Fore.CYAN}DailyStaffMessages{Style.RESET_ALL}: Adds a graphs to your figure with the average amount of messages per day in the recorded period.\nDefaults to{Fore.RED} False {Style.RESET_ALL} ',
                    'StartDate': f'{Fore.CYAN}StartDate{Style.RESET_ALL}: Force a date to start registering data from. A data later than the last recorded day will just return no information.\nDefaults to{Fore.MAGENTA} Defaults to first date in data. {Style.RESET_ALL}'
                    }

class InvalidArgument(Exception):

    def __init__(self, argument, *args):
        super().__init__(args)
        self.argument = argument

    def __str__(self):
        return f'{self.argument} is not a valid option. A list of valid options is:\n{" -- ".join(ALLOWED_ARGUMENTS.keys())}'

class InvalidLayout(Exception):

    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return f'Arguments should be off the form "TotalMessages=True".'

class InvalidOption(Exception):

    def __init__(self, argument, *args):
        super().__init__(args)
        self.argument = argument
    
    def __str__(self):
        if ALLOWED_ARGUMENTS[self.argument]["type"] == "options":
            return f'The allowed options for {self.argument} are: \n{", ".join(ALLOWED_ARGUMENTS[self.argument]["options"])}'
        elif ALLOWED_ARGUMENTS[self.argument]["type"] == "Regex Check":
            return f'Your argument for {self.argument} must match the following Regex String. An example is given below\n' \
                   f'{ALLOWED_ARGUMENTS[self.argument]["Regex String"]}\nExample: {ALLOWED_ARGUMENTS[self.argument]["Example"]}'
        else:
            return ""

class CustomFileError(Exception):
    def __init__(self, error, *args):
        super().__init__(args)
        self.error = error
    
    def __str__(self):
        return self.error


def arg_check(argument: str) -> bool:
    try:
        argument.split('=')[1]
    except IndexError:
        raise InvalidLayout
    else:
        arg_type, arg_option = argument.split('=')[0], argument.split('=')[1]
        if  arg_type in ALLOWED_ARGUMENTS.keys():
            if ALLOWED_ARGUMENTS[arg_type]['type'] == 'options':
                if arg_option in ALLOWED_ARGUMENTS[arg_type]['options']:
                    return True
            elif ALLOWED_ARGUMENTS[arg_type]['type'] == 'Regex Check':
                if re.match(ALLOWED_ARGUMENTS[arg_type]['Regex String'], arg_option):
                    return True
            raise InvalidOption(arg_type)
        else:
            raise InvalidArgument(arg_type)

def arg_correction(argument: str) -> Union[str, bool, int]:
    if argument == 'True':
        return True
    elif argument == 'False':
        return False
    elif argument.isdigit():
        return int(argument)
    else:
        return argument

def on_start() -> Union[dict, str]:

    try:
        if sys.argv[1].split('=')[0] == "FileName":
            FileNames = sys.argv[1].split('=')[1].split(',')
        else:
            raise IndexError
    except IndexError:
        raise CustomFileError("Your first argument must be the filename:\nFileName=myFile.csv")
    else:
        if all(exists(FileName) for FileName in FileNames):
            args = {i.split('=')[0]: arg_correction(i.split('=')[1]) for i in sys.argv[2::] if arg_check(i)}
        else:
            raise CustomFileError('Please provide a valid FileName! Or you in the cwd?')
    
    for argument in ALLOWED_ARGUMENTS.keys():
        if argument not in args.keys():
            args[argument] = DEFAULT_ARGUMENTS[argument]
    
    return args, FileNames

