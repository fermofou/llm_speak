from app.tools import spotify_tools

AVAILABLE_TOOLS = {
    "play_song": spotify_tools.play_song,
    "pause_playback": spotify_tools.pause_playback,
    "resume_playback": spotify_tools.resume_playback,
    "next_track": spotify_tools.next_track,
    "previous_track": spotify_tools.previous_track,
    "get_current_track": spotify_tools.get_current_track,
}
