from init import on_start, ARGUMENT_EXPLAIN
import matplotlib.pyplot as plt
from datetime import datetime
from colorama import Fore, Style
import csv

args, FileName = on_start()

if args['ShowExplanation']:
    print("\n\n".join([ARGUMENT_EXPLAIN[key] for key in args.keys() if args[key]]))
    print('==================================================\n')

if args['TotalMessages']:
    dictReply = {"Q": 0,
                 "S": 0
                }

if args['Daily']:
    dictDayMessages = {}

if args['ConsecutiveTime']:
    dictConsecutiveTime = {}

with open(FileName, 'r') as f:
    reader = csv.reader(f)

    first_row = next(reader)
    start_time = datetime.strptime(first_row[0], '%Y-%m-%d %H:%M:%S.%f')
    last_time = 0

    if args['Daily']:
        current_day = start_time.date()
        current_day_count = 0
    
    if args['ConsecutiveTime']:
        current_staff = 0
        current_count = 0
        current_time = start_time
        interruptions = 5
        

    for row in [first_row] + list(reader):
        last_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')

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
            if current_day == datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').date():
                if row[1] != 'non staff replied':
                    current_day_count += 1
            else:
                dictDayMessages[current_day] = current_day_count
                current_day_count = 0
                current_day = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').date()
        
        if args['ConsecutiveTime']:
            if row[1] != 'non staff replied':
                if row[1] != current_staff:
                    if current_count > 5:
                        if interruptions == 5:
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

amount_of_graphs = sum([1 for key, value in args.items() if value and key not in ["SaveGraphs", "ShowExplanation", "ShowGraph"]])

graph_placements = [((amount_of_graphs + 1)//2, 2, i + 1) for i in range(amount_of_graphs)]
current_index = 0

print(f'Data from {start_time.date()} until {last_time.date()}')

if args['TotalMessages']:

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
    l0 = [i for i in dictConsecutiveTime.keys()]
    l1 = [sum([i.total_seconds()/(3600) for i in dictConsecutiveTime[key]]) for key in l0]
    plt.subplot(*graph_placements[current_index])
    current_index += 1
    plt.bar(l0, l1)
    plt.title('Total time spend in staff help in hours')
    plt.xticks(l0, l0, rotation='vertical')

plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=1)
plt.suptitle(f'Data from {start_time.date()} until {last_time.date()}')

if args['SaveGraphs']:
    plt.savefig('out.png')

if args['ShowGraph']:
    plt.show()
