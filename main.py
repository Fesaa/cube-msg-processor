from init import on_start, ALLOWED_ARGUMENTS, DEFAULT_ARGUMENTS
import matplotlib.pyplot as plt
from datetime import datetime
import csv

args, FileName = on_start()

if args['TotalMessages']:
    dictReply = {"Q": 0,
                 "S": 0
                }
if args['DailyAvarage']:
    dictDayMessages = {}

if args['ConsecutiveTime']:
    dictConsecutiveTime = {}

with open(FileName, 'r') as f:
    reader = csv.reader(f)

    first_row = next(reader)
    start_time = datetime.strptime(first_row[0], '%Y-%m-%d %H:%M:%S.%f')

    if args['DailyAvarage']:
        current_day = start_time.date()
        current_day_count = 0
    
    if args['ConsecutiveTime']:
        current_staff = 0
        current_count = 0
        current_time = start_time
        interuptions = 5
        

    for row in [first_row] + list(reader):

        if args['TotalMessages']:
            if row[1] == 'non staff replied':
                dictReply['Q'] += 1
            else:
                dictReply['S'] += 1
                if row[1] in dictReply:
                    dictReply[row[1]] += 1
                else:
                    dictReply[row[1]] = 1

        if args['DailyAvarage']:
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
                    if current_count > 10:
                        if interuptions == 5:
                            if current_staff in dictConsecutiveTime:
                                dictConsecutiveTime[current_staff].append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f') - current_time)
                            else:
                                dictConsecutiveTime[current_staff] = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f') - current_time]
                            current_staff, interuptions,  = row[1], 0
                        else:
                            interuptions += 1
                    else:
                        current_staff, current_count, current_time = row[1], 1, datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
                else:
                    current_count += 1




    
    if args['TotalMessages']:
        print(dictReply)
    if args['DailyAvarage']:
        print(dictDayMessages)
    if args['ConsecutiveTime']:
        print(dictConsecutiveTime)


