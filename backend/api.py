from core import *
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import re
from googleapiclient.errors import HttpError


app_router = APIRouter()


SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_service = None
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

class Task(BaseModel):
    eventName: str
    priority: str
    # due_date: datetime
    duration: str



async def delete_open_motion_events():
        # Get all events for the current month
    events = await get_events()
    open_motion_events = events['open_motion_events']
    
    deleted_count = 0
    for event in open_motion_events:
        try:
            # Search for the event by its name
            events_result = calendar_service.events().list(
                calendarId='primary',
                q=event['event-name'],
                singleEvents=True
            ).execute()
            
            items = events_result.get('items', [])
            
            for item in items:
                if 'open-motion' in item.get('description', '').lower():
                    calendar_service.events().delete(
                        calendarId='primary',
                        eventId=item['id']
                    ).execute()
                    deleted_count += 1
        
        except HttpError as error:
            print(f"An error occurred while deleting event {event['event-name']}: {error}")
    
    return {"message": f"Successfully deleted {deleted_count} open-motion events"}





async def add_task(task: Task):
    start_time = datetime.utcnow() + timedelta(minutes=30)
    end_time = start_time + timedelta(minutes=int(task.duration.split()[0]))
    event = {
        'summary': task.eventName,
        'description': f'open-motion\nPriority: {task.priority}\nDuration: {task.duration}',
        'start': {'dateTime': start_time.isoformat() + 'Z'},
        'end': {'dateTime': end_time.isoformat() + 'Z'},
    }
    calendar_service.events().insert(calendarId='primary', body=event).execute()
    return {"message": "Task added successfully to Google Calendar"}

async def get_events():
        # Get the first and last day of the current month
    now = datetime.utcnow()
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

    # Fetch events from Google Calendar for the current month
    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=first_day.isoformat() + 'Z',
        timeMax=last_day.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    open_motion_events = []
    default_events = []

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        if 'open-motion' in event.get('description', '').lower():
            # Parse priority and duration from the description
            description = event.get('description', '').lower()
            priority = 'medium'  # default priority
            if 'high' in description:
                priority = 'high'
            elif 'low' in description:
                priority = 'low'
            
            duration = '60 minutes'  # default duration
            duration_match = re.search(r'(\d+)\s*minutes', description)
            if duration_match:
                duration = f"{duration_match.group(1)} minutes"

            open_motion_events.append({
                'event-name': event['summary'],
                'event-priority': priority,
                'event-duration': duration
            })
        else:
            default_events.append({
                'event-name': event['summary'],
                'timeslot': f"{start} to {end}"
            })

    return {
        "open_motion_events": open_motion_events,
        "default_events": default_events
    }


async def add_event(event_name: str, event_priority: str, event_duration: str):
    pst_zone = ZoneInfo("America/Los_Angeles")
    now = datetime.now(pst_zone)
    end_time = now + timedelta(days=7)
    
    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=now.astimezone(ZoneInfo("UTC")).isoformat(),
        timeMax=end_time.astimezone(ZoneInfo("UTC")).isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    
    duration = timedelta(minutes=int(event_duration.split()[0]))
    
    current_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
    if current_time < now:
        current_time += timedelta(days=1)
    
    while current_time < end_time:
        if 10 <= current_time.hour < 21 and current_time.weekday() < 5:
            event_start = current_time
            event_end = event_start + duration
            if event_end.hour >= 21:
                current_time = current_time.replace(hour=10, minute=0) + timedelta(days=1)
                continue
            
            if all(event_start >= datetime.fromisoformat(e['end'].get('dateTime', e['end'].get('date'))).replace(tzinfo=pst_zone) or
                   event_end <= datetime.fromisoformat(e['start'].get('dateTime', e['start'].get('date'))).replace(tzinfo=pst_zone)
                   for e in events):
                new_event = {
                    'summary': event_name,
                    'description': f'open-motion\nPriority: {event_priority}\nDuration: {event_duration}',
                    'start': {'dateTime': event_start.isoformat(), 'timeZone': 'America/Los_Angeles'},
                    'end': {'dateTime': event_end.isoformat(), 'timeZone': 'America/Los_Angeles'},
                }
                calendar_service.events().insert(calendarId='primary', body=new_event).execute()
                return {"message": f"Event '{event_name}' added successfully for {event_start.isoformat()}"}
        
        current_time += timedelta(minutes=15)
    
    return {"message": "No suitable time slot found within the next week's business hours"}

async def add_events(open_motion_events: list[dict[str, str]]):
    priority_order = {'high': 1, 'medium': 2, 'low': 3}
    
    # Sort events by priority
    sorted_events = sorted(open_motion_events, key=lambda x: priority_order.get(x['event-priority'], 4))
    
    for event in sorted_events:
        await add_event(
            event_name=event['event-name'],
            event_priority=event['event-priority'],
            event_duration=event['event-duration']
        )


async def sync():
    events = await get_events()
    open_motion_events = events['open_motion_events']
    await delete_open_motion_events()
    return await add_events(open_motion_events)


@app_router.post("/add_task")
async def create_task(task: Task):
    await add_task(task)
    await sync()



@app_router.post("/create_open_motion_events")
async def create_task():
    if not calendar_service:
        raise HTTPException(status_code=500, detail="Google Calendar service not initialized")
    try:
        now = datetime.utcnow()
        for i in range(1, 3):
            start_time = now + timedelta(hours=i)
            end_time = start_time + timedelta(hours=1)
            event = {
                'summary': f'Open Motion Event {i}',
                'description': 'open-motion',
                'start': {
                    'dateTime': start_time.isoformat() + 'Z',
                },
                'end': {
                    'dateTime': end_time.isoformat() + 'Z',
                },
            }
            calendar_service.events().insert(calendarId='primary', body=event).execute()
        return {"message": "Two open-motion events added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app_router.get("/events")
async def get_calendar_events():
    if not calendar_service:
        raise HTTPException(status_code=500, detail="Google Calendar service not initialized")
    try:
        # Get the first and last day of the current month
        now = datetime.utcnow()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        # Fetch events from Google Calendar for the current month
        events_result = calendar_service.events().list(
            calendarId='primary',
            timeMin=first_day.isoformat() + 'Z',
            timeMax=last_day.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        if not events:
            return {"message": "No events found for the current month."}
        return [events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app_router.get("/get_categorized_events")
async def get_categorized_events():
    if not calendar_service:
        raise HTTPException(status_code=500, detail="Google Calendar service not initialized")
    try:
        # Get the first and last day of the current month
        return await get_events()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

async def syncEvents():
    if not calendar_service:
        raise HTTPException(status_code=500, detail="Google Calendar service not initialized")
    try:
        # Get the first and last day of the current month
        return await sync()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app_router.get("/")
def health_check():
    return {"status": "ok"}

__all__ = ["app_router"]