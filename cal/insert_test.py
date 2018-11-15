from datetime import datetime, timezone
from bkb_calendar import create_event
from pytz import timezone

CALENDAR_ID = 'primary'


def main():
    # logging.basicConfig(level=logging.DEBUG)
    prg_tz = timezone('Europe/Prague')
    start_time = datetime(2018, 11, 16, 7, 0, tzinfo=prg_tz)
    end_time = datetime(2018, 11, 16, 8, 0, tzinfo=prg_tz)
    summary = 'Fegit of the year'
    event = create_event(CALENDAR_ID, '123456', start_time, end_time, summary)
    if event is not None:
        print('Event created: %s' % (event.get('htmlLink')))
    else:
        print('Could not create event.')


if __name__ == '__main__':
    main()
