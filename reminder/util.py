import dateparser
import re


def line_break():
    return "#-------------------------------------------------------------------"


def header_str(show_id=False):
    hdr = "   From    |  Interval | Limit | Description"
    if show_id:
        return "#ID|  " + hdr
    else:
        return "#" + hdr


def parse_start_date(input):
    date1 = dateparser.parse(input, settings={
        'PREFER_DAY_OF_MONTH': 'first',
        'PREFER_MONTH_OF_YEAR': 'first'
    })
    date2 = dateparser.parse(input, settings={
        'PREFER_DAY_OF_MONTH': 'last',
        'PREFER_MONTH_OF_YEAR': 'last'
    })
    if date1 is None or date2 is None:
        return None

    if date1.day != date2.day:
        return (date1.year, date1.month, None)
    
    return (date1.year, date1.month, date1.day)


def parse_end_date(input):
    end_date = dateparser.parse(input, settings={
        'PREFER_DAY_OF_MONTH': 'last',
        'PREFER_MONTH_OF_YEAR': 'last'
    })
    return end_date.date() if end_date is not None else None;


def parse_interval(input):
    str = input.strip().lower()
    #days = 0
    months = 0

    #if str == 'weekly':
    #    days = 7

    if str == 'monthly':
        months = 1

    elif str == 'yearly':
        months = 12

    elif str == 'annually':
        months = 12

    #elif match := re.search(r'(?P<days>[-+]?\d+) day', str):
    #    days =  int(match['days'])

    #elif match := re.search(r'(?P<weeks>[-+]?\d+) week', str):
    #    days =  int(match['weeks']) * 7

    elif match := re.search(r'(?P<months>[-+]?\d+) month', str):
        months =  int(match['months'])

    elif match := re.search(r'(?P<years>[-+]?\d+) year', str):
        months =  int(match['years']) * 12

    # print(f"days {days}, months {months}")

    return months