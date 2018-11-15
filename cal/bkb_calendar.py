from datetime import datetime, timedelta
from calendar_api import events_list, events_insert
from pytz import timezone

LOCAL_TZ = timezone('Europe/Amsterdam')


def create_event(calendar_id, loanee_id, start_time, end_time, summary, description=None, loanee_email=None,
                 loanee_name=None,
                 location=None):
    existing_events = list_events(calendar_id, start_time, end_time)
    if len(existing_events) > 0:
        # FIXME log?
        return None

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat()
        },
        'end': {
            'dateTime': end_time.isoformat()
        },
        'extendedProperties': {
            'private': {
                'loanee_id': loanee_id
            }
        }
    }
    if description is not None:
        event['description'] = description

    if location is not None:
        event['location'] = location

    if loanee_email is not None:
        loanee = {'email': loanee_email}
        if loanee_name is not None:
            loanee['displayName'] = loanee_name
        event['atendees'] = [loanee]

    return events_insert(event, calendar_id)


def list_events(calendar_id, time_min, time_max):
    one_minute = timedelta(minutes=1)
    time_min = time_min + one_minute
    time_max = time_max - one_minute
    return events_list(time_min, time_max, calendar_id)


def list_all_future_loans(calendar_id, loanee_id):
    def event_has_loanee_id(event, loanee_id):
        event_loanee_id = event.get('extendedProperties', {}).get('private', {}).get('loanee_id', {})
        if event_loanee_id is None:
            return False
        return event_loanee_id == loanee_id

    now_in_cz = LOCAL_TZ.localize(datetime.now())
    events = events_list(time_min=now_in_cz, time_max=None, calendar_id=calendar_id)
    loanee_events = [e for e in events if event_has_loanee_id(e, loanee_id)]
    return loanee_events
