import os
import time
import json
import re
import pandas as pd
import tempfile
from csv import DictWriter
from csv import reader
from os import system

def clear(): system('cls')

def printChapterTime():
    print(r'''
      ______  __                      _                  
    .' ___  |[  |                    / |_                
   / .'   \_| | |--.   ,--.  _ .--. `| |-'.---.  _ .--.  
   | |        | .-. | `'_\ :[ '/'`\ \| | / /__\\[ `/'`\] 
   \ `.___.'\ | | | | // | |,| \__/ || |,| \__., | |     
    `.____ .'[___]|__]\'-;__/| ;.__/ \__/ '.__.'[___]    
   _________  _              [__|                         
  |  _   _  |(_)                            _        
  |_/ | | \_|__   _ .--..--.  .---.       ,/_\,
      | |   [  | [ `.-. .-. |/ /__\\    ,/_/ \_\,   
     _| |_   | |  | | | | | || \__.,   /_/ ___ \_\      
    |_____| [___][___||__||__]'.__.'  /_/ |(V)| \_\         
                                        |  .-.  |
                                        | / / \ |
                                        | \ \ / |
                                        |  '-'  |
                                        '--,-,--'
                                            | |
                                            | |
                                            | |
                                            /\|
                                            \/|
                                             /\
                                             \/
''')
    
def getSeconds(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

tailDotRGX = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')

def removeZeros(a):
    return tailDotRGX.sub(r'\2', a)

system("title Chapter Time -- Podcast Chapter Converter")

def main():
    finished = False
    while finished == False:
        clear()
        printChapterTime()
        print('Please choose what you would like to do:')
        choice = input('1) convert JSON chapters to CSV markers\n'
                    + '2) convert CSV markers to JSON chapters\n')
        if choice == '1':
            podAnswered = False
            while podAnswered == False:
                podcastAnswer = input('\nWhich podcast are you producing? 1) BAB 2) HGH ')
                match podcastAnswer.lower():
                    case '1' | 'bab' | 'bowl after bowl':
                        podcastAnswer = 'bab'
                        podAnswered = True
                        break
                    case '2' | 'hgh' | 'homegrown hits' | 'home grown hits':
                        podcastAnswer = 'hgh'
                        podAnswered = True
                        break
                    case _:
                        print('\nThat\'s not a valid input! How about giving it another shot?' )
                        time.sleep(2)
                        clear()
                        printChapterTime()
                        continue
            if podcastAnswer == 'bab':
                path = f'C:/Users/tiger/Desktop/Spencer/Podcasting/Bowl After Bowl/feed/chapters/'
                show = 'bab'
            else:
                path = f'C:/Users/tiger/Desktop/Spencer/Podcasting/Homegrown Hits/feed.homegrownhits.xyz/assets/chapters/'
                show = 'hgh'
            print(f'Path: {path}, show: {show}')
            epAnswered = False
            while epAnswered == False:
                episode = input('\nWhich episode are you producing? Numbers only! ')
                if re.match(r'\d{1,3}', episode) and len(episode) < 4:
                    conf = False
                    while conf == False:
                        confirm = input(f'\nYou entered "{episode}," is that correct? Y/N: ').lower()
                        if confirm == 'y' or confirm == 'yes':
                            epAnswered = True
                            conf = True
                            break
                        elif confirm == 'n' or confirm == 'no':
                            print("\nLet's try again.")
                            time.sleep(1)
                            conf = True
                            clear()
                            printChapterTime()
                            continue
                        else:
                            print("\nInvalid format. Please enter Y(es) or N(o).")
                            time.sleep(2)
                            clear()
                            printChapterTime()
                            continue
                else:
                    print("\nInvalid format. Please enter a 2-3 digit number.")
                    time.sleep(2)
                    clear()
                    printChapterTime()
                    continue
            converted = False
            while converted == False:
                if show == 'bab':
                    fullPath = path + f'episode-{episode}-chapters.json'
                    print(f'\nOpening Episode {episode} chapter file\n'
                          + f'from path: {fullPath}')
                    f = open(fullPath)
                    jsonData = json.load(f)
                    timestamps = []
                    counter = 0
                    for i in jsonData['chapters']:
                        print (i)
                        # get startTime and name of chapter
                        startTime = i['startTime']
                        chapterName = i['title']
                        # convert seconds to hh:mm:ss
                        hms = time.strftime('%H:%M:%S', time.gmtime(startTime))
                        print(f'Formatted time: {hms}')
                        time.sleep(.2)
                        # add to timestamp list
                        timestamps.append({'Name': {chapterName}, 'Start': hms, 'Duration': '0:00.000', 'Format': 'decimal', 'Type': 'Cue', 'Description': ''})
                        counter += 1
                    print(timestamps)
                    # make keys from dict list
                    keys = timestamps[0].keys()
                    with open(path + f'markers-ep-{episode}.csv', 'w', newline='') as outputFile:
                        dictWriter = DictWriter(outputFile, keys, delimiter='\t')
                        dictWriter.writeheader()
                        dictWriter.writerows(timestamps)
                    print('Markers file created. Exiting program...')
                    time.sleep(2)
                    converted = True
                    finished = True
                else:
                    fullPath = path + f'ch-episode-{episode}.json'
                    print(f'\nOpening Episode {episode} chapter file\n'
                          + f'from path: {fullPath}')
                    f = open(fullPath)
                    jsonData = json.load(f)
                    timestamps = []
                    counter = 0
                    for i in jsonData['chapters']:
                        print (i)
                        # get startTime of chapter
                        startTime = i['startTime']
                        #get chapter name
                        chapterName = i['title']
                        # convert seconds to hh:mm:ss
                        hms = time.strftime('%H:%M:%S', time.gmtime(startTime))
                        print(f'Formatted time: {hms}')
                        time.sleep(.2)
                        # add to timestamp list
                        timestamps.append({'Name': chapterName, 'Start': hms, 'Duration': '0:00.000', 'Format': 'decimal', 'Type': 'Cue', 'Description': ''})
                        counter += 1
                    print(timestamps)
                    # make keys from dict list
                    keys = timestamps[0].keys()
                    with open(path + f'markers-ep-{episode}.csv', 'w', newline='') as outputFile:
                        dictWriter = DictWriter(outputFile, keys, delimiter='\t')
                        dictWriter.writeheader()
                        dictWriter.writerows(timestamps)
                    print('Markers file created. Exiting program...')
                    time.sleep(2)
                    converted = True
                    finished = True
        elif choice == '2':
            podAnswered = False
            while podAnswered == False:
                podcastAnswer = input('\nWhich podcast are you producing? 1) BAB 2) HGH ')
                match podcastAnswer.lower():
                    case '1' | 'bab' | 'bowl after bowl':
                        podcastAnswer = 'bab'
                        podAnswered = True
                        break
                    case '2' | 'hgh' | 'homegrown hits' | 'home grown hits':
                        podcastAnswer = 'hgh'
                        podAnswered = True
                        break
                    case _:
                        print('\nThat\'s not a valid input! How about giving it another shot?' )
                        time.sleep(2)
                        clear()
                        printChapterTime()
                        continue
            if podcastAnswer == 'bab':
                path = f'C:/Users/tiger/Desktop/Spencer/Podcasting/Bowl After Bowl/feed/chapters/'
                show = 'bab'
            else:
                path = f'C:/Users/tiger/Desktop/Spencer/Podcasting/Homegrown Hits/feed.homegrownhits.xyz/assets/chapters/'
                show = 'hgh'
            print(f'Path: {path}, show: {show}')
            epAnswered = False
            while epAnswered == False:
                episode = input('\nWhich episode are you producing? Numbers only! ')
                if re.match(r'\d{1,3}', episode) and len(episode) < 4:
                    conf = False
                    while conf == False:
                        confirm = input(f'\nYou entered "{episode}," is that correct? Y/N: ').lower()
                        if confirm == 'y' or confirm == 'yes':
                            clear()
                            printChapterTime()
                            epAnswered = True
                            conf = True
                            break
                        elif confirm == 'n' or confirm == 'no':
                            print("\nLet's try again.")
                            time.sleep(1)
                            conf = True
                            clear()
                            printChapterTime()
                            continue
                        else:
                            print("\nInvalid format. Please enter Y(es) or N(o).")
                            time.sleep(2)
                            clear()
                            printChapterTime()
                            continue
                else:
                    print("\nInvalid format. Please enter a 2-3 digit number.")
                    time.sleep(2)
                    clear()
                    printChapterTime()
                    continue
            converted = False
            while converted == False:
                if show == 'bab':
                    fullPath = path + f'markers-ep-{episode}.csv'
                    print(f'\nOpening Episode {episode} markers file\n'
                          + f'from path: {fullPath}')
                    f = open(fullPath)
                    csvReader = reader(f)
                    timestamps = []
                    counter = 0
                    for i in csvReader:
                        #skip first loop
                        if counter > 0:
                            # get start time
                            list = i[0].split('\t')
                            startTime = list[1]
                            ogTime = startTime
                            # remove ms from time
                            ms = startTime.split('.')[1]
                            startTime = startTime.split('.')[0]
                            if len(startTime.split(':')) < 3:
                                startTime = '0:' + startTime
                            # convert hh:mm:ss to seconds
                            seconds = getSeconds(startTime)
                            if ms != '000':
                                seconds = str(seconds) + '.' + ms
                            else:
                                seconds = str(seconds)
                            seconds = float(removeZeros(seconds))
                            if seconds == 0.0:
                                seconds = 0.001
                            # add to timestamp list
                            print(f'Marker {counter}: {ogTime} => {seconds} seconds')
                            time.sleep(.2)
                            timestamps.append(seconds)
                            timestamps.sort()
                        counter += 1
                    print(f'timestamps: {timestamps}')
                    # open json chapters file
                    with open(path + f'episode-{episode}-chapters.json', 'r+') as jsonFile:
                        jsonChapters = json.load(jsonFile)
                        counter = 0
                        for i in jsonChapters['chapters']:
                            oldTime = i['startTime']
                            # update timestamp
                            print(f"timestamps[counter]: {timestamps[counter]}")
                            i['startTime'] = timestamps[counter]
                            print(f'Old time: {oldTime} ==> New time: {i['startTime']}')
                            time.sleep(.25)

                            counter += 1
                        jsonFile.seek(0)
                        jsonFile.write(json.dumps(jsonChapters))
                        jsonFile.truncate()
                        print('Chapters file updated. Exiting program...')
                        time.sleep(2)
                        converted = True
                        finished = True
        else:
            print('\nInvalid selection, try again!')
            time.sleep(2)
            clear()
            printChapterTime()
            continue

if __name__ == '__main__':
    main()