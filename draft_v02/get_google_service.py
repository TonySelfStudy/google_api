# Created by Tony Held 02-23-21

# Source 1: https://www.youtube.com/watch?v=Z5G0luBohCg&list=PLOU2XLYxmsILOIxBRPPhgYbuSslr50KVq&index=4
# Source 2: https://dev.to/karenapp/how-to-get-started-with-google-calendar-api-using-python-with-examples-4c4h
# Source 3: https://github.com/karenapp/google-calendar-python-api/blob/master/list_events.py
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from datetime import datetime, timedelta
import pprint

pp = pprint.PrettyPrinter(indent=4)  # usage pp.pprint(stuff)


def get_calendar_service():
    """Return a google API service associated with a scope and google oath_key."""

    # 1.  Specify one or more scopes (strings or iterable)
    #     that you wish the google user to authorize
    scopes = "https://www.googleapis.com/auth/calendar"

    # 2.  Set name for local file created on google site
    #     which handles API's for registered projects
    google_oath_key = 'client_secret_oath_key_calendar.json'

    # 3.  Local file to store a google user's credential authorization
    store = file.Storage('storage.json')
    credz = store.get()
    if not credz or credz.invalid:
        flow = client.flow_from_clientsecrets(google_oath_key, scopes)
        credz = tools.run_flow(flow, store)

    # 4.  Instantiate Google service with authorization credential
    api = 'calendar'
    version = 'v3'
    service = build(api, version, http=credz.authorize(Http()))

    return service

def list_calendars(service):
    print('Getting list of calendars\n')
    calendars_result = service.calendarList().list().execute()

    calendars = calendars_result.get('items', [])

    if not calendars:
        print('No calendars found.')
    for calendar in calendars:
        summary = calendar['summary']
        id_ = calendar['id']
        primary = "Primary" if calendar.get('primary') else ""
        # print("%s\t%s\t%s" % (summary, id, primary))
        print(f'{summary}, \t{id_}, \t{primary}')
    print()

    pp.pprint(calendars_result)

def list_events(service):
    print('Getting list of events\n')

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting List of next 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    pp.pprint(events)

def update_event(service):
    print('Updating event\n')

    # update the event to tomorrow 9 AM IST

    d = datetime.now().date()
    tomorrow = datetime(d.year, d.month, d.day, 9) + timedelta(days=1)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=2)).isoformat()

    event_result = service.events().update(
        calendarId='primary',
        eventId='27mprdt4o3ema2p63ppti2jgrb',
        body={
            "summary": 'Updated Automating calendar',
            "description": 'This is a tutorial example of automating google calendar with python, updated time.',
            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
        },
    ).execute()

    print("updated event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])


if __name__ == '__main__':
    my_service = get_calendar_service()
    print(my_service)
    list_calendars(my_service)
    list_events(my_service)
    update_event(my_service)
