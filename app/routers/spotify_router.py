from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.spotify_service import get_auth_url, exchange_code_for_token

router = APIRouter()


@router.get("/login")
def login():
    return RedirectResponse(get_auth_url())


@router.get("/callback")
def callback(code: str):
    token_data = exchange_code_for_token(code)
    return token_data
