from datetime import datetime, timezone, timedelta
from bkb_calendar import has_events

CALENDAR_ID = 'primary'


def main():
    # logging.basicConfig(level=logging.INFO)

    # FIXME tz not hardwired, CET/CEST
    prg_tz = timezone(timedelta(hours=1))
    time_min_prg = datetime(2018, 11, 12, 7, 0, tzinfo=prg_tz)
    time_max_prg = datetime(2018, 11, 12, 18, 0, tzinfo=prg_tz)
    events = has_events(CALENDAR_ID, time_min_prg, time_max_prg)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['start'].get('date'))
        summary = event['summary']
        event_id = event['id']
        description = event.get('description')
        event_pretty = f'[{event_id}] {start} - {end}: {summary}'
        if description is not None:
            event_pretty += f' - {description}'
        print(event_pretty)


if __name__ == '__main__':
    main()
