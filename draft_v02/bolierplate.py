# From video lesson https://www.youtube.com/watch?v=Z5G0luBohCg&list=PLOU2XLYxmsILOIxBRPPhgYbuSslr50KVq&index=4

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import pprint
pp = pprint.PrettyPrinter(indent=4)  # usage pp.pprint(stuff)

# 1.  Specify one or more scopes (strings or iterable)
#     that you wish the google user to authorize
SCOPES = ""

# 2.  Set name for local file created on google site
#     which handles API's for registered projects
CLIENT_SECRET = 'client_secret_oath_key.json'

# 3.  Local File to store credential authorization by user
store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow, store)

# 4.  Instantiate Google service with authorization credential
API = 'calendar'
VERSION = 'v3'
SERVICE = build(API, VERSION, http=credz.authorize(Http()))

# 5.  Use google api service with good intentions
pp.pprint(SERVICE)

