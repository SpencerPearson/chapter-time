import os
import time
import json
import re
import pandas as pd
from csv import DictWriter
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
                    confirm = input(f'\nYou entered "{episode}," is that correct? Y/N: ').lower()
                    conf = False
                    while conf == False:
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
                    chapterNames = ['intro', 'v4v', 'on chain', 'top 3 33', 'btc', 'mm', 'fite', 'fidlgb', 'outro']
                    counter = 0
                    for i in jsonData['chapters']:
                        print (i)
                        # get startTime of chapter
                        startTime = i['startTime']
                        # convert seconds to hh:mm:ss
                        hms = time.strftime('%H:%M:%S', time.gmtime(startTime))
                        print(f'Formatted time: {hms}')
                        time.sleep(.2)
                        # add to timestamp list
                        timestamps.append({'Name': chapterNames[counter], 'Start': hms, 'Duration': '0:00.000', 'Format': 'decimal', 'Type': 'Cue', 'Description': ''})
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
                    chapters = open(path + f'ch-episode-{episode}.json')
                    data = json.load(chapters)
                    for i in data:
                        print (i)
        elif choice == '2':
            print('CSV to JSON coming soon')
        else:
            print('\nInvalid selection, try again!')
            time.sleep(2)
            clear()
            printChapterTime()
            continue

if __name__ == '__main__':
    main()