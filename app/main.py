from fastapi import FastAPI
from app.routers import chat_router,spotify_router

app = FastAPI()

app.include_router(chat_router.router)
app.include_router(spotify_router.router)
