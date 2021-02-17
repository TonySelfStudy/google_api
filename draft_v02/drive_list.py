# From video lesson https://www.youtube.com/watch?v=Z5G0luBohCg&list=PLOU2XLYxmsILOIxBRPPhgYbuSslr50KVq&index=4

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = "https://www.googleapis.com/auth/drive.readonly" # one of more scopes (strings or iterable)
CLIENT_SECRET = 'client_secret_oath_key_gdrive.json'

store = file.Storage('storage_oath_key_gdrive.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow, store)

SERVICE = build('drive', 'v2', http=credz.authorize(Http()))

files = SERVICE.files().list().execute().get('items', [])
for f in files:
    print(f"{f['title']=}, {f['mimeType']=}")

