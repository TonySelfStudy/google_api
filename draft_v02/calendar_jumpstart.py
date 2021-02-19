# based on https://www.youtube.com/watch?app=desktop&v=tNo9IoZMelI&list=PLOU2XLYxmsILOIxBRPPhgYbuSslr50KVq&index=21

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from tony_util.dir_diagnostics import values
import pprint
pp = pprint.PrettyPrinter(indent=4)
pprint = pp.pprint # usage pprint(stuff)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = "https://www.googleapis.com/auth/calendar"  # one of more scopes (strings or iterable)
CLIENT_SECRET = 'client_secret_oath_key_calendar.json'

store = file.Storage('cal_authorization_calendar.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow, store)

# SERVICE = build(API, VERSION, http=credz.authorize(Http()))

CAL = build('calendar', 'v3', http=credz.authorize(Http()))

GMT_OFF = '-08:00'
EVENT = {
    'summary': 'Dinner with friends',
    'start': {'dateTime': f'2021-02-18T19:00:00{GMT_OFF}'},
    'end': {'dateTime': f'2021-02-18T22:00:00{GMT_OFF}'},
    'attendees': [
        {'email': 'employee01@tony-held.com'},
        {'email': 'tony.held@gmail.com'},
    ]
}

e = CAL.events().insert(calendarId='primary',
                        sendNotifications=True, body=EVENT).execute()

pprint(e)
