from fastapi import APIRouter
from app.services.nasa import fetch_today_neos

router = APIRouter(prefix="/neos", tags=["NEOs"])


@router.get("/today")
async def get_today_neos():
    return await fetch_today_neos()
