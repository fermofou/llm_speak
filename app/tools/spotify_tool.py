from app.services.spotify_service import SpotifyService

spotify_service = SpotifyService()


def play_song(song: str) -> dict:
    """
    Plays a song on the user's active Spotify device.
    """
    return spotify_service.play_song(song)


def pause_playback() -> dict:
    return spotify_service.pause()


def resume_playback() -> dict:
    return spotify_service.resume()


def next_track() -> dict:
    return spotify_service.next_track()


def previous_track() -> dict:
    return spotify_service.previous_track()


def get_current_track() -> dict:
    return spotify_service.current_track()
