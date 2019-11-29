from langdetect import detect
import requests
from bs4 import BeautifulSoup as bs
from googlesearch import search
import json

# get a name of song (maybe with an artist included inside), google search it return the lyrics
# the function changing the site it searches in according to the language of the song
# currently supports only english and hebrew
def GetLyricsByName(song_name):
    lang = detect(song_name)
    if lang == "he":
        # google search the song on "shironet.mako.co.il"
        lyrics_site = "shironet.mako.co.il"
        query = "site:" + lyrics_site + " " + song_name
        results_lst = list()
        for j in search(query, tld="com", num=1, stop=1, pause=2):
            results_lst.append(j)
        url = results_lst[0]
        r= requests.get(url)
        r.encoding = 'utf-8'
        soup = bs(r.text, "html.parser")
        lyrics = soup.find('span', {'class': 'artist_lyrics_text'}).text
    else: # language is english or something else
        # google search the song on "songmeanings.com"
        lyrics_site = "songmeanings.com"
        query = "site:" + lyrics_site + " " + song_name
        results_lst = list()
        for j in search(query, tld="com", num=1, stop=1, pause=2):
            results_lst.append(j)
        url = results_lst[0]
        r= requests.get(url)
        soup = bs(r.text, "html.parser")
        # extracting the lyrics
        lyrics = soup.find('div', {'class': 'holder lyric-box'}).text
        lyrics = lyrics.replace("Edit Lyrics", "")
        lyrics = lyrics.replace("Edit Wiki", "")
        lyrics = lyrics.replace("Add Video", "")
        # getting rid of the last random line, and all the blankspaces in the begining
        lyrics = lyrics[:len(lyrics) - 90]
        lyrics = lyrics.lstrip()

    return(lyrics)


# get a lyrics of a song and message it to Nir Yarden using the Telegram Lyrics_bot.
# return a dictionary (json based) with the details of the message which was sent
def SendMessageWithLyricsBot(lyrics):
    lyrics_bot_token = "888025423:AAF_ovzPu3HrrWrwzI5i5u41JTQqKvhD7sY"
    my_chat_id = "881293443"
    message_text = lyrics
    send_text = 'https://api.telegram.org/bot' + lyrics_bot_token + '/sendMessage?chat_id=' + my_chat_id + '&parse_mode=Markdown&text=' + message_text
    response = requests.get(send_text).json()
    return(response)


# MAIN
# calling all the abovementioned functions.
# getting a title and the artist of the currnet song from iTunes, sending the lyrics by telegram, printing

to_search = input("type the song >> ")
lyrics = GetLyricsByName(to_search)
message_text = lyrics
response_dict = SendMessageWithLyricsBot(message_text)
try:
    sent_message_body = response_dict["result"]["text"]
    print("the lyrics for the song '" + to_search + "' were sent to Nir Yarden from the lovely Lyrics_Bot")
except:
    print("Lyrics_bot sending his appologies.. but something went wrong")
