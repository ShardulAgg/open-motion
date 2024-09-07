from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
import webbrowser
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from api import *
from api import app_router
import debugpy


# Set up fastapi
# def setup_fastapi():
#     app = FastAPI()
#     origins = ["*"]
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=False,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
#     return app



# Set up app
app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_service = None

# Function to initialize Google Calendar service
def initialize_calendar_service():
    global calendar_service
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"Please visit this URL to authorize the application: {auth_url}")
            code = input("Enter the authorization code: ")
            flow.fetch_token(code=code)
            creds = flow.credentials

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    calendar_service = build('calendar', 'v3', credentials=creds)
    print("Calendar service initialized successfully")

@app.get("/start_auth")
async def start_auth():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', 
        SCOPES,
        redirect_uri='http://localhost:80/oauth2callback'  # Use your actual redirect URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url

@app.get("/oauth2callback")
async def oauth2callback(code: str = None, error: str = None):
    if error:
        return {"error": error}
    if code:
        return  code
    return {"error": "No code received"}

@app.get("/complete_auth")
async def complete_auth(code: str):
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', 
        SCOPES,
        redirect_uri='http://localhost:80/oauth2callback'
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    
    global calendar_service
    calendar_service = build('calendar', 'v3', credentials=creds)
    return {"message": "Authentication completed successfully"}




def onload():
    # pass
    debugpy.listen(("0.0.0.0", 5678))
    # initialize_calendar_service()




onload()


# FastAPI startup event to initialize the Google Calendar service
    
@app.get("/events")
async def get_calendar_events():
    if not calendar_service:
        raise HTTPException(status_code=500, detail="Google Calendar service not initialized")

    try:
        # Fetch events from Google Calendar
        events_result = calendar_service.events().list(
            calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return {"message": "No upcoming events found."}

        return [{"start": event['start'].get('dateTime', event['start'].get('date')), 
                 "summary": event['summary']} for event in events]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Include routers
app.include_router(app_router, prefix="")