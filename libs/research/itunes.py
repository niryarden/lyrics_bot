from win32com.client import Dispatch


def is_itunes_open():
    try:
        itunes = Dispatch("iTunes.Application")
        current_track = itunes.CurrentTrack
        title = current_track.Name
        return True
    except AttributeError:
        return False


def get_current_song_played_itunes():
    itunes = Dispatch("iTunes.Application")
    current_track = itunes.CurrentTrack
    title = current_track.Name
    title = title.replace("&", "and")
    artist = current_track.Artist
    artist = artist.replace("&", "and")
    return title, artist
