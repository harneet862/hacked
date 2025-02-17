import datetime
import os.path
import requests
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly", "https://www.googleapis.com/auth/calendar"]

def get_credentials():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
  creds = None
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
  return creds

def save_credentials(creds):
    # Save the credentials for the next run in token.json
    with open("token.json", "w") as token:
      token.write(creds.to_json())

def get_scheduled_events(creds):
  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API

    # Get the calendar's timezone (e.g., 'America/Edmonton' for GMT-07:00)
    calendar = service.calendars().get(calendarId="primary").execute()
    calendar_timezone = calendar.get("timeZone", "UTC")

    # Get current time in the calendar's timezone
    tz = pytz.timezone(calendar_timezone)
    now = datetime.datetime.now(tz)

    # Set timeMin to the start of the current day in the calendar's timezone
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    # Set timeMax to the end of the current day in the calendar's timezone
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()

    # print(f"Start of Day: {start_of_day}")
    # print(f"End of Day: {end_of_day}")

    # print("Getting the events for the current day...")

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
      # print(f"Next Page Token: {page_token}")
            
      if not page_token:
        break # Exit the loop if there are no more pages

    if not events:
      print("No events found for today.")
      return
    
    # Create a list to store event data
    event_data = []
    
    # Prints the start, end, name of all events for today
    # print(f"Events collected in events list: {len(events)}") # Debugging: Checking how many events in collected from Cal
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date")) # trying to get datetime, if N/A then gets date
      end = event["end"].get("dateTime", event["start"].get("date"))

      # Parse the start and end timestamps into timezone-aware datetime objects
      start_dt = datetime.datetime.fromisoformat(start)
      end_dt = datetime.datetime.fromisoformat(end)

      # Get the time zone name (e.g. MDT, MST, PST)
      tz_name = start_dt.strftime("%Z") if start_dt.tzinfo else "Time Zone Unknown"

      # Format the date (e.g. "February 16, 2025")
      date_formatted = start_dt.strftime("%B %d, %Y")

      # Format the output string in 24-Hour format (e.g. "February 16, 2025 @ 18:00 MST")
      start_formatted = start_dt.strftime("%H:%M") 
      end_formatted = end_dt.strftime("%H:%M") 

      # print(f"Start Time: {start_formatted} End Time: {end_formatted} Event Title: {event['summary']}")

      # Append the event data to the list
      event_data.append({
          "date": date_formatted,
          "start_time": start_formatted,
          "end_time": end_formatted,
          "title": event["summary"]
      })
    return event_data
  except HttpError as error:
    print(f"An error occurred: {error}")

def send_event_data_to_server(event_data):
  # Send the event data to the Flask server
  url = "http://127.0.0.1:5000/calendar"  # TODO: CHECK THAT THIS IS CORRECT
  response = requests.post(url, json=event_data)

  # Check the response from the server
  if response.status_code == 200:
      print("Event data successfully sent to the Flask server.")
  else:
      print(f"Failed to send event data. Status code: {response.status_code}")
      print(f"Response: {response.text}")
  return

def run_events_caller():
  creds = get_credentials()
  save_credentials(creds)

  event_data = get_scheduled_events(creds)
  send_event_data_to_server(event_data)
  
  return

def main():
  run_events_caller()
  return
  
if __name__ == "__main__":
  main()