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


# get a name of song (maybe with an artist included inside), google search it return the lyrics
# the function changing the site it searches in according to the language of the song
# currently supports only english and hebrew
def get_lyrics_by_name(song_name):
    lang = detect(song_name)
    if lang == "he":
        # google search the song on "shironet.mako.co.il"
        lyrics_site = "shironet.mako.co.il"
        query = "site:" + lyrics_site + " " + song_name
        results_lst = list()
        for j in search(query, tld="com", num=1, stop=1, pause=0):
            results_lst.append(j)
        if len(results_lst) < 0:
            return "We're sorry but your song meaning wasn't found automatically - try looking it manually. 😩"
        url = results_lst[0]
        shironet_cookies = {
            "rbzid": "jhUn+Y00n+FMi+LOeQsbknxNe+2e/z6zE4VOK3UK30Lq5Cm0kZ2Ng5de4WUqR0IjFp59Kr/6vhSgG+5D4xdcsm8+0cTMr6Pp4LULGRK5ID5zwGjWoOwm3fkfEq/dQKeKJJKaIdrIR5h6EMF5T0vMEWAm9b4cTpTMdyR7/0mIGTRBJZPcihTKy+oZ6uRPNLHoUqOHDyXvt8A9NrGgVhNs9k6f8Wygz3uHYH+WnR3SZwM="
        }
        shironet_header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        r= requests.get(url, headers=shironet_header, cookies=shironet_cookies)
        r.encoding = 'utf-8'
        soup = bs(r.text, "html.parser")
        lyrics = soup.find('span', {'class': 'artist_lyrics_text'}).text
    else: # language is english or something else
        # google search the song on "songmeanings.com"
        lyrics_site = "songmeanings.com"
        query = "site:" + lyrics_site + " " + song_name
        results_lst = list()
        for j in search(query, tld="com", num=1, stop=1, pause=0):
            results_lst.append(j)
        if len(results_lst) < 1:
            return "We're sorry but your song lyrics wasn't found automatically - try looking it manually. 😩"
        url = results_lst[0]
        r= requests.get(url)
        soup = bs(r.text, "html.parser")
        # extracting the lyrics
        try:
            lyrics = soup.find('div', {'class': 'holder lyric-box'}).text
            lyrics = lyrics.replace("Edit Lyrics", "")
            lyrics = lyrics.replace("Edit Wiki", "")
            lyrics = lyrics.replace("Add Video", "")
            # getting rid of the last random line, and all the blankspaces in the begining
            lyrics = lyrics[:len(lyrics) - 90]
            lyrics = lyrics.lstrip()
        except:
            lyrics = "sorry. the song wasn't found"
    return(lyrics)

# get a lyrics of a song and message it to Nir Yarden using the Telegram Lyrics_bot.
# return a dictionary (json based) with the details of the message which was sent


def get_msg_for_lyrics(current, user_message):
    if current == True:
        current_track = get_current_song_played_iTunes()
        title = str(current_track[0])
        artist = str(current_track[1])
        to_search = title + " " + artist
        lyrics = get_lyrics_by_name(to_search)
        if detect(to_search) == "he":
            headline = "*מילים לשיר '" + title + "' של " + artist + "*\n\n"
        else:
            headline = "*Lyrics for the song '" + title + "' by " + artist + "*\n\n"
        message_text = headline + lyrics
    else:
        to_search = user_message
        lyrics = get_lyrics_by_name(to_search)
        headline = "*" + user_message + "*\n\n"
        message_text = headline + lyrics
    return message_text
