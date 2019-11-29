from langdetect import detect
import requests
from bs4 import BeautifulSoup as bs
from googlesearch import search
from win32com.client import Dispatch

# returning the title and the artist of the current playing song in iTunes
def get_current_song_played_iTunes():
    itunes = Dispatch("iTunes.Application")
    current_track = itunes.CurrentTrack
    title = current_track.Name
    title = title.replace("&", "and")
    artist = current_track.Artist
    artist = artist.replace("&", "and")
    tup = (title, artist)
    return(tup)

def get_meaning_by_name(song_name):
    lang = detect(song_name)
    if lang == "he":
        meaning = "😩 לצערנו, השירות של ניתוח שירים לא ניתן לשירים בעברית בשל חוסר במקור מידע מהימן"
    else: # language is english or something else
        # google search the song on "genius.com"
        meaning_site = "genius.com"
        query = "site:" + meaning_site + " " + song_name
        results_lst = list()
        for j in search(query, tld="com", num=1, stop=1, pause=0):
            results_lst.append(j)
        if len(results_lst) < 1:
            return "We're sorry but your song meaning wasn't found automatically - try looking it manually. 😩"
        url = results_lst[0]
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        try:
            meaning = soup.find("div", {"class":["rich_text_formatting"]}).text
        except:
            meaning = "We're so rry but your song meaning wasn't found automatically - try looking it manually. 😩"
        if meaning == " " or meaning == "" or meaning == None or meaning == "\n":
            meaning = "We're sorry but your song meaning wasn't found automatically - try looking it manually. 😩"
    return(meaning)


def get_msg_for_meaning(current, user_message):
    if current == True:
        current_track = get_current_song_played_iTunes()
        title = str(current_track[0])
        artist = str(current_track[1])
        to_search = title + " " + artist
        meaning = get_meaning_by_name(to_search)
        if detect(to_search) == "he":
            headline = ""
        else:
            headline = "*Meaning of the song '" + title + "' by " + artist + "*\n\n"
        message_text = headline + meaning
    else:
        to_search = user_message
        meaning = get_meaning_by_name(to_search)
        headline = "*" + to_search + "*\n\n"
        message_text = headline + meaning
    return message_text
