import os
import logging
import platformdirs
from datetime import date, timedelta
from configparser import ConfigParser
import calendar
import math

from .storage import Storage
from . import util

logger = logging.getLogger(__name__)

appname = "reminder"
appauthor = "leeb.dev"


class Reminder():
    def __init__(self):
        config_dir = platformdirs.user_config_dir(appname, appauthor)

        if not os.path.exists(config_dir):
            os.makedirs(config_dir, mode = 0o700)

        self.__config_path = os.path.join(config_dir, "config.ini")

        self.config = ConfigParser()
        self.config['storage'] = { 
            'data_dir': platformdirs.user_data_dir(appname, appauthor),
            'event_file': 'reminder.txt',
            'db_file': 'reminder.db'
        }

        # load the config if it exists, save it if it doesn't.
        if os.path.isfile(self.__config_path):
            self.read_config()
        else:
            self.write_config()

        self.storage = Storage(**self.config['storage'])
        self.storage.text_import()


    def read_config(self):
        self.config.read(self.__config_path)


    def write_config(self):
        with open(self.__config_path, 'w') as configfile:
            self.config.write(configfile)
        

    def summary(self, today=None, past=31, future=31):
        if today == None:
            today = date.today()

        start = today - timedelta(days = past)
        end = today + timedelta(days = future)

        today_months = (today.year * 12) + today.month - 1
        start_months = today_months - int(math.ceil(past / 31))
        end_months = today_months + int(math.ceil(past / 31))

        print(util.line_break())
        print("#ID |     Date    | Description")
        ##print("--------------------------------------------------------------------")
        print(util.line_break())


        #print("This is the summary")
        #print(f"today: {today_months} from: {start_months} to: {end_months}")
        
        result = {}

        # sort events by their proximity to the target date
        index = 0
        for event in self.storage.events:
            index += 1
            evt_months = (event.year * 12) + event.month - 1
            rep = 0

            #print(f"events months; {evt_months} interval {event.interval} limit {event.limit}: {event.text}")    

            if start_months > evt_months and event.interval:
                rep = int((start_months - evt_months) / event.interval)
                evt_months += (rep * event.interval)
                #print(f"events months; {evt_months} interval {event.interval} limit {event.limit}: {event.text}")    
                #print(f"diff: {rep} {evt_months}")

            t = 100 # limit number of iterations while debugging
            while t:
                t -= 1

                if event.limit and rep >= event.limit:
                    #print("limit exceeded")
                    break

                if evt_months > end_months:
                    #print(f"evt_months out of range {evt_months} {end_months}")
                    break

                
                if event.day is None:                   # whole month events
                    if evt_months >= start_months:
                        year = int(evt_months / 12)
                        month = (evt_months % 12) + 1
                        key = f"{year:04d}{month:02d}00"
                        result[key] = { 
                            'date': (year, month),
                            'delta': int(evt_months - today_months),
                            'event': event,
                            'index': index }
                        #print(f" match {year}-{month:02d}    {event.text}")

                else:
                    if evt_months >= start_months:
                        year = int(evt_months / 12)
                        month = (evt_months % 12) + 1
                        maxday = calendar.monthrange(year, month)[1]
                        day = event.day if event.day <= maxday else maxday
                        key = f"{year:04d}{month:02d}{day:02d}"
                        result[key] = { 
                            'date': (year, month, day),
                            'delta': int(evt_months - today_months),
                            'event': event, 
                            'index': index }
                        #print(f" match {year}-{month:02d}-{day:02d} {event.text}")
                        
                evt_months += event.interval
                rep += 1

        for key, item in sorted(result.items()):
            color = "\033[37m"
            if item['delta'] > 0:
                color = "\033[32m"
            elif item['delta'] < 0:
                color = "\033[90m"

            if len(item['date']) == 2:
                date_str = date(item['date'][0], item['date'][1], 1).strftime('-- %b %Y')
            else:                
                date_str = date(item['date'][0], item['date'][1], item['date'][2]).strftime('%d %b %Y')
                if item['delta'] == 0:
                    if item['date'][2] > today.day:
                        color = "\033[32m"
                    elif item['date'][2] < today.day:
                        color = "\033[90m"
                    
            print(color, f'{item["index"]:3d}', ' | ', date_str, ' | ', item['event'].text, sep='')
        
        print('\033[37m', end='')


    def count_events(self):
        return len(self.storage.events)

    def list_events(self):
        self.storage.list_events()







