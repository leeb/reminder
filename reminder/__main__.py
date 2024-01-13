from importlib import metadata
from argparse import ArgumentParser, ArgumentTypeError, REMAINDER
from datetime import date
import dateparser
import logging

from .reminder import Reminder
from .storage import Event
from . import util

logger = logging.getLogger(__name__)


def valid_start_date(input):
    start_date = util.parse_start_date(input)
    if start_date == None:
        raise ArgumentTypeError("Not a valid date")
    return start_date


def valid_end_date(input):
    end_date = util.parse_end_date(input)
    if end_date == None:
        raise ArgumentTypeError("Not a valid date")
    return end_date


def valid_interval(input):
    interval = util.parse_interval(input)
    if interval == 0:        
        raise ArgumentTypeError("Not a valid interval")
    return interval


def main():
    parser = ArgumentParser(description="Remind me because I forget.")

    parser.add_argument('-v', '--version', action="store_true",
        help="Show application version")

    loglevel_group = parser.add_mutually_exclusive_group()

    loglevel_group.add_argument('--info',
        action="store_const", dest="loglevel", const=logging.INFO, default=logging.WARNING,
        help="Show information messages (loglevel=INFO)")

    loglevel_group.add_argument('-d', '--debug',
        action="store_const", dest="loglevel", const=logging.DEBUG,
        help="Show debug and information messages (loglevel=DEBUG)")

    subparsers = parser.add_subparsers(title=None, dest="command", help="", metavar="Event commands")

    parser_list = subparsers.add_parser('summary', help="Summary of immediate reminders")

    parser_list = subparsers.add_parser('list', aliases=['ls'], help="List events")
    parser_list.set_defaults(command="list")

    parser_remove = subparsers.add_parser('remove', aliases=['rm'], help="Remove event")
    parser_remove.set_defaults(command="remove")
    parser_remove.add_argument('id', type=int, help="event id")

    parser_create = subparsers.add_parser('create', aliases=['add'], help="Add new event")
    parser_create.set_defaults(command="create")
    parser_create.add_argument('--startdate', '-s', type=valid_start_date, help="Start date")
    parser_create.add_argument('--interval', '-i', type=valid_interval, help="repeat interval")
    parser_create.add_argument('--limit', '-l', type=int, help="repeat interval")
    parser_create.add_argument('description', nargs='?', help="description")

    parser_edit = subparsers.add_parser('edit', help="Open event file with default editor.")

    parser_list = subparsers.add_parser('help', help="Show help message")

    args = parser.parse_args()

    #print(args)

    logging.basicConfig(level=args.loglevel)  # debug, info, warning, error, critical
    logging.info(f"loglevel {args.loglevel}")

    if args.version:
        print(f"Version: {metadata.version('reminder')}")
        return
    
    reminder = Reminder()
    # reminder.read_config()
    # reminder.write_config()

    if args.command == 'summary' or args.command == None:
        reminder.summary()

    elif args.command == 'help':
        parser.print_help()

    elif args.command == 'create':

        while args.startdate is None:
            try:
                args.startdate = valid_start_date(input("Start date: "))
                break
            except ArgumentTypeError:
                pass
            
        if args.interval is None:
            try:
                args.interval = valid_interval(input("Repeating interval (return for none): "))
            except ArgumentTypeError:
                pass

        if args.limit is None:
            try:
                args.limit = int(input("Limit maximium occurances (return for none): "))
            except ValueError:
                pass

        if args.description is None:
            args.description = input("Event description: ")

        #print(f"Creating event: \"{args.description}\"")
        #print(f'Starting from {args.startdate:%a %d %b %Y} until ')
        #if args.interval:
        #    print(f'Repeating {args.interval}')

        #print(f"start date: {args.startdate}")
        #print(f"end date: {args.enddate}")
        #print(f"interval: {args.interval}")
        #print(f"description: {args.description}")
            
        evt = Event(args.description, 
                    year=args.startdate[0], month=args.startdate[1], day=args.startdate[2],                    
                    interval=args.interval, limit=args.limit)

        print(util.line_break())
        print(util.header_str(show_id=False))
        print(util.line_break())
        print(evt)
        print("")

        while True:
            confirm = input("Confirm (Y/n): ").strip()
            if confirm == 'Y' or confirm == "":                                
                print("Saved.")
                reminder.storage.append_event(evt)
                reminder.storage.text_export()
                break
            if confirm == 'n':
                print("Cancelled.")
                break

    elif args.command == 'remove':
        id = args.id
        max_id = reminder.count_events()
        if id <= 0:
            print("Error: Out of range, [id] must be greater than 0")            
            return
        if id > max_id:
            print(f"Error: Out of range, [id] must be less than or equal to {max_id}")
            return

        print(f"Removing id {id}")
        reminder.storage.remove_event(id - 1)
        reminder.storage.text_export()


    elif args.command == 'list':
        reminder.list_events()

    elif args.command == 'edit':
        reminder.edit_events()

    #logger.debug("This is a debug messages")


if __name__ == "__main__":
    main()