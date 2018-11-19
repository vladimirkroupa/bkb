from bkb_calendar import list_all_future_loans, list_future_loans

CALENDAR_ID = 'primary'


def main():
    events = list_future_loans(CALENDAR_ID, 'goobyson')

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
