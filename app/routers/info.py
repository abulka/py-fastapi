from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import random
import time

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Random Info Test"})
@router.get("/random-info")
async def get_random_info():
    info_list = [
        "The server is running on FastAPI.",
        f"Server timestamp: {time.ctime()}",
        f"Random number: {random.randint(1, 1000)}",
        "This data was fetched asynchronously.",
        "Fedora Silverblue + Podman detected!",
        "Andy was here. 🤓😁😆😆😆😆 🔥",
        "Containers make development reproducible."
    ]
    return {"data": random.choice(info_list), "success": True}