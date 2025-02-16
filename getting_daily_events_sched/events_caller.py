import datetime
import os.path
import zoneinfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token: # if the credential instance exists but is expired and needs to refresh
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=5000)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API

    # Get current time in UTC, timezone aware
    now = datetime.datetime.now(datetime.timezone.utc) 

    # Set timeMin to the start of the current day in UTC
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    # Set timeMax to the start of the NEXT day in UTC
    end_of_day = (now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)).isoformat()

    print(start_of_day)
    print(end_of_day)

    print("Getting the events for the current day...")

    # Initialize variables for handling pagination
    events = []
    page_token = None
    
    while True:
      # Make a request to the Calendar API
      events_result = (
          service.events()
          .list(
              calendarId="primary",
              timeMin=start_of_day,
              timeMax=end_of_day,
              singleEvents=True,
              orderBy="startTime",
              pageToken=page_token  # Pass the page token for pagination
          )
          .execute()
      )
      # Add the events from this page to the list
      events.extend(events_result.get("items", []))

      # Check if there are more pages
      page_token = events_result.get("nextPageToken")
      
      # Debugging: Print the page token
      print(f"Next Page Token: {page_token}")
            
      if not page_token:
        break # Exit the loop if there are no more pages

    if not events:
      print("No events found for today.")
      return

    # Prints the start, end, name of all events for today
    print(f"Events collected in events list: {len(events)}") # Debugging: Checking how many events in collected from Cal
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date")) # trying to get datetime, if N/A then gets date
      end = event["end"].get("dateTime", event["start"].get("date"))

      # Parse the start and end timestamps into timezone-aware datetime objects
      start_dt = datetime.datetime.fromisoformat(start)
      end_dt = datetime.datetime.fromisoformat(end)

      # Get the time zone name (e.g. MDT, MST, PST)
      tz_name = start_dt.strftime("%Z") if start_dt.tzinfo else "Time Zone Unknown"

      # Format the output string in 24-Hour format (e.g. "February 16, 2025 @ 18:00 MST")
      start_formatted = start_dt.strftime(f"%B %d, %Y @ %H:%M {tz_name}")
      end_formatted = end_dt.strftime(f"%B %d, %Y @ %H:%M {tz_name}")

      print(f"Start Time: {start_formatted} End Time: {end_formatted} Event Title: {event['summary']}")

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()