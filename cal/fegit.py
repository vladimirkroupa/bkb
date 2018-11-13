from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import timezone, timedelta
from pytz import utc

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
store = file.Storage('token.json')

def build_calendar_service(cred_storage):
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service

def has_events_in_tz(time_min_local, time_max_local, calendar_id):
    time_min_utc = time_min_local.astimezone(utc)
    time_max_utc = time_max_local.astimezone(utc)
    return has_events(time_min_utc, time_max_utc, calendar_id)

def has_events(time_min_utc, time_max_utc, calendar_id):
    one_minute = datetime.timedelta(minutes=1)
    time_min = time_min_utc + one_minute
    time_max = time_max_utc - one_minute
    return events_list(time_min, time_max, calendar_id)

def events_list(time_min_utc, time_max_utc, calendar_id):
    service = build_calendar_service(store)
    time_max_iso = time_max_utc.isoformat()
    time_min_iso = time_min_utc.isoformat()
    print("timeMin utc:", time_min_iso)
    print("timeMax utc:", time_max_iso)
    events_result = service.events().list(calendarId=calendar_id,
					timeMax=time_max_iso,
					timeMin=time_min_iso,
                                        maxResults=10, 
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events
 

def main():
    prg_tz = timezone(timedelta(hours=1))
    # is available between 17 - 18?
    time_min_prg = datetime.datetime(2018, 11, 12, 17, 0, tzinfo=prg_tz)
    time_max_prg = datetime.datetime(2018, 11, 12, 18, 0, tzinfo=prg_tz)
    events = has_events_in_tz(time_min_prg, time_max_prg, 'primary')

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()

