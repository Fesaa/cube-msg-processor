import ast
import csv
import time
import json
import warnings
import matplotlib.pyplot as plt

from math import floor
from typing import Tuple
from os import listdir, path
from colorama import Fore, Style
from datetime import datetime, timedelta

from processor.functions import *
from processor.constants import *

async def grapher(options: dict):
    
    total_run_time = time.time()
    FileNames = options['FileName']

    if not FileNames:
        FileNames = [options['Path'] + i for i in listdir(options['Path']) if options['Path'] + i not in options['Exclude']]     

    if options['TotalMessages'] or options['User'] is not True:
        dictTotalMessages = {"Q": 0, "S": 0}

    if options['Daily'] or options['User'] is not True:
        dictDaily = {}

    if options['ConsecutiveTime']:
        dictConsecutiveTime = {}

    if options['ReplyTimes']:
        dictReplyTimes = {i: [] for i in range(24)}
        dictAccurateReplyTimes = {(hour, minute): [] for hour in range(24) for minute in range(0,60,10)}

    if options['DailyMessages']:
        dictDailyMessages = {}
    
    if options['RoleDistribution']:
        dictRoleDistribution = {i: 0 for i in ROLES.keys()}
        RolesMsg = 0
    
    if options['HourlyActivity'] or options['User'] is not True:
        dictHourlyActivity = {i: 0 for i in range(24)}
        dictAccurateHourlyActivity = {(hour, minute): 0 for hour in range(24) for minute in range(0,60,10)}

    file_reading_time = time.time()

    for index, FileName in enumerate(FileNames):

        with open(FileName, 'r') as f:
            reader = csv.reader(f)

            first_row = next(reader)
            current_time = 0

            if options['ConsecutiveTime']:
                    active_members = {}
            
            if options['ReplyTimes']:
                messages_times = []

            if index == 0:
                total_msgs = 0

                if options['ReplyTimes']:
                    messages_times = []

                if options['StartDate'] == 'First Date':
                    start_date = '0000-00-00'
                    earliest_date: str = '9999-12-31'
                else:
                    start_date = options['StartDate']
                    earliest_date = start_date
                
                if options['EndDate'] == 'End Date':
                    end_date = '9999-12-31'
                    last_date = '0000-00-00'
                else:
                    end_date = options['EndDate']
                    last_date = end_date

            for row in [first_row] + list(reader):
                current_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
                if len(row) == 3:
                    roles = ast.literal_eval(row[2])
                else:
                    roles = []

                if str(current_time.date()) < earliest_date and options['StartDate'] == 'First Date':
                    earliest_date = str(current_time.date())
                
                if last_date < str(current_time.date()) and options['EndDate'] == 'End Date':
                    last_date = str(current_time.date()) 
                
                if start_date <= str(current_time.date()) <= end_date and (row[1] == str(options['User']) or options['User'] is True or options['User'] == 'Q'):
                    total_msgs += 1

                    do = False
                    if options['StaffHelp']:
                        if len(row) == 3:
                            if check_staff(roles):
                                do = True
                            elif options['User'] == 'Q':
                                do = True
                        else:
                            if row[1] != 'non staff replied':
                                do = True
                            elif options['User'] == 'Q':
                                do = True
                    elif row[1] != 'non staff replied':
                        do = True

                    if options['TotalMessages'] and do:

                        if options['StaffHelp']:
                            if (check_staff(roles) and len(row) == 3) or row[1] != 'non staff replied':
                                dictTotalMessages['S'] += 1 

                        if do:
                            if row[1] in dictTotalMessages:
                                dictTotalMessages[row[1]] += 1
                            else:
                                dictTotalMessages[row[1]] = 1

                    if (options['Daily'] or options['User'] is not True) and do:
                        day = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').date()
                        if day in dictDaily.keys():
                            dictDaily[day] += 1
                        else:
                            dictDaily[day] = 1

                    if options['ConsecutiveTime']:
                        to_remove = []

                        if row[1] not in active_members and do:
                            active_members[row[1]] = {'start_time': current_time, 'last_time': current_time}
                        elif do:
                            active_members[row[1]]['last_time'] = current_time

                        for user_id, info in active_members.items():
                            time_difference: timedelta = current_time - info['last_time']

                            if time_difference.total_seconds()/60 > 10:
                                delta_t: timedelta = info['last_time'] - info['start_time']
                                if delta_t.total_seconds() == 0:
                                    delta_t = timedelta(minutes=5)
                                
                                if user_id in dictConsecutiveTime:
                                    dictConsecutiveTime[user_id].append(delta_t)
                                else:
                                    dictConsecutiveTime[user_id] = [delta_t]

                                to_remove.append(user_id)
                            
                        for user_id in to_remove:
                            active_members.pop(user_id)

                    if options['ReplyTimes']:
                        if (not check_staff(roles) and len(row) == 3) or row[1] == 'non staff replied':
                            try:
                                last_msg = messages_times[-1]
                            except IndexError:
                                last_msg = (00, datetime(year=1, month=1, day=1))
                            
                            if last_msg[0] != row[1] or row[1] == 'non staff replied':
                                messages_times.append((row[1], current_time))
                        else:

                            for times in messages_times[options['IgnoreMessages'] if len(messages_times) > options['IgnoreMessages'] else 0:]:
                                times: Tuple[int, datetime]
                                dictReplyTimes[times[1].hour].append(current_time - times[1])
                                dictAccurateReplyTimes[(times[1].hour, floor(times[1].minute/10)*10)].append(current_time - times[1])

                            messages_times = []

                    if options['DailyMessages'] and do:
                        if row[1] in dictDailyMessages:
                            if current_time.day in dictDailyMessages[row[1]]:
                                dictDailyMessages[row[1]][current_time.day] += 1
                            else:
                                dictDailyMessages[row[1]][current_time.day] = 1
                        else:
                            dictDailyMessages[row[1]] = {current_time.day: 1}
                    
                    if options['RoleDistribution'] and len(row) == 3:
                        to_add = [int(i) for i in roles if int(i) in ROLES]

                        if JAVA_ROLE in roles and BEDROCK_ROLE not in roles:
                            dictRoleDistribution['Java Only'] += 1
                        elif JAVA_ROLE not in roles and BEDROCK_ROLE in roles:
                            dictRoleDistribution['Bedrock Only'] += 1
                        elif JAVA_ROLE in roles and BEDROCK_ROLE in roles:
                            dictRoleDistribution['Dual'] += 1

                        if to_add == []:
                            dictRoleDistribution['No Roles'] += 1
                        else:
                            for i in to_add:
                                dictRoleDistribution[i] += 1
                            
                        RolesMsg += 1
                    
                    if options['HourlyActivity'] or options['User'] is not True and do:
                        dictHourlyActivity[current_time.hour] += 1
                        dictAccurateHourlyActivity[(current_time.hour, floor(current_time.minute/10) * 10)] += 1

    if options['StaffHelp']:
        dictTotalMessages['Q'] = total_msgs - dictTotalMessages['S']

    file_reading_time_end = time.time()
    processing_dicts_time = time.time()

    if options['User'] is True:
        amount_of_graphs = sum([1 for key, value in options.items() if value and key not in ["FigName", "ShowExplanation", "ShowGraphs", "IgnoreMessages", "StartDate", "FileName", "MinMsg", "MinTime", "UpdateJson", "EndDate", "Percentages", "User", "Output", "Accurate", "Path", "StaffHelp", "Exclude"]])
    else:
        amount_of_graphs = 2
    graph_placements = [((amount_of_graphs + 1)//2, 2, i + 1) for i in range(amount_of_graphs)]
    current_index = 0

    print(f'Data from {earliest_date} until {last_date}')

    summary = f"{Fore.GREEN}Global Summary: {Style.RESET_ALL}\n\n"

    plt.style.use('ggplot')
    plt.figure(facecolor='silver', figsize=(15 if options['User'] is True else 10, 5 * amount_of_graphs//2))

    if options['TotalMessages'] and options['User'] is True:
        dictTotalMessages = {key: (value/total_msgs)*100 if options['Percentages'] else value for key, value in dictTotalMessages.items()}
        dictTotalMessages = await correct_dict_for_id(dictTotalMessages, not options['UpdateJson'])
        dictTotalMessages = dict(sorted(dictTotalMessages.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}TotalMessages{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {value}" if not options['Percentages'] else f"{key}: {round(value, 3)}%" for key, value in dictTotalMessages.items())]))
        summary += "Top 3 Users with most messages\n\t" + \
                "".join(f"{key}: {dictTotalMessages[key]}".ljust(25) if not options['Percentages'] else f"{key}: {round(dictTotalMessages[key], 3)}%".ljust(25) for key in list([i for i in dictTotalMessages.keys() if i not in ['Q', 'S']])[:3]) + "\n\n"

        l0 = list(reversed([i for i in dictTotalMessages.keys() if i not in ['Q', 'S'] and (dictTotalMessages[i] > options['MinMsg'] if not options['Percentages'] and options['User'] is True else dictTotalMessages[i] > 1)]))
        if len(l0) > 0:
            l1 = [dictTotalMessages[key] for key in l0]
            plt.subplot(*graph_placements[current_index])
            current_index += 1
            plt.barh(l0, l1, color = colour_list(l1))
            plt.title(f'Amount of msg {"per member" if options["User"] is True else ""} {"%" if options["Percentages"] else ""}')
            plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

    if options['Daily'] or options['User'] is not True:
        dictDaily = {str(key): (value/total_msgs)*100 if options['Percentages'] else value for key, value in dictDaily.items()}
        dictDaily = {key: dictDaily[key] for key in sorted(dictDaily.keys(), reverse=True)}
        
        print(f'{Fore.MAGENTA}Daily{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {value}" if not options['Percentages'] else f"{key}: {round(value, 3)}%" for key, value in dictDaily.items())]))
        summary += "Top 3 most active days\n\t" + \
                "".join(f'{inv_dict(dictDaily)[value]}: {value}'.ljust(25) if not options['Percentages'] else f"{inv_dict(dictDaily)[value]}: {round(value, 3)}%".ljust(25) for value in sorted(dictDaily.values(), reverse=True)[:3]) + "\n\n"

        l0 = list(reversed([i for i in dictDaily.keys()]))
        l1 = [dictDaily[i] for i in l0]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.barh(l0, l1, color = colour_list(l1))
        plt.title(f'Amount msg by per day {"%" if options["Percentages"] else ""}')
        plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

    if options['ConsecutiveTime'] and options['User'] is True:
        dictConsecutiveTime = {key: sum([i.total_seconds()/(3600) for i in value]) for key, value in dictConsecutiveTime.items()}
        dictConsecutiveTime = await correct_dict_for_id(dictConsecutiveTime, not options['UpdateJson'])
        dictConsecutiveTime = dict(sorted(dictConsecutiveTime.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}ConsecutiveTime{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {round(value, 2)}" for key, value in dictConsecutiveTime.items())]))
        summary += "Top 3 users with most time spend\n\t" + \
                "".join(f"{key}: {round(dictConsecutiveTime[key], 2)}".ljust(25) for key in list(dictConsecutiveTime.keys())[:3]) + "\n\n"

        l0 = list(reversed([key for key, value in dictConsecutiveTime.items() if value > options['MinTime']]))
        if len(l0) > 0:
            l1 = [dictConsecutiveTime[key] for key in l0]
            plt.subplot(*graph_placements[current_index])
            current_index += 1
            plt.barh(l0, l1, color = colour_list(l1))
            plt.title('Total time spend in hours')
            plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

    if options['ReplyTimes'] and options['User'] is True:
        dictReplyTimes = {key: 0 if len(value) == 0 else sum(delta_t.total_seconds()/60 for delta_t in value)/len(value) for key, value in  dictReplyTimes.items()}
        dictAccurateReplyTimes = {f"{key[0]}:{key[1]}{0 if key[1] < 10 else ''}": 0 if len(value) == 0 else sum(delta_t.total_seconds()/60 for delta_t in value)/len(value) for key, value in  dictAccurateReplyTimes.items()}

        if options['Accurate']:
            used = dictAccurateReplyTimes
        else:
            used = dictReplyTimes

        print(f'{Fore.MAGENTA}ReplyTimes{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(
            f"{key}: {round(value, 2)}" for key, value in used.items())]))

        l0 = [str(i) for i in used.keys()]
        l1 = [i for i in used.values()]
        plt.subplot(*graph_placements[current_index])
        current_index += 1

        if options['Accurate']:
            plt.plot(l0, l1)
            plt.xticks(l0[0::6], l0[0::6], rotation='vertical', fontsize=font_size(24))
        else:
            plt.barh(l0, l1, color = colour_list(l1))
            plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

        plt.title(f'Average wait time on a question per {"hour" if not options["Accurate"] else "10 minutes"}. Ignores {options["IgnoreMessages"]} messages')

    if options['DailyMessages'] and options['User'] is True:
        dictDailyMessages = {key: sum([j for j in value.values()])/(len([j for j in value.values()])) for key, value in dictDailyMessages.items()}
        dictDailyMessages = await correct_dict_for_id(dictDailyMessages, not options['UpdateJson'])
        dictDailyMessages = dict(sorted(dictDailyMessages.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}DailyMessages{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {round(value, 2)}" for key, value in dictDailyMessages.items())]))

        l0 = list(reversed([i for i in dictDailyMessages.keys() if dictDailyMessages[i] > (options['MinMsg']/5 if not options['Percentages'] else 1/5 * max(dictDailyMessages.values())) ]))
        if len(l0) > 0:
            l1 = [dictDailyMessages[i] for i in l0]
            plt.subplot(*graph_placements[current_index])
            current_index += 1
            plt.barh(l0, l1, color = colour_list(l1))
            plt.title(f'Average msg per member on a day')
            plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

    if options['RoleDistribution'] and options['User'] is True:
        dictRoleDistribution = {key: (dictRoleDistribution[key]/RolesMsg)*100 for key in dictRoleDistribution.keys()}
        dictRoleDistribution = dict(sorted(dictRoleDistribution.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}RoleDistribution{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{ROLES[key]}: {round(value, 2)}%" for key, value in dictRoleDistribution.items())]))
        summary += "Top 3 roles with most messages send\n\t" + \
                "".join(f'{ROLES[key]}: {round(dictRoleDistribution[key], 3)}%'.ljust(25) for key in list(dictRoleDistribution.keys())[:3]) + "\n\n"
        summary += "Top 3 staff roles with most messages send\n\t" + \
                "".join(f'{ROLES[key]}: {round(dictRoleDistribution[key], 3)}%'.ljust(25) for key in list(i for i in dictRoleDistribution.keys() if i in STAFF_ROLES)[:3]) + "\n\n"

        l0 = list(reversed([i for i in dictRoleDistribution.keys() if dictRoleDistribution[i] > 0]))
        if len(l0) > 0:
            l1 = [dictRoleDistribution[i] for i in l0]
            l0 = [ROLES[i] for i in l0]
            plt.subplot(*graph_placements[current_index])
            current_index += 1
            plt.barh(l0, l1, color = colour_list(l1))
            plt.title(f'Role Distribution over {RolesMsg} messages %')
            plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))  
    
    if options['HourlyActivity'] or options['User'] is not True:
        dictHourlyActivity = {key: (dictHourlyActivity[key]/total_msgs)*100 for key in dictHourlyActivity.keys()}
        dictAccurateHourlyActivity = {f"{key[0]}:{key[1]}{0 if key[1] < 10 else ''}": (dictAccurateHourlyActivity[key]/total_msgs)*100 for key in dictAccurateHourlyActivity.keys()}

        if options['Accurate']:
            used = dictAccurateHourlyActivity
        else:
            used = dictHourlyActivity

        print(f'{Fore.MAGENTA}HourlyActivity{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {round(value,2)}%" for key, value in used.items())]))
        summary += "Top 3 most active hours\n\t" + \
            "".join(f'{inv_dict(used)[value]}: {round(value, 3)}%'.ljust(25) for value in sorted(used.values(), reverse=True)[:3]) + "\n\n"


        l0 = [i for i in used.keys()]
        l1 = [i for i in used.values()]
        plt.subplot(*graph_placements[current_index])
        current_index += 1

        if options['Accurate']:
            plt.plot(l0, l1)
            plt.xticks(l0[0::6], l0[0::6], rotation='vertical', fontsize=font_size(24))
        else:
            plt.barh(l0, l1, color = colour_list(l1))
            plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))
        
        plt.title(f'Hourly Activity %')
    
    print(summary)
    plt.subplots_adjust(left=0.1, bottom=0.10, right=0.9, top=0.93 if options['User'] is True else 0.80, wspace=0.2, hspace=0.2)
    plt.suptitle(f'Data from {earliest_date} until {current_time.date() if str(current_time.date()) < options["EndDate"] else options["EndDate"]}. Times are CET\nTotal messages: {total_msgs}' + f'\n{"Info on user " + await get_name_from_id(options["User"], not options["UpdateJson"]) if options["User"] is not True else ""}',
    color = 'midnightblue')

    processing_dicts_time_end = time.time()

    with open('data/json/external_id_cache.json', 'w', encoding='ISO 8859-1') as f:
        json.dump({**EXTERNAL_ID_CACHE, **{str(key): value for key, value in ID_CACHE.items()}}, f)

    warnings.filterwarnings("ignore")
    if options['ShowGraphs']:
        plt.show()

    output_file_name = str(earliest_date).replace('-', '') + "-" + str(last_date).replace('-', '')
    if options['User'] is not True:
        output_file_name += '_' + (await get_name_from_id(options["User"], True))
    if options['StaffHelp']:
        output_file_name += '_StaffHelp'
    
    n = 0
    output_file_name += '_0'
    
    time_saving_fig0 = time.time()
    while path.exists(f'data/out/{output_file_name}.png'):
        n += 1
        output_file_name = output_file_name[:-1]
        output_file_name += str(n)
    
    plt.savefig(f'data/out/{output_file_name}.png', dpi=500)
    time_saving_fig1 = time.time()
    
    out = {}

    if options['Daily'] or options['User'] is not True:
        out['Daily'] = dictDaily
    
    if options['ConsecutiveTime'] and options['User'] is True:
        out['ConsecutiveTime'] = dictConsecutiveTime
    
    if options['TotalMessages'] and options['User'] is True:
        out['TotalMessages'] = dictTotalMessages
    
    if options['ReplyTimes'] and options['User'] is True:
        if options['Accurate']:
            out['AccurateReplyTimes'] = {key: value for key, value in dictAccurateReplyTimes.items()}
        else:
            out['ReplyTimes'] = dictReplyTimes
    
    if options['DailyMessages'] and options['User'] is True:
        out['DailyMessages'] = dictDailyMessages
    
    if options['RoleDistribution'] and options['User'] is True:
        out['RoleDistribution'] = dictRoleDistribution
    
    if options['HourlyActivity'] or options['User'] is not True:
        if options['Accurate']:
            out['AccurateHourlyActivity'] = {key: value for key, value in dictAccurateHourlyActivity.items()}
        else:
            out['HourlyActivity'] = dictHourlyActivity
    
    with open(f'data/out/{output_file_name}.json', 'w', encoding='ISO 8859-1') as f:
        json.dump(out, f)
    
    print(f"--- Total Run Time {time.time() - total_run_time} seconds ---")
    print(f"--- File Reading Time {file_reading_time_end - file_reading_time} seconds ---")
    print(f"--- Making Plots Time {processing_dicts_time_end - processing_dicts_time -sum(ID_LOAD_TIME)} seconds ---")
    print(f"--- Fetching ids {sum(ID_LOAD_TIME)} seconds ---")
    print(f"--- Saving graph time {time_saving_fig1 - time_saving_fig0} seconds ---")