from langdetect import detect
from libs.research.itunes import is_itunes_open, get_current_song_played_itunes
from libs.research.search import get_output_by_name


def generate_headline(wished_output, title, artist):
    if detect(title + " " + artist) == "he":
        if wished_output == "lyrics":
            return "*מילים לשיר '" + title + "' של " + artist + "*\n\n"
        return ""
    if wished_output == "lyrics":
        return "*Lyrics for the song '" + title + "' by " + artist + "*\n\n"
    return "*Meaning of the song '" + title + "' by " + artist + "*\n\n"


def generate_answer(from_itunes, wished_output, user_message):
    if from_itunes:
        if is_itunes_open():
            title, artist = get_current_song_played_itunes()
            to_search = title + " " + artist
            output = get_output_by_name(to_search, wished_output)
            headline = generate_headline(wished_output, title, artist)
            return headline + output
        return "No song is played on iTunes"
    to_search = user_message
    output = get_output_by_name(to_search, wished_output)
    headline = "*" + user_message + "*\n\n"
    return headline + output
