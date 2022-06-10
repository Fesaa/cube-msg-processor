import ast
import csv
import time
import json
import asyncio
import warnings
import matplotlib.pyplot as plt

from math import floor
from colorama import Fore, Style
from datetime import datetime, timedelta

from init import options
from functions import *
from constants import *

async def main():
    total_run_time = time.time()
    FileNames = options['FileName']

    args = options

    if args['TotalMessages'] or args['User'] is not True:
        dictTotalMessages = {"Q": 0, "S": 0}

    if args['Daily'] or args['User'] is not True:
        dictDaily = {}

    if args['ConsecutiveTime']:
        dictConsecutiveTime = {}

    if args['ReplyTimes']:
        dictReplyTimes = {i: [] for i in range(24)}
        dictAccurateReplyTimes = {(hour, minute): [] for hour in range(24) for minute in range(0,60,10)}

    if args['DailyMessages']:
        dictDailyMessages = {}
    
    if args['RoleDistribution']:
        dictRoleDistribution = {i: 0 for i in ROLES.keys()}
        RolesMsg = 0
    
    if args['HourlyActivity'] or args['User'] is not True:
        dictHourlyActivity = {i: 0 for i in range(24)}
        dictAccurateHourlyActivity = {(hour, minute): 0 for hour in range(24) for minute in range(0,60,10)}
    
    if args['User'] == 'Q':
        args['User'] = 'non staff replied'
    elif args['User'] == 'S':
        args["User"] == True

    file_reading_time = time.time()

    for index, FileName in enumerate(FileNames):

        with open(FileName, 'r') as f:
            reader = csv.reader(f)

            first_row = next(reader)
            current_time = 0

            if args['ConsecutiveTime']:
                    active_members = {}

            if index == 0:
                total_msgs = 0

                if args['ReplyTimes']:
                    messages_times = []
                    non_staff_replies = 0

                if args['StartDate'] == 'First Date':
                    start_date = '0000-00-00'
                    earliest_date = '9999-12-31'
                else:
                    start_date = args['StartDate']
                    earliest_date = start_date
                
                if args['EndDate'] == 'End Date':
                    end_date = '9999-12-31'
                else:
                    end_date = args['EndDate']

            for row in [first_row] + list(reader):
                current_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')

                if str(current_time.date()) < earliest_date and args['StartDate'] == 'First Date':
                    earliest_date = str(current_time.date())
                
                if start_date <= str(current_time.date()) <= end_date and (row[1] == args['User'] or args['User'] is True):
                    total_msgs += 1

                    if args['TotalMessages']:
                        if row[1] == 'non staff replied':
                            dictTotalMessages['Q'] += 1
                        else:
                            dictTotalMessages['S'] += 1
                            if row[1] in dictTotalMessages:
                                dictTotalMessages[row[1]] += 1
                            else:
                                dictTotalMessages[row[1]] = 1

                    if args['Daily'] or args['User'] is not True:
                        if row[1] != 'non staff replied' or args['User'] == 'non staff replied':
                            day = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').date()
                            if day in dictDaily.keys():
                                dictDaily[day] += 1
                            else:
                                dictDaily[day] = 1

                    if args['ConsecutiveTime']:
                        to_remove = []

                        if row[1] != 'non staff replied':
                            if row[1] not in active_members:
                                active_members[row[1]] = {'start_time': current_time, 'last_time': current_time}
                                
                            
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

                    if args['ReplyTimes']:

                        if row[1] == "non staff replied":
                            non_staff_replies += 1
                            if non_staff_replies >= args['IgnoreMessages']:
                                messages_times.append(current_time)
                        else:
                            if non_staff_replies > args['IgnoreMessages']:
                                for times in messages_times:
                                    times: datetime
                                    dictReplyTimes[times.hour].append(current_time - times)
                                    dictAccurateReplyTimes[(times.hour, floor(times.minute/10)*10)].append(current_time - times)

                                messages_times = []
                            non_staff_replies = 0

                    if args['DailyMessages']:
                        if row[1] != "non staff replied":
                            if row[1] in dictDailyMessages:
                                if current_time.day in dictDailyMessages[row[1]]:
                                    dictDailyMessages[row[1]][current_time.day] += 1
                                else:
                                    dictDailyMessages[row[1]][current_time.day] = 1
                            else:
                                dictDailyMessages[row[1]] = {current_time.day: 1}
                    
                    if args['RoleDistribution']:
                        if len(row) == 3:
                            user_roles = ast.literal_eval(row[2])
                            if len((set(user_roles) & set(STAFF_ROLES))) > 1:
                                to_add = [int(i) for i in user_roles if int(i) in STAFF_ROLES]
                            else:
                                to_add = [int(i) for i in user_roles if int(i) in ROLES]

                            if JAVA_ROLE in user_roles and BEDROCK_ROLE not in user_roles:
                                dictRoleDistribution['Java Only'] += 1
                            elif JAVA_ROLE not in user_roles and BEDROCK_ROLE in user_roles:
                                dictRoleDistribution['Bedrock Only'] += 1
                            elif JAVA_ROLE in user_roles and BEDROCK_ROLE in user_roles:
                                dictRoleDistribution['Dual'] += 1

                            if to_add == []:
                                dictRoleDistribution['No Roles'] += 1
                            else:
                                for i in to_add:
                                    dictRoleDistribution[i] += 1
                            
                            RolesMsg += 1
                    
                    if args['HourlyActivity'] or args['User'] is not True:
                        if row[1] != 'non staff replied':
                            dictHourlyActivity[current_time.hour] += 1
                            dictAccurateHourlyActivity[(current_time.hour, floor(current_time.minute/10) * 10)] += 1


    file_reading_time_end = time.time()
    processing_dicts_time = time.time()

    if args['User'] is True:
        amount_of_graphs = sum([1 for key, value in args.items() if value and key not in ["SaveGraphs", "ShowExplanation", "ShowGraphs", "IgnoreMessages", "StartDate", "FileName", "MinMsg", "MinTime", "UpdateJson", "EndDate", "Percentages", "User", "Output", "Accurate"]])
    else:
        amount_of_graphs = 2
    graph_placements = [((amount_of_graphs + 1)//2, 2, i + 1) for i in range(amount_of_graphs)]
    current_index = 0

    print(f'Data from {earliest_date} until {current_time.date()}')

    summary = f"{Fore.GREEN}Global Summary: {Style.RESET_ALL}\n\n"

    plt.style.use('ggplot')
    plt.figure(facecolor='silver')

    if args['TotalMessages'] and args['User'] is True:
        dictTotalMessages = {key: (value/total_msgs)*100 if args['Percentages'] else value for key, value in dictTotalMessages.items()}
        dictTotalMessages = await correct_dict_for_id(dictTotalMessages, not args['UpdateJson'])
        dictTotalMessages = dict(sorted(dictTotalMessages.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}TotalMessages{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {value}" if not args['Percentages'] else f"{key}: {round(value, 3)}%" for key, value in dictTotalMessages.items())]))
        summary += "Top 3 Users with most messages\n\t" + \
                "".join(f"{key}: {dictTotalMessages[key]}".ljust(25) if not args['Percentages'] else f"{key}: {round(dictTotalMessages[key], 3)}%".ljust(25) for key in list([i for i in dictTotalMessages.keys() if i not in ['Q', 'S']])[:3]) + "\n\n"

        l0 = list(reversed([i for i in dictTotalMessages.keys() if i not in ['Q', 'S'] and (dictTotalMessages[i] > args['MinMsg'] if not args['Percentages'] and args['User'] is True else dictTotalMessages[i] > 1)]))
        l1 = [dictTotalMessages[key] for key in l0]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.barh(l0, l1, color = colour_list(l1))
        plt.title(f'Amount of msg {"per member" if args["User"] is True else ""} {"in percentage of the total" if args["Percentages"] else ""}')
        plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

    if args['Daily'] or args['User'] is not True:
        dictDaily = {str(key): (value/total_msgs)*100 if args['Percentages'] else value for key, value in dictDaily.items()}
        dictDaily = {key: dictDaily[key] for key in sorted(dictDaily.keys(), reverse=True)}
        
        print(f'{Fore.MAGENTA}Daily{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {value}" if not args['Percentages'] else f"{key}: {round(value, 3)}%" for key, value in dictDaily.items())]))
        summary += "Top 3 most active days\n\t" + \
                "".join(f'{inv_dict(dictDaily)[value]}: {value}'.ljust(25) if not args['Percentages'] else f"{inv_dict(dictDaily)[value]}: {round(value, 3)}%".ljust(25) for value in sorted(dictDaily.values(), reverse=True)[:3]) + "\n\n"

        l0 = list(reversed([i for i in dictDaily.keys()]))
        l1 = [dictDaily[i] for i in l0]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.barh(l0, l1, color = colour_list(l1))
        plt.title('Amount msg by per day')
        plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

    if args['ConsecutiveTime'] and args['User'] is True:
        dictConsecutiveTime = {key: sum([i.total_seconds()/(3600) for i in value]) for key, value in dictConsecutiveTime.items()}
        dictConsecutiveTime = await correct_dict_for_id(dictConsecutiveTime, not args['UpdateJson'])
        dictConsecutiveTime = dict(sorted(dictConsecutiveTime.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}ConsecutiveTime{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {round(value, 2)}" for key, value in dictConsecutiveTime.items())]))
        summary += "Top 3 users with most time spend\n\t" + \
                "".join(f"{key}: {round(dictConsecutiveTime[key], 2)}".ljust(25) for key in list(dictConsecutiveTime.keys())[:3]) + "\n\n"

        l0 = list(reversed([key for key, value in dictConsecutiveTime.items() if value > args['MinTime']]))
        l1 = [dictConsecutiveTime[key] for key in l0]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.barh(l0, l1, color = colour_list(l1))
        plt.title('Total time spend in hours')
        plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

    if args['ReplyTimes'] and args['User'] is True:
        dictReplyTimes = {key: 0 if len(value) == 0 else sum(delta_t.total_seconds()/60 for delta_t in value)/len(value) for key, value in  dictReplyTimes.items()}
        dictAccurateReplyTimes = {f"{key[0]}:{key[1]}{0 if key[1] < 10 else ''}": 0 if len(value) == 0 else sum(delta_t.total_seconds()/60 for delta_t in value)/len(value) for key, value in  dictAccurateReplyTimes.items()}

        if args['Accurate']:
            used = dictAccurateReplyTimes
        else:
            used = dictReplyTimes

        print(f'{Fore.MAGENTA}ReplyTimes{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(
            f"{key}: {round(value, 2)}" for key, value in used.items())]))

        l0 = [str(i) for i in used.keys()]
        l1 = [i for i in used.values()]
        plt.subplot(*graph_placements[current_index])
        current_index += 1

        if args['Accurate']:
            plt.plot(l0, l1)
            plt.xticks(l0[0::6], l0[0::6], rotation='vertical', fontsize=font_size(24))
        else:
            plt.barh(l0, l1, color = colour_list(l1))
            plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

        plt.title(f'Avarage wait time on a question for a given hour. Ignores {args["IgnoreMessages"]} messages')

    if args['DailyMessages']:
        dictDailyMessages = {key: sum([j for j in value.values()])/(len([j for j in value.values()])) for key, value in dictDailyMessages.items()}
        dictDailyMessages = await correct_dict_for_id(dictDailyMessages, not args['UpdateJson'])
        dictDailyMessages = dict(sorted(dictDailyMessages.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}DailyMessages{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {round(value, 2)}" for key, value in dictDailyMessages.items())]))

        l0 = list(reversed([i for i in dictDailyMessages.keys() if dictDailyMessages[i] > args['MinMsg']/5]))
        l1 = [dictDailyMessages[i] for i in l0]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.barh(l0, l1, color = colour_list(l1))
        plt.title(f'Avarage msg per member on a day')
        plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))

    if args['RoleDistribution'] and args['User'] is True:
        dictRoleDistribution = {key: (dictRoleDistribution[key]/RolesMsg)*100 for key in dictRoleDistribution.keys()}
        dictRoleDistribution = dict(sorted(dictRoleDistribution.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}RoleDistribution{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{ROLES[key]}: {round(value, 2)}%" for key, value in dictRoleDistribution.items())]))
        summary += "Top 3 roles with most messages send\n\t" + \
                "".join(f'{ROLES[key]}: {round(dictRoleDistribution[key], 3)}%'.ljust(25) for key in list(dictRoleDistribution.keys())[:3]) + "\n\n"
        summary += "Top 3 staff roles with most messages send\n\t" + \
                "".join(f'{ROLES[key]}: {round(dictRoleDistribution[key], 3)}%'.ljust(25) for key in list(i for i in dictRoleDistribution.keys() if i in STAFF_ROLES)[:3]) + "\n\n"

        l0 = list(reversed([i for i in dictRoleDistribution.keys() if dictRoleDistribution[i] > 0]))
        l1 = [dictRoleDistribution[i] for i in l0]
        l0 = [ROLES[i] for i in l0]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.barh(l0, l1, color = colour_list(l1))
        plt.title(f'Role Distribution in percentage over {RolesMsg} messages')
        plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))
    
    if args['HourlyActivity'] or args['User'] is not True:
        dictHourlyActivity = {key: (dictHourlyActivity[key]/total_msgs)*100 for key in dictHourlyActivity.keys()}
        dictAccurateHourlyActivity = {f"{key[0]}:{key[1]}{0 if key[1] < 10 else ''}": (dictAccurateHourlyActivity[key]/total_msgs)*100 for key in dictAccurateHourlyActivity.keys()}

        if args['Accurate']:
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

        if args['Accurate']:
            plt.plot(l0, l1)
            plt.xticks(l0[0::6], l0[0::6], rotation='vertical', fontsize=font_size(24))
        else:
            plt.barh(l0, l1, color = colour_list(l1))
            plt.yticks(l0, l0, rotation='horizontal', fontsize=font_size(len(l0)))
        
        plt.title(f'Hourly Activity in percentage')
    
    print(summary)

    processing_dicts_time_end = time.time()

    print(f"--- Total Run Time {time.time() - total_run_time} seconds ---")
    print(f"--- File Reading Time {file_reading_time_end - file_reading_time} seconds ---")
    print(f"--- Making Plots Time {processing_dicts_time_end - processing_dicts_time -sum(ID_LOAD_TIME)} seconds ---")
    print(f"--- Fetching ids {sum(ID_LOAD_TIME)} seconds ---")

    with open('json/external_id_cache.json', 'w', encoding='ISO 8859-1') as f:
        json.dump({**EXTERNAL_ID_CACHE, **{str(key): value for key, value in ID_CACHE.items()}}, f)

    if args['SaveGraphs']:
        warnings.filterwarnings("ignore")
        plt.savefig('out.png')

    if args['ShowGraphs']:

        plt.subplots_adjust(left=0.1, bottom=0.15, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
        plt.suptitle(f'Data from {earliest_date} until {current_time.date() if str(current_time.date()) < args["EndDate"] else args["EndDate"]}. Times are CET\nTotal messages: {total_msgs}' + f'\n{"Info on user " + await get_name_from_id(args["User"], not args["UpdateJson"]) if args["User"] is not True else ""}',
        color = 'midnightblue')

        warnings.filterwarnings("ignore")
        plt.show()
    
    if args['Output']:
        out = {}

        if args['Daily'] or args['User'] is not True:
            out['Daily'] = dictDaily
        
        if args['ConsecutiveTime'] and args['User'] is True:
            out['ConsecutiveTime'] = dictConsecutiveTime
        
        if args['TotalMessages'] and args['User'] is True:
            out['TotalMessages'] = dictTotalMessages
        
        if args['ReplyTimes'] and args['User'] is True:
            if args['Accurate']:
                out['AccurateReplyTimes'] = {key: value for key, value in dictAccurateReplyTimes.items()}
            else:
                out['ReplyTimes'] = dictReplyTimes
        
        if args['DailyMessages'] and args['User'] is True:
            out['DailyMessages'] = dictDailyMessages
        
        if args['RoleDistribution'] and args['User'] is True:
            out['RoleDistribution'] = dictRoleDistribution
        
        if args['HourlyActivity'] or args['User'] is not True:
            if args['Accurate']:
                out['AccurateHourlyActivity'] = {key: value for key, value in dictAccurateHourlyActivity.items()}
            else:
                out['HourlyActivity'] = dictHourlyActivity
        
        with open('out/output.json', 'w', encoding='ISO 8859-1') as f:
            json.dump(out, f)

if __name__ == '__main__':
    asyncio.run(main())
