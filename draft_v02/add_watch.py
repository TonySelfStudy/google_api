# Based on
# https://developers.google.com/calendar/v3/push
# https://medium.com/swlh/google-drive-push-notification-b62e2e2b3df4

from oauth2client import file, client, tools

import uuid
import requests
import json

from tony_util.dir_diagnostics import values

# 1.  Specify one or more scopes (strings or iterable)
#     that you wish the google user to authorize
SCOPES = "https://www.googleapis.com/auth/calendar"  # one of more scopes (strings or iterable)

# 2.  Set name for local file created on google site
#     which handles API's for registered projects
CLIENT_SECRET = 'client_secret_oath_key_calendar.json'

# 3.  Local File to store credential authorization by user
store = file.Storage('cal_authorization_calendar.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow, store)

# 4. Get access token for http webhook request
# todo - flesh this out
access_token_info = credz.get_access_token()
token = access_token_info.access_token

# 5.  Create components of http watch request

# A. Create randomly generated id associated with channel information
#    and specify the address that will handle the watch request.
channel_id = str(uuid.uuid4())
watch_handler = 'https://ez066144.pythonanywhere.com/parse_request'

# B. Determine web google web address to send POST request to
# Example http watch requests
# https://www.googleapis.com/apiName/apiVersion/resourcePath/watch
# POST https://www.googleapis.com/calendar/v3/calendars/my_calendar@gmail.com/events/watch
watch_request = "https://www.googleapis.com/calendar/v3/calendars/1706.fawn.gate@gmail.com/events/watch"

# C. Create header and body for POST request
header = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
body = {
    "id": channel_id,
    "type": "web_hook",
    "address": f'{watch_handler}'
}

# D. Execute POST request
r = requests.post(url=watch_request,
                  data=json.dumps(body), headers=header)
print(r)
values(r)
