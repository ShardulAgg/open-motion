from core import *
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle


app_router = APIRouter()


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_service = None

class Task(BaseModel):
    name: str
    desc: str
    priority: int
    due_date: datetime
    duration: str

@app_router.post("/add_task")
def create_task(task: Task):
    return {"message": "Task added successfully"}

@app_router.get("/start_auth")
async def start_auth():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', 
        SCOPES,
        redirect_uri='http://localhost:80/oauth2callback'  # Use your actual redirect URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url

@app_router.get("/oauth2callback")
async def oauth2callback(code: str = None, error: str = None):
    if error:
        return {"error": error}
    if code:
        return  code
    return {"error": "No code received"}

@app_router.get("/complete_auth")
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



@app_router.get("/events")
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

@app_router.get("/")
def health_check():
    return {"status": "ok"}

__all__ = ["app_router"]