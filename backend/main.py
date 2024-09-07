from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
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

def onload():
    debugpy.listen(("0.0.0.0", 5678))
    

# Set up app
app = setup_fastapi()
onload()



# Include routers
app.include_router(app_router, prefix="")