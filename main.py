from init import on_start, ARGUMENT_EXPLAIN
import matplotlib.pyplot as plt
from datetime import datetime
from colorama import Fore, Style
import requests, csv, json, asyncio, time

id_cache = dict()


# Need to find better way
def correct_username(s: str) -> str:
    while r'\u' in s:
        for index, letter in enumerate(s):
            if index < len(s):
                if letter + s[index + 1] == r'\u':
                    s = s[:index] + s[index + 6:]
                    break
    return s


async def get_name_from_id(id: int) -> str:

    config = json.load(open('config.json'))

    if id in id_cache.keys():
        return id_cache[id]
    else:
        while True:
            res = requests.get(f"https://discord.com/api/v9/users/{id}", headers={"Authorization": config.get('TOKEN')})

            if str(res) == "<Response [429]>":
                await asyncio.sleep(5)

            elif str(res) == "<Response [200]>":
                username = correct_username(res.text.split('"username": "')[1].split('",')[0])

                if len(username) > 15:
                    username = username[:15] + '...'

                id_cache[id] = username
                return username

            else:
                print(res)
                await asyncio.sleep(1)

async def correct_dict_for_id(d: dict) -> dict:
    return {await get_name_from_id(int(key)) if key.isdigit() else key : value for key, value in d.items()}

async def main():
    total_run_time = time.time()
    args, FileName = on_start()
    

    if args['ShowExplanation']:
        print("\n\n".join([ARGUMENT_EXPLAIN[key] for key in args.keys() if args[key]]))
        print('==================================================\n')

    if args['TotalMessages']:
        dictReply = {"Q": 0, "S": 0}

    if args['Daily']:
        dictDayMessages = {}

    if args['ConsecutiveTime']:
        dictConsecutiveTime = {}
    
    if args['ReplyTimes']:
        dictReplyTimes = {i: [datetime(year=2022, month=10, day=1, microsecond=1) - datetime(year=2022, month=10, day=1)] for i in range(24)}

    if args['DailyStaffMessages']:
        dictDayStaffMessages = {}
    
    file_reading_time = time.time()
    with open(FileName, 'r') as f:
        reader = csv.reader(f)

        first_row = next(reader)
        start_time = datetime.strptime(first_row[0], '%Y-%m-%d %H:%M:%S.%f')
        last_time = 0
        
        if args['ConsecutiveTime']:
            current_staff = 0
            current_count = 0
            current_time = start_time
            interruptions = 5
            ConsecutiveTime_non_staff_replies = 0
        
        if args['ReplyTimes']:
            last_reply_time = start_time
            non_staff_replies = 0
        
        if args['StartDate'] == 'First Date':
            start_date = str(start_time.date())
        else:
            start_date = args['StartDate']
            

        for row in [first_row] + list(reader):
            last_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        
            if start_date <= str(last_time.date()):

                if args['TotalMessages']:
                    if row[1] == 'non staff replied':
                        dictReply['Q'] += 1
                    else:
                        dictReply['S'] += 1
                        if row[1] in dictReply:
                            dictReply[row[1]] += 1
                        else:
                            dictReply[row[1]] = 1

                if args['Daily']:
                    if row[1] != 'non staff replied':
                        day = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').date()
                        if day in dictDayMessages.keys():
                            dictDayMessages[day] += 1
                        else:
                            dictDayMessages[day] = 1

                if args['ConsecutiveTime']:
                    if row[1] != 'non staff replied':
                        if row[1] != current_staff:
                            if current_count > 5:
                                if interruptions == 5:
                                    if current_staff != 0:
                                        if current_staff in dictConsecutiveTime:
                                            dictConsecutiveTime[current_staff].append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f') - current_time)
                                        else:
                                            dictConsecutiveTime[current_staff] = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f') - current_time]
                                    current_staff, current_count, current_time, interruptions = row[1], 1, datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'), 0
                                else:
                                    interruptions += 1
                            else:
                                current_staff, current_count, current_time, interruptions = row[1], 1, datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'), 0
                        else:
                            current_count += 1
                            interruptions = 0
                    else:
                        if ConsecutiveTime_non_staff_replies == 20:
                            if current_staff != 0:
                                if current_staff in dictConsecutiveTime:
                                    dictConsecutiveTime[current_staff].append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f') - current_time)
                                else:
                                    dictConsecutiveTime[current_staff] = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f') - current_time]
                            current_staff, current_count, current_time, interruptions = 0, 0, datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'), 0
                        else:
                            ConsecutiveTime_non_staff_replies += 1



                if args['ReplyTimes']:

                    if row[1] == "non staff replied":
                        non_staff_replies += 1
                        if non_staff_replies == args['IgnoreMessages']:
                            last_reply_time = last_time
                    else:
                        if non_staff_replies > args['IgnoreMessages']:
                            dictReplyTimes[last_time.hour].append(last_time - last_reply_time)
                        non_staff_replies, last_reply_time = 0, last_time
                
                if args['DailyStaffMessages']:
                    if row[1] != "non staff replied":
                        if row[1] in dictDayStaffMessages:
                            if last_time.day in dictDayStaffMessages[row[1]]:
                                dictDayStaffMessages[row[1]][last_time.day] += 1
                            else:
                                dictDayStaffMessages[row[1]][last_time.day] = 1
                        else:
                            dictDayStaffMessages[row[1]] = {last_time.day: 1}
                            

    file_reading_time_end = time.time()
    processing_dicts_time = time.time()

    amount_of_graphs = sum([1 for key, value in args.items() if value and key not in ["SaveGraphs", "ShowExplanation", "ShowGraph", "IgnoreMessages", "StartDate"]])

    graph_placements = [((amount_of_graphs + 1)//2, 2, i + 1) for i in range(amount_of_graphs)]
    current_index = 0

    print(f'Data from {start_date} until {last_time.date()}')

    if args['TotalMessages']:
        dictReply = await correct_dict_for_id(dictReply)
        dictReply = dict(sorted(dictReply.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}TotalMessages{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {value}" for key, value in dictReply.items())]))

        l0 = [i for i in dictReply.keys() if i not in ['Q', 'S']]
        l1 = [dictReply[key] for key in l0]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.bar(l0, l1)
        plt.title('Amount of msg per staff member')
        plt.xticks(l0, l0, rotation='vertical')
        

    if args['Daily']:

        print(f'{Fore.MAGENTA}Daily{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {value}" for key, value in dictDayMessages.items())]))

        l0 = [str(i) for i in dictDayMessages.keys()]
        l1 = dictDayMessages.values()
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.bar(l0, l1)
        plt.title('Amount msg by staff per day')
        plt.xticks(l0, l0, rotation='vertical')

    if args['ConsecutiveTime']:
        dictConsecutiveTime = await correct_dict_for_id(dictConsecutiveTime)
        dictConsecutiveTime = dict(sorted(dictConsecutiveTime.items(), key=lambda item: item[1], reverse=True))

        print(f'{Fore.MAGENTA}ConsecutiveTime{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {round(sum([i.total_seconds()/(3600) for i in value]), 2)}" for key, value in dictConsecutiveTime.items())]))

        l0 = [i for i in dictConsecutiveTime.keys()]
        l1 = [sum([i.total_seconds()/(3600) for i in dictConsecutiveTime[key]]) for key in l0]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.bar(l0, l1)
        plt.title('Total time spend in staff help in hours')
        plt.xticks(l0, l0, rotation='vertical')
    
    if args['ReplyTimes']:

        print(f'{Fore.MAGENTA}ReplyTimes{Style.RESET_ALL}:\n'+"".join([i.ljust(30) if (index + 1) % 2 != 0 else i + '\n' for index, i in enumerate(f"{key}: {round(sum([i.total_seconds()/(60) for i in value])/len(value), 2)}" for key, value in dictReplyTimes.items())]))

        l0 = [str(i) for i in dictReplyTimes.keys()]
        l1 = [sum([j.total_seconds()/60 for j in i])/len(i) for i in dictReplyTimes.values()]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.bar(l0, l1)
        plt.title(f'Avarage wait time on a question for a given hour. Ignores {args["IgnoreMessages"]} messages')
        plt.xticks(l0, l0, rotation='vertical')
    
    if args['DailyStaffMessages']:
        dictDayStaffMessages = await correct_dict_for_id(dictDayStaffMessages)

        l0 = [i for i in dictDayStaffMessages.keys()]
        l1 = [sum([j for j in value.values()])/(len([j for j in value.values()])) for value in dictDayStaffMessages.values()]
        plt.subplot(*graph_placements[current_index])
        current_index += 1
        plt.bar(l0, l1)
        plt.title(f'Avarage msg per staff on a day')
        plt.xticks(l0, l0, rotation='vertical')


    plt.subplots_adjust(left=0.1, bottom=0.15, right=0.9, top=0.9, wspace=0.2, hspace=0.75)
    plt.suptitle(f'Data from {start_date} until {last_time.date()}')

    processing_dicts_time_end = time.time()

    print(f"---Total Run Time {time.time() - total_run_time} seconds ---")
    print(f"---File Reading Time {file_reading_time_end - file_reading_time} seconds ---")
    print(f"---Making Plots Time {processing_dicts_time_end - processing_dicts_time} seconds ---")

    if args['SaveGraphs']:
        plt.savefig('out.png')

    if args['ShowGraph']:
        plt.show()

if __name__ == '__main__':
    asyncio.run(main())