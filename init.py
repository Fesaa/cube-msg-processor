from CommandLineOptions import CommandLineOptions, CommandLineOption, RegexOptions
from typing import List
from colorama import Fore, Style

command_line_options = CommandLineOptions()
file_option_one = command_line_options.add_option(CommandLineOption('FileName', regex=r'\b.*\.csv\b', return_type=List[str],
                                info=f'{Fore.CYAN}FileName{Style.RESET_ALL}: Filenames to process'))
file_option_two = command_line_options.add_option(CommandLineOption('Path', regex=RegexOptions.SIMPLE_STR, return_type=str,
                                info=f'{Fore.CYAN}Path{Style.RESET_ALL}: specify a path to get all files from.'))
command_line_options.add_dependency(file_option_one, file_option_two)
command_line_options.add_option(CommandLineOption('Exclude', regex=RegexOptions.SIMPLE_STR, default_argument=[], return_type=List[str],
                                info=f'{Fore.CYAN}Exclude{Style.RESET_ALL}: not use certain files. Should be used in combination with {Fore.CYAN}Path{Style.RESET_ALL}.'))
command_line_options.add_option(CommandLineOption('Daily', regex=RegexOptions.BOOL, default_argument=False, return_type=bool,
                                info=f'{Fore.CYAN}Daily{Style.RESET_ALL}: Adds a graphs to your figure with the total amount of messages per day.\nMinimum of {Fore.MAGENTA}10{Style.RESET_ALL} messages are needed to be displayed on the graph.'))
command_line_options.add_option(CommandLineOption('ConsecutiveTime', regex=RegexOptions.BOOL, default_argument=True, return_type=bool,
                                info=f'{Fore.CYAN}ConsecutiveTime{Style.RESET_ALL}: Adds a graph to your figure with the total time spend in the channel. \nMinimum of {Fore.MAGENTA}30min {Style.RESET_ALL}is needed to be displayed on the graph.'))
command_line_options.add_option(CommandLineOption('TotalMessages', regex=RegexOptions.BOOL, default_argument=True, return_type=bool,
                                info=f'{Fore.CYAN}TotalMessages{Style.RESET_ALL}: Adds a graph to your figure with the total messages send in the channel per member.'))
command_line_options.add_option(CommandLineOption('ReplyTimes', regex=RegexOptions.BOOL, default_argument=False, return_type=bool,
                                info=f'{Fore.CYAN}ReplyTimes{Style.RESET_ALL}: Adds a graphs to your figure with the average waiting time per time slots of one hour.'))
command_line_options.add_option(CommandLineOption('DailyMessages', regex=RegexOptions.BOOL, default_argument=False, return_type=bool,
                                info=f'{Fore.CYAN}DailyMessages{Style.RESET_ALL}: Adds a graphs to your figure with the average amount of messages per day in the recorded period.'))
command_line_options.add_option(CommandLineOption('RoleDistribution', regex=RegexOptions.BOOL, default_argument=True, return_type=bool,
                                info=f'{Fore.CYAN}RoleDistribution{Style.RESET_ALL}: Adds a graph to your figure with the msg per role. Will be the displayed in percentage.'))
command_line_options.add_option(CommandLineOption('HourlyActivity', regex=RegexOptions.BOOL, default_argument=True, return_type=bool,
                                info=f'{Fore.CYAN}HourlyActivity{Style.RESET_ALL}: Adds a graph to your figure with the percentage of msg send per hour.'))
command_line_options.add_option(CommandLineOption('IgnoreMessages', regex=r'\b([0-9]|1[0-9])\b', default_argument=2, return_type=int,
                                info=f'{Fore.CYAN}IgnoreMessages{Style.RESET_ALL}: amount of non staff messages have to be send before we start counting wait time. This to take thank you messages into account. {Fore.RED}[Staff Help Specific]{Style.RESET_ALL}'))
command_line_options.add_option(CommandLineOption('Percentages', regex=RegexOptions.BOOL, default_argument=False, return_type=bool,
                                info=f'{Fore.CYAN}Percentages{Style.RESET_ALL}: Converts absolute values to percentages on available graphs.'))
command_line_options.add_option(CommandLineOption('StartDate', regex=RegexOptions.DATE, default_argument='First Date', return_type=str,
                                info=f'{Fore.CYAN}StartDate{Style.RESET_ALL}: Force a date to start registering data from. A date later than the last recorded day will just return no information.'))                                
command_line_options.add_option(CommandLineOption('EndDate', regex=RegexOptions.DATE, default_argument='End Date', return_type=str,
                                info=f'{Fore.CYAN}EndDate{Style.RESET_ALL}: Force a date to end registering data from. A date earlier than the first recorded day will just return no information.'))
command_line_options.add_option(CommandLineOption('User', regex=r'\b(\d{18}|Q)\b', default_argument=True, return_type=str,
                                info=f'{Fore.CYAN}User{Style.RESET_ALL}: Only record info on a singular person. Will choose the graphs for you.'))
command_line_options.add_option(CommandLineOption('MinMsg', regex=r'\b(\d{1,3})\b', default_argument=10, return_type=int,
                                info=f'{Fore.CYAN}MinMsg{Style.RESET_ALL}: Minimal messages send in the channel to appear on TotalMessages graph.'))
command_line_options.add_option(CommandLineOption('MinTime', regex=r'\b(\d{1,2}\.{0,1}\d{0,2})\b', default_argument=0.5, return_type=float,
                                info=f'{Fore.CYAN}MinTime{Style.RESET_ALL}: Minium time spend in the channel to be displayed on the graph.'))
command_line_options.add_option(CommandLineOption('UpdateJson', regex=RegexOptions.BOOL, default_argument=False, return_type=bool,
                                info=f'{Fore.CYAN}UpdateJson{Style.RESET_ALL}: Save ID_CACHE to external_id_cache.json for future reference. When True, no usernames will be loaded from the json.'))
command_line_options.add_option(CommandLineOption('FigName', regex=RegexOptions.SIMPLE_STR, default_argument='output', return_type=str,
                                info=f"{Fore.CYAN}FigName{Style.RESET_ALL}: Name of the saved .png file"))
command_line_options.add_option(CommandLineOption('ShowGraphs', regex=RegexOptions.BOOL, default_argument=False, return_type=bool,
                                info=f'{Fore.CYAN}ShowGraphs{Style.RESET_ALL}: Shows your graph after making it.'))
command_line_options.add_option(CommandLineOption('Accurate', regex=RegexOptions.BOOL, default_argument=False, return_type=bool,
                                info=f'{Fore.CYAN}Accurate{Style.RESET_ALL}: More accurate division of times.'))
command_line_options.add_option(CommandLineOption('StaffHelp', regex=RegexOptions.BOOL, return_type=bool, default_argument=False,
                                info=f'{Fore.CYAN}StaffHelp{Style.RESET_ALL}: Filters staff and non staff msg. Only use when Only checking staff help.'))