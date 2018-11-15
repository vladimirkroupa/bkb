from datetime import datetime, timezone
from bkb_calendar import create_event
from pytz import timezone
import logging

CALENDAR_ID = 'primary'


def main():
    # logging.basicConfig(level=logging.DEBUG)
    prg_tz = timezone('Europe/Prague')
    start_time = prg_tz.localize(datetime(2018, 11, 16, 9, 0))
    end_time = prg_tz.localize(datetime(2018, 11, 16, 10, 0))
    summary = 'Fegit of the year'
    event = create_event(CALENDAR_ID, 'goobyson', start_time, end_time, summary)
    if event is not None:
        print('Event [%s] created: %s' % (event.get('id'), event.get('htmlLink')))
    else:
        print('Could not create event.')


if __name__ == '__main__':
    main()
