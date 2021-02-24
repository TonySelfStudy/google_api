# Created by Tony Held 02-19-21

# based on https://www.youtube.com/watch?app=desktop&v=tNo9IoZMelI&list=PLOU2XLYxmsILOIxBRPPhgYbuSslr50KVq&index=21

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import pprint
pp = pprint.PrettyPrinter(indent=4)  # usage pp.pprint(stuff)

# 1.  Specify one or more scopes (strings or iterable)
#     that you wish the google user to authorize
SCOPES = "https://www.googleapis.com/auth/calendar"

# 2.  Set name for local file created on google site
#     which handles API's for registered projects
CLIENT_SECRET = 'client_secret_oath_key_calendar.json'

# 3.  Local File to store credential authorization by user
store = file.Storage('cal_authorization_calendar.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow, store)

# 4.  Instantiate Google service with authorization credential
API = 'calendar'
VERSION = 'v3'
CAL = build(API, VERSION, http=credz.authorize(Http()))

# 5.  Use google api to create calendar invite
GMT_OFF = '-08:00'

EVENT = {
    'summary': 'Dinner with friends',
    'start': {'dateTime': f'2021-02-23T19:00:00{GMT_OFF}'},
    'end': {'dateTime': f'2021-02-23T22:00:00{GMT_OFF}'},
    'attendees': [
        {'email': 'employee01@tony-held.com'},
        # {'email': 'tony.held@gmail.com'},
    ]
}

e = CAL.events().insert(calendarId='primary',
                        sendNotifications=True, body=EVENT).execute()

pp.pprint(e)
