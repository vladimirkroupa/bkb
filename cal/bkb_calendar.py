from datetime import timedelta
from calendar_api import events_list, events_insert


def create_event(calendar_id, start_time, end_time, summary, description=None, loanee_email=None, loanee_name=None,
                 location=None):
    existing_events = has_events(calendar_id, start_time, end_time)
    if len(existing_events) > 0:
        # FIXME log?
        return None

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat()
        },
        'end': {
            'dateTime': end_time.isoformat()
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


def has_events(calendar_id, time_min, time_max):
    one_minute = timedelta(minutes=1)
    time_min = time_min + one_minute
    time_max = time_max - one_minute
    return events_list(time_min, time_max, calendar_id)
