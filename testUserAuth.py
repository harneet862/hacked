from flask import Flask, redirect, url_for, session, request 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key used for session management and securing cookies

# Google OAuth settings
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
REDIRECT_URI = "http://localhost:5000/oauth2callback"

# Step 1: Redirect user to Google OAuth
@app.route("/")
def index():
    if "credentials" in session:
        return redirect(url_for("get_events"))
    return redirect(url_for("authorize"))

# Step 2: Start OAuth flow
@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(prompt="consent")
    session["state"] = state
    return redirect(auth_url)

# Step 3: Handle OAuth callback
@app.route("/oauth2callback")
def oauth2callback():
    state = session.get("state")
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI, state=state
    )
    flow.fetch_token(authorization_response=request.url)
    
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    
    return redirect(url_for("get_events"))

# Step 4: Fetch Google Calendar events
@app.route("/events")
def get_events():
    credentials = Credentials(**session["credentials"])
    service = build("calendar", "v3", credentials=credentials)
    
    events_result = service.events().list(
        calendarId="primary", maxResults=5, singleEvents=True, orderBy="startTime"
    ).execute()
    
    events = events_result.get("items", [])
    if not events:
        return "No upcoming events found."
    
    return "<br>".join([f"{event['summary']} - {event['start'].get('dateTime', 'All day')}" for event in events])

# Helper function to store credentials
def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

if __name__ == "__main__":
    app.run(debug=True)
