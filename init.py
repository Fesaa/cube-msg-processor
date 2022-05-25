from os.path import exists
from colorama import Fore, Style
import sys

ALLOWED_ARGUMENTS = {'Daily': ['True', 'False'],
                     'ConsecutiveTime': ['True', 'False'],
                     'TotalMessages': ['True', 'False'],
                     'SaveGraphs': ['True', 'False'],
                     'ShowExplanation': ['True', 'False'],
                     'ShowGraph': ['True', 'False']
                     }

DEFAULT_ARGUMENTS = {'Daily': True,
                     'ConsecutiveTime': False,
                     'TotalMessages': True,
                     'SaveGraphs': False,
                     'ShowExplanation': True,
                     'ShowGraph': True,
                    }

ARGUMENT_EXPLAIN = {'Daily': f'{Fore.CYAN}Daily{Style.RESET_ALL}: Adds a graphs to your figure with the total amount of messages per day. \nDefaults to{Fore.GREEN} True {Style.RESET_ALL}',
                    'ConsecutiveTime': f'{Fore.CYAN}ConsecutiveTime{Style.RESET_ALL}: Adds a graph to your figure with the total time spend by ' \
                                       f'a staff member in staff help. \nTime is added to the total if more than 5 messages have been send without ' \
                                       f'5 messages by an other staff member between two messages. \nDefaults to{Fore.RED} False {Style.RESET_ALL}',
                    'TotalMessages': f'{Fore.CYAN}TotalMessages{Style.RESET_ALL}: Adds a graph to your figure with the total messages send in staff help per staff member. \nDefaults to{Fore.GREEN} True {Style.RESET_ALL}',
                    'SaveGraphs': f"{Fore.CYAN}SaveGraphs{Style.RESET_ALL}: Save your figure to a .png in your cwd. \nDefaults to{Fore.RED} False {Style.RESET_ALL}",
                    'ShowExplanation': f"{Fore.CYAN}ShowExplanation{Style.RESET_ALL}: Shows an explanation about your chosen options. \nDefaults to{Fore.GREEN} True {Style.RESET_ALL}",
                    'ShowGraph': f'{Fore.CYAN}ShowGraph{Style.RESET_ALL}: Shows your graph after making it.\nDefaults to{Fore.GREEN} True {Style.RESET_ALL} '
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
        return f'The allowed options for {self.argument} are: \n{", ".join(ALLOWED_ARGUMENTS[self.argument])}'

class CustomFileError(Exception):
    def __init__(self, error, *args):
        super().__init__(args)
        self.error = error
    
    def __str__(self):
        return self.error


def arg_check(argument):
    try:
        argument.split('=')[1]
    except IndexError:
        raise InvalidLayout
    else:
        if argument.split('=')[0] in ALLOWED_ARGUMENTS.keys():
            if argument.split('=')[1] in ALLOWED_ARGUMENTS[argument.split('=')[0]]:
                return True
            else:
                raise InvalidOption(argument.split('=')[0])
        else:
            raise InvalidArgument(argument.split('=')[0])

def arg_correction(argument):
    if argument == 'True':
        return True
    elif argument == 'False':
        return False
    else:
        try:
            return int(argument)
        except ValueError:
            return argument

def on_start():

    try:
        if sys.argv[1].split('=')[0] == "FileName":
            FileName = sys.argv[1].split('=')[1]
        else:
            raise IndexError
    except IndexError:
        raise CustomFileError("Your first argument must be the filename:\nFileName=myFile.csv")
    else:
        if exists(FileName):
            args = {i.split('=')[0]: arg_correction(i.split('=')[1]) for i in sys.argv[2::] if arg_check(i)}
        else:
            raise CustomFileError('Please provide a valid FileName! Or you in the cwd?')
    
    for argument in ALLOWED_ARGUMENTS.keys():
        if argument not in args.keys():
            args[argument] = DEFAULT_ARGUMENTS[argument]
    
    return args, FileName

