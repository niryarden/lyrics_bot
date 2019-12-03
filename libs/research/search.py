from langdetect import detect
from libs.research.lyrics import get_lyrics_for_english, get_lyrics_for_hebrew
from libs.research.meaning import get_meaning_for_english, get_meaning_for_hebrew


def get_output_by_name(to_search, wished_output):
    lang = detect(to_search)
    if wished_output == "lyrics":
        if lang == "he":
            return get_lyrics_for_hebrew(to_search)
        return get_lyrics_for_english(to_search)
    if lang == "he":
        return get_meaning_for_hebrew(to_search)
    return get_meaning_for_english(to_search)
