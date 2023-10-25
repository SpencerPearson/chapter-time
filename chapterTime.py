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
def printWolf():
    print(r'''
                                        __
                            .d$$b
                          .' TO$;\     AWWWWOOOOOO"
                         /  : TP._;
                        / _.;  :Tb|           SIR SPENCER, WOLF OF KANSAS CITY SAYS:
                       /   /   ;j$j
                   _.-'       d$$$$           THANKS FOR USING CHAPTER TIME!
                 .' ..       d$$$$;           THIS IS VALUE FOR VALUE SOFTWARE!
                /  / P'      d$$$$P. |\       IF YOU RECEIVED VALUE FROM USING
               / '      .d$$$P' |\^'l         THIS PROGRAM, CONSIDER RETURNING
             .'           `T$P^''"''  :       EQUIVALENT VALUE IN ONE OF THE
         ._.'      _.'                ;       FOLLOWING WAYS:
      `-.- '.-'-' ._.       _.-'.-''
    `.-' _____  ._              .-'           - SHARE CHAPTER TIME WITH A FRIEND
   - (.g$$$$$$$b.              .'             - BOOST THE BOWL AFTER BOWL PODCAST
     '' ^^ T$$$P ^)            .(:            - SEND SATS TO ONE OF THESE LN ADDRESSES:
          _ / -'  /.'         /:/;                  sirspencer@fountain.fm
       ._.'-'`-'  ')/         /;/;                  sirspencer@getalby.com
 `-.- '..--''   ' /         /  ;              
.-' ..--''        -'          :               GOT AN IDEA TO MAKE IT BETTER? SUBMIT A
..--''--.- '         (\      .-(\             PR TO THE PROJECT HERE:
  ..--''              `-\(\/;`                https://github.com/SpencerPearson/chapter-time
    _.                      :                 
                            ;`-               TOOT ME ON MASTODON: @SirSpencer@noagendasocial.com
                        :\                    EMAIL ME: spencer@bowlafterbowl.com
                           ; 
          ''')
    
def getSeconds(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

tailDotRGX = re.compile(r'(?:(\.)|(\.\d*?[1-9]\d*?))0+(?=\b|[^0-9])')

def removeZeros(a):
    return tailDotRGX.sub(r'\2', a)

def getFileNameFormat(show, episode):
    if show == 'bab':
        return f'episode-{episode}-chapters.json'
    else:
        return f'ch-episode-{episode}.json'
    
def getShowPath(show):
    if show == 'bab':
        return 'C:/Users/tiger/Desktop/Spencer/Podcasting/Bowl After Bowl/feed/chapters/'
    else:
        return 'C:/Users/tiger/Desktop/Spencer/Podcasting/Homegrown Hits/feed.homegrownhits.xyz/assets/chapters/'

system("title Chapter Time -- Podcast Chapter Converter")

def main():
    finished = False
    while finished == False:
        clear()
        printChapterTime()
        print('Please choose what you would like to do:')
        choice = input('1) convert JSON chapters to CSV markers\n'
                    + '2) convert CSV markers to JSON chapters\n'
                    + '3) see Value For Value info\n\n'
                    + 'Selection: ')
        if choice == '1':
            podAnswered = False
            while podAnswered == False:
                podcastAnswer = input('\nWhich podcast are you producing? 1) BAB 2) HGH ')
                match podcastAnswer.lower():
                    case '1' | 'bab' | 'bowl after bowl':
                        show = 'bab'
                        podAnswered = True
                        break
                    case '2' | 'hgh' | 'homegrown hits' | 'home grown hits':
                        show = 'hgh'
                        podAnswered = True
                        break
                    case _:
                        print('\nThat\'s not a valid input! How about giving it another shot?' )
                        time.sleep(2)
                        clear()
                        printChapterTime()
                        continue
            path = getShowPath(show)
            print(f'Path: {path}, show: {show}')
            epAnswered = False
            while epAnswered == False:
                episode = input('\nWhich episode are you producing? Numbers only! ')
                if re.match(r'\d{1,3}', episode) and len(episode) < 4:
                    conf = False
                    while conf == False:
                        confirm = input(f'\nYou entered "{episode}," is that correct? Y/N: ').lower()
                        if confirm == 'y' or confirm == 'yes' or confirm == '1':
                            clear()
                            printChapterTime()
                            epAnswered = True
                            conf = True
                            break
                        elif confirm == 'n' or confirm == 'no' or confirm == '2':
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
                fileName = getFileNameFormat(show, episode)
                fullPath = path + fileName
                print(f'\nOpening Episode {episode} chapter file\n'
                        + f'from path: {fullPath}')
                f = open(fullPath)
                jsonData = json.load(f)
                timestamps = []
                counter = 0
                print(f'Converting Episode {episode} chapters to timestamps...')
                for i in jsonData['chapters']:
                    # get startTime and name of chapter
                    startTime = i['startTime']
                    chapterName = i['title']
                    # remove any commas in chapterName
                    if ',' in chapterName:
                        chapterName = chapterName.replace(',', '')
                    # convert seconds to hh:mm:ss
                    hms = time.strftime('%H:%M:%S', time.gmtime(startTime))
                    print(f'Chapter {counter + 1}: {chapterName}\nJSON seconds: {startTime}\nFormatted time: {hms}')
                    print('------------------------------------------------------')
                    time.sleep(.2)
                    # add to timestamp list
                    timestamps.append({'Name': chapterName, 'Start': hms, 'Duration': '0:00.000', 'Format': 'decimal', 'Type': 'Cue', 'Description': ''})
                    counter += 1
                confStamps = input('Review formatted times above. Does that look right?'
                                       + f'\n(Y)es to save changes to {fileName}, (N)o to cancel.' 
                                       + '\n(Y)es/(N)o: ').lower()
                if confStamps == 'y' or confStamps == 'yes' or confStamps == '1':
                    clear()
                    printChapterTime()
                    # make keys from dict list
                    keys = timestamps[0].keys()
                    with open(path + f'markers-ep-{episode}.csv', 'w', newline='') as outputFile:
                        dictWriter = DictWriter(outputFile, keys, delimiter='\t')
                        dictWriter.writeheader()
                        dictWriter.writerows(timestamps)
                    input('Markers file created! Press Enter to continue...')
                    keepGoin = input('Are you all finished?\nEnter (Y)es to exit, or anything else to return to main menu.')
                    converted = True
                    if keepGoin == 'yes' or keepGoin == 'y' or keepGoin == '1':
                        clear()
                        printWolf()
                        input('Press Enter to exit Chapter Time...')
                        finished = True
                else:
                    clear()
                    printChapterTime()
                    print(f'Changes discarded. Please check that your {fileName} timestamps are correct before trying again.')
                    input('Press Enter to continue...')
                    clear()
                    printChapterTime()
                    keepGoin = input('Are you all finished?\nEnter (Y)es to exit, or anything else to return to main menu.')
                    converted = True
                    if keepGoin == 'yes' or keepGoin == 'y' or  keepGoin == '1':
                        clear()
                        printWolf()
                        input('Press Enter to exit Chapter Time...')
                        finished = True
        elif choice == '2':
            podAnswered = False
            while podAnswered == False:
                podcastAnswer = input('\nWhich podcast are you producing? 1) BAB 2) HGH ')
                match podcastAnswer.lower():
                    case '1' | 'bab' | 'bowl after bowl':
                        show = 'bab'
                        podAnswered = True
                        break
                    case '2' | 'hgh' | 'homegrown hits' | 'home grown hits':
                        show = 'hgh'
                        podAnswered = True
                        break
                    case _:
                        print('\nThat\'s not a valid input! How about giving it another shot?' )
                        time.sleep(2)
                        clear()
                        printChapterTime()
                        continue
            path = getShowPath(show)
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
                fullPath = path + f'markers-ep-{episode}.csv'
                print(f'\nOpening Episode {episode} markers file\n'
                        + f'from path: {fullPath}')
                f = open(fullPath)
                csvReader = reader(f)
                timestamps = []
                counter = 0
                print(f'Converting Episode {episode} timestamps to seconds...')
                for i in csvReader:
                    #skip first loop
                    if counter > 0:
                        # get start time
                        list = i[0].split('\t')
                        startTime = list[1]
                        ogTime = startTime
                        # remove ms from time
                        if len(startTime.split('.')) > 1:
                            ms = startTime.split('.')[1]
                        else:
                            ms = None
                        startTime = startTime.split('.')[0]
                        if len(startTime.split(':')) < 3:
                            startTime = '0:' + startTime
                        # convert hh:mm:ss to seconds
                        seconds = getSeconds(startTime)
                        if ms != None:
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
                print(f'timestamps converted! Here are your timestamps:')
                print(timestamps)
                input('Press enter to continue...')
                clear()
                printChapterTime()
                # open json chapters file
                fileName = getFileNameFormat(show, episode)
                with open(path + fileName, 'r+') as jsonFile:
                    jsonChapters = json.load(jsonFile)
                    counter = 0
                    print(f'Replacing old chapter times with new timestamps...')
                    for i in jsonChapters['chapters']:
                        oldTime = i['startTime']
                        # update timestamp
                        i['startTime'] = timestamps[counter]
                        print(f'Chapter {counter}: {i['title']}\nOld time: {oldTime} ==> New time: {i['startTime']}')
                        print('-------------------------------------------')
                        time.sleep(.25)

                        counter += 1
                    confStamps = input('Review timestamps above. Does that look right?'
                                       + f'\n(Y)es to save changes to {fileName}, (N)o to cancel.' 
                                       + '\n(Y)es/(N)o: ').lower()
                    if confStamps == 'y' or confStamps == 'yes' or confStamps == '1':
                        clear()
                        printChapterTime()
                        jsonFile.seek(0)
                        jsonFile.write(json.dumps(jsonChapters))
                        jsonFile.truncate()
                        print(f'Chapters file updated! Changes to {fileName} saved!')
                        time.sleep(2)
                        converted = True
                    else:
                        clear()
                        printChapterTime()
                        print(f'Changes discarded. Please check that your {fileName} timestamps are correct before trying again.')
                        input('Press Enter to continue...')
                        converted = True
                    keepGoin = input('Are you all finished?\nEnter (Y)es to exit, or anything else to return to main menu.')
                    if keepGoin == 'yes' or keepGoin == 'y' or keepGoin == '1':
                        clear()
                        printWolf()
                        input('Press Enter to exit Chapter Time...')
                        finished = True

        elif choice == '3':
            clear()
            printWolf()
            input('Press Enter to return to the menu...')

        else:
            print('\nInvalid selection, try again!')
            time.sleep(2)
            clear()
            printChapterTime()
            continue

if __name__ == '__main__':
    main()