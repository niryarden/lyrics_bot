import os
import json
import requests
from bs4 import BeautifulSoup as bs
from googlesearch import search


def get_lyrics_for_hebrew(to_search):
    # google search the song on "shironet.mako.co.il"
    lyrics_site = "shironet.mako.co.il"
    query = "site:" + lyrics_site + " " + to_search
    results_lst = [result for result in search(query, tld="com", num=1, stop=1, pause=0)]
    if len(results_lst) < 0:
        return "We're sorry but your song meaning wasn't found automatically - try looking it manually. 😩"
    url = results_lst[0]
    with open(os.path.join("data", "shironet.json"), 'r') as file_content:
        shironet_creds = json.loads(file_content.read())
        shironet_cookies = shironet_creds["cookies"]
        shironet_headers = shironet_creds["headers"]
    response = requests.get(url, headers=shironet_headers, cookies=shironet_cookies)
    response.encoding = 'utf-8'
    soup = bs(response.text, "html.parser")
    return soup.find('span', {'class': 'artist_lyrics_text'}).text


def get_lyrics_for_english(to_search):
    # google search the song on "songmeanings.com"
    lyrics_site = "songmeanings.com"
    query = "site:" + lyrics_site + " " + to_search
    results_lst = [result for result in search(query, tld="com", num=1, stop=1, pause=0)]
    if len(results_lst) < 1:
        return "We're sorry but your song lyrics wasn't found automatically - try looking it manually. 😩"
    url = results_lst[0]
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    # extracting the lyrics
    try:
        lyrics = soup.find('div', {'class': 'holder lyric-box'}).text
        lyrics = lyrics.replace("Edit Lyrics", "")
        lyrics = lyrics.replace("Edit Wiki", "")
        lyrics = lyrics.replace("Add Video", "")
        # getting rid of the last random line, and all the blankspaces in the begining
        lyrics = lyrics[:len(lyrics) - 90]
        return lyrics.lstrip()
    except:
        return "sorry. the song wasn't found"
