from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import logging

log = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.events'

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
store = file.Storage('token.json')


def build_calendar_service(cred_storage):
    creds = cred_storage.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, cred_storage)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service


def events_list(time_min, time_max, calendar_id):
    service = build_calendar_service(store)
    time_min_iso = time_min.isoformat()
    time_max_iso = time_max.isoformat()
    log.warn('timeMin utc: %s', time_min_iso)
    log.warn('timeMax utc: %s', time_max_iso)
    events_result = service.events().list(calendarId=calendar_id,
                                          timeMax=time_max_iso,
                                          timeMin=time_min_iso,
                                          maxResults=10,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def events_insert(event, calendar_id):
    service = build_calendar_service(store)
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event

# TODO event as a namedtuple
