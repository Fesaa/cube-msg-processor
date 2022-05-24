from os.path import exists
import sys

ALLOWED_ARGUMENTS = {'DailyAvarage': ['True', 'False'],
                     'ConsecutiveTime': ['True', 'False'],
                     'TotalMessages': ['True', 'False'],
                     'SaveGraphs': ['True', 'False']
                     }

DEFAULT_ARGUMENTS = {'DailyAvarage': False,
                     'ConsecutiveTime': False,
                     'TotalMessages': True,
                     'SaveGraphs': False
                    }

class InvalidArgument(Exception):

    def __init__(self, argument, *args):
        super().__init__(args)
        self.argument = argument

    def __str__(self):
        return f'{self.argument} is not a valid option. A list of valids is:\n{" -- ".join(ALLOWED_ARGUMENTS.keys())}'

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

