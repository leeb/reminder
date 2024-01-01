from datetime import date
from . import util

class Event():
    def __init__(self, text:str, year:int, month:int, day:int=None, interval:int=None, limit:int=None):
        self.text = text
        self.year = year
        self.month = month
        self.day = day
        self.interval = interval
        self.limit = limit


    def __str__(self):
        end_str = start_str = "             "
        
        #start_str = self.start_date.strftime('%d %b %Y') if self.start_date is not None else ""
        #end_str = self.end_date.strftime('%d %b %Y') if self.end_date is not None else ""

        interval = ""
        if self.interval:
            if self.interval == 1:
                interval = "Monthly"
            elif self.interval == 12:
                interval = "Annually"
            elif self.interval % 12 == 0:
                interval = "{:2d} years".format(int(self.interval / 12))
            else:
                interval = "{:2d} months".format(self.interval)

        limit = ""
        if self.limit:
            limit = str(self.limit)

        if self.day is None:
            date_str = date(self.year, self.month, 1).strftime('-- %b %Y')
        else:
            date_str = date(self.year, self.month, self.day).strftime('%d %b %Y')

        return "{:11s} |{:>10s} | {:>5s} | {:s}".format(
            date_str, interval, limit, self.text)

