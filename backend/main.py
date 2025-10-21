from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from api import app_router
from core import initialize_calendar_service
import debugpy


# Set up fastapi
def setup_fastapi():
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


# Set up app
app = setup_fastapi()


def onload():
    debugpy.listen(("0.0.0.0", 5678))
    # Try to initialize calendar service from existing token
    if initialize_calendar_service():
        print("Google Calendar service initialized successfully from existing token")
    else:
        print("No existing token found. Please authenticate via /start_auth endpoint")


onload()


# Include routers
app.include_router(app_router, prefix="")