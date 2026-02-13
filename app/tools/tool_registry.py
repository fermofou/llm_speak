from app.tools.spotify_tools import (
    play_song,
    pause_playback,
    resume_playback,
    next_track,
    previous_track,
    get_current_track,
)

AVAILABLE_TOOLS = {
    "play_song": play_song,
    "pause_playback": pause_playback,
    "resume_playback": resume_playback,
    "next_track": next_track,
    "previous_track": previous_track,
    "get_current_track": get_current_track,
}
