from datetime import date
import dateparser
import sqlite3
import os

from .event import Event
from . import util



class Storage():
    def __init__(self, data_dir=None, event_file="reminder.txt", db_file="reminder.db"):
        self.events = []

        if not os.path.exists(data_dir):
            os.makedirs(data_dir, mode = 0o700)

        self.event_file = os.path.join(data_dir, event_file)

        # db_path = os.path.join(data_dir, db_file)
        #print(f"creating db : {db_path}")
        #self.con = sqlite3.connect(db_path)
        #self.create_db()
        # print(f"@Storage {data_dir} {sql_db}")

    def append_event(self, event:Event):
        self.events.append(event)

    def list_events(self):
        print(util.line_break())
        print(util.header_str(show_id=True))
        print(util.line_break())
        for index, event in enumerate(self.events):
            print(f"{index + 1: 3}| ", event, sep='')
            #print(f"{index:02d}", event)


    def create_db(self):
        self.con.execute("""CREATE TABLE IF NOT EXISTS events ( 
            id INTEGER,
            start_date INTEGER NOT NULL,
            last_date INTEGER,
            months INTEGER NOT NULL,
            weeks INTEGER NOT NULL,
            PRIMARY KEY(id)                 
        );""")
        self.con.commit()


    def text_export(self, filename=None):
        if filename is None:
            filename = self.event_file

        with open(filename, "w") as textfile:
            print(util.line_break(), file=textfile)
            print(util.header_str(show_id=False), file=textfile)
            print(util.line_break(), file=textfile)

            for index, event in enumerate(self.events):
                textfile.write(str(event) + "\n")


    def text_import(self, filename=None):
        if filename is None:
            filename = self.event_file

        with open(filename, "r") as textfile:
            for line in textfile:
                if line.startswith('#'):
                    continue

                parts = line.strip().split('|')
                if len(parts) < 4:
                    continue

                start_date = util.parse_start_date(parts[0])
                interval = util.parse_interval(parts[1])
                try:
                    limit = int(parts[2])
                except ValueError:
                    limit = None

                text = parts[3].strip()
                #print(start_date, interval, limit, text)

                self.events.append(Event(text, 
                        year=start_date[0], month=start_date[1], day=start_date[2],
                        interval=interval, limit=limit))











