from module.CommandLineOptions import CommandLineOption, CommandLineOptions
from typing import List
from colorama import Fore, Style

command_line_options = CommandLineOptions()
command_line_options.add_option(CommandLineOption('FileName', regex=r'\w*', return_type=List[str], info=f'Filenames to process'))
command_line_options.add_option(CommandLineOption('Daily', regex=r'\b(False|True)\b', default_option=True, return_type=bool,
                                info=f'{Fore.CYAN}Daily{Style.RESET_ALL}: Adds a graphs to your figure with the total amount of messages per day.\nMinimum of {Fore.MAGENTA}10{Style.RESET_ALL} messages are needed to be displayed on the graph.'))
command_line_options.add_option(CommandLineOption('ConsecutiveTime', regex=r'\b(False|True)\b', default_option=False, return_type=bool,
                                info=f'{Fore.CYAN}ConsecutiveTime{Style.RESET_ALL}: Adds a graph to your figure with the total time spend by ' \
                                       f'a staff member in staff help. \nTime is added to the total if more than 5 messages have been send without ' \
                                       f'5 messages by an other staff member between two messages.\nMinimum of {Fore.MAGENTA}30min {Style.RESET_ALL} is needed to be displayed on the graph.'))
command_line_options.add_option(CommandLineOption('TotalMessages', regex=r'\b(False|True)\b', default_option=True, return_type=bool,
                                info=f'{Fore.CYAN}TotalMessages{Style.RESET_ALL}: Adds a graph to your figure with the total messages send in staff help per staff member.'))
command_line_options.add_option(CommandLineOption('SaveGraphs', regex=r'\b(False|True)\b', default_option=False, return_type=bool,
                                info=f"{Fore.CYAN}SaveGraphs{Style.RESET_ALL}: Save your figure to a .png in your cwd."))
command_line_options.add_option(CommandLineOption('ShowGraphs', regex=r'\b(False|True)\b', default_option=True, return_type=bool,
                                info=f'{Fore.CYAN}ShowGraph{Style.RESET_ALL}: Shows your graph after making it.'))
command_line_options.add_option(CommandLineOption('ReplyTimes', regex=r'\b(False|True)\b', default_option=False, return_type=bool,
                                info=f'{Fore.CYAN}ReplyTimes{Style.RESET_ALL}: Adds a graphs to your figure with the average waiting time per time slots of one hour.'))
command_line_options.add_option(CommandLineOption('IgnoreMessages', regex=r'\b([0-9]|1[0-9])\b', default_option=2, return_type=int,
                                info=f'{Fore.CYAN}IgnoreMessages{Style.RESET_ALL}: amount of non staff messages have to be send before we start counting wait time. This to take thank you messages into account.'))
command_line_options.add_option(CommandLineOption('DailyStaffMessages', regex=r'\b(False|True)\b', default_option=False, return_type=bool,
                                info=f'{Fore.CYAN}DailyStaffMessages{Style.RESET_ALL}: Adds a graphs to your figure with the average amount of messages per day in the recorded period.'))
command_line_options.add_option(CommandLineOption('StartDate', regex=r'^\d{4}[\-\/\s]?((((0[13578])|(1[02]))[\-\/\s]?(([0-2][0-9])|(3[01])))|(((0[469])|(11))[\-\/\s]?(([0-2][0-9])|(30)))|(02[\-\/\s]?[0-2][0-9]))$',
                                default_option='First Date', return_type=str, info=f'{Fore.CYAN}StartDate{Style.RESET_ALL}: Force a date to start registering data from. A data later than the last recorded day will just return no information.'))                                
command_line_options.add_option(CommandLineOption('MinMsg', regex=r'\b(\d{1,3})\b', default_option=10, return_type=int,
                                info=f'{Fore.CYAN}MinMsg{Style.RESET_ALL}: Minimal messages send in the channel to appear on TotalMessages graph.'))


options = command_line_options.on_start()