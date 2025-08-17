import os
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
client_config = {
  "installed": {
    "client_id": client_id,
    "client_secret": client_secret,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
  }
}
flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_console()
print("REFRESH_TOKEN=", creds.refresh_token)
