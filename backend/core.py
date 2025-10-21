from googleapiclient.discovery import build
import pickle
import os

calendar_service = None

def get_calendar_service():
    """Get the global calendar service instance"""
    return calendar_service

def set_calendar_service(service):
    """Set the global calendar service instance"""
    global calendar_service
    calendar_service = service

def initialize_calendar_service():
    """Initialize calendar service from existing token if available"""
    global calendar_service
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                calendar_service = build('calendar', 'v3', credentials=creds)
                print("Calendar service initialized from existing token")
                return True
        except Exception as e:
            print(f"Failed to load existing token: {e}")
            return False
    return False




