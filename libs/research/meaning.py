import requests
from bs4 import BeautifulSoup as bs
from googlesearch import search


def get_meaning_for_hebrew(to_search):
    return "😩 לצערנו, השירות של ניתוח שירים לא ניתן לשירים בעברית בשל חוסר במקור מידע מהימן"


def get_meaning_for_english(to_search):
    # google search the song on "genius.com"
    meaning_site = "genius.com"
    query = "site:" + meaning_site + " " + to_search
    results_lst = [result for result in search(query, tld="com", num=1, stop=1, pause=0)]
    if len(results_lst) < 1:
        return "We're sorry but your song meaning wasn't found automatically - try looking it manually. 😩"
    url = results_lst[0]
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    try:
        meaning = soup.find("div", {"class": ["rich_text_formatting"]}).text
        if meaning not in [" ", "", None, "\n"]:
            return meaning
        return "We're sorry but your song meaning wasn't found automatically - try looking it manually. 😩"
    except:
        return "We're sorry but your song meaning wasn't found automatically - try looking it manually. 😩"
