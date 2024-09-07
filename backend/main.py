from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from api import *
from api import app_router
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


# Function to initialize Google Calendar service




def onload():
    # pass
    debugpy.listen(("0.0.0.0", 5678))
    # initialize_calendar_service()




onload()


# FastAPI startup event to initialize the Google Calendar service
    



# Include routers
app.include_router(app_router, prefix="")