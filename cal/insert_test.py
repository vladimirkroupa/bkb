from datetime import datetime, timezone, timedelta
from bkb_calendar import create_event

CALENDAR_ID = 'primary'


def main():
    prg_tz = timezone(timedelta(hours=1))
    start_time = datetime(2018, 11, 14, 7, 0, tzinfo=prg_tz)
    end_time = datetime(2018, 11, 14, 8, 0, tzinfo=prg_tz)
    summary = 'Fegit of the year'
    event = create_event(CALENDAR_ID, str(start_time.isoformat()), str(end_time.isoformat()), summary)
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
