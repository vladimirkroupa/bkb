from datetime import datetime, timedelta
from calendar_api import events_list, events_insert, events_delete
from pytz import timezone

LOCAL_TZ = timezone('Europe/Prague')


def create_event(calendar_id, user_id, start_time, end_time, summary, description=None, loanee_email=None,
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
                'loanee_id': user_id
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


def list_all_future_loans(calendar_id):
    def has_any_loanee_id(event):
        event_loanee_id = event.get('extendedProperties', {}).get('private', {}).get('loanee_id', None)
        return bool(event_loanee_id)

    now_in_cz = LOCAL_TZ.localize(datetime.now())
    events = events_list(time_min=now_in_cz, time_max=None, calendar_id=calendar_id)
    loans = [e for e in events if has_any_loanee_id(e)]
    return loans


def list_future_loans(calendar_id, user_id):
    def has_same_loanee_id(event, loanee_id):
        event_loanee_id = event.get('extendedProperties', {}).get('private', {}).get('loanee_id', None)
        if event_loanee_id is None:
            return False
        return event_loanee_id == loanee_id

    now_in_cz = LOCAL_TZ.localize(datetime.now())
    events = events_list(time_min=now_in_cz, time_max=None, calendar_id=calendar_id)
    loans = [e for e in events if has_same_loanee_id(e, user_id)]
    return loans


def cancel_loan(calendar_id, user_id, event_id):
    user_loans = list_future_loans(calendar_id, user_id)
    loan_to_delete = [event for event in user_loans if event['id'] == event_id]
    if len(loan_to_delete) != 1:
        raise Exception(f'Loan [{event_id}] does not exist or does not belong to user {user_id}')

    events_delete(loan_to_delete[0]['id'], calendar_id)
