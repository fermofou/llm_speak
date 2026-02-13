from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat_router, spotify_router

app = FastAPI(
    title="LLM Speech Assistant",
    description="An LLM assistant that understands speech, can control Spotify, check weather, search Wikipedia, and more",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router.router)
app.include_router(spotify_router.router)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "LLM Speech Assistant",
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "tools": "/chat/tools",
            "speak": "/chat/speak"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
