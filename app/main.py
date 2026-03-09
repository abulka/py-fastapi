from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import info

app = FastAPI()

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(info.router)
