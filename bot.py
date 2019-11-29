import requests
import json
import urllib
import configparser as cfg
import time
import signal
from operators.lyrics import get_msg_for_lyrics
from operators.meaning import get_msg_for_meaning
from operators.commands import *

# render token
parser = cfg.ConfigParser()
parser.read('token.cfg')
TOKEN = parser.get('creds', 'token')

# define base url
BASE_URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# define mychat_id
CHAT_ID = 881293443

# define a list which will help me keep track with the messages i've sent
# does not include "Working on it..." and "unrecognized command. try typing again" messages
sent_messages = []


# running a url on the telegram api and returns the json
def get_json_from_url(url):
    try:
        response = requests.get(url)
    except:
        on_bot_sleep(None, None)
        response = requests.get(url)
    content = response.content.decode("utf-8")
    return json.loads(content)


# get the new updates from the bot, the new messages it got
def get_telegram_update(offset=None):
    url = BASE_URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


# the basic function for sending a message to the user. just send it the text you want
def send_telegram_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = BASE_URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    url = url + "&parse_mode=Markdown"
    response = get_json_from_url(url)
    # save in the sent_messages list all the messages which were sent since the script started running
    if text != "Working on it...":
        sent_messages.append(text)


# returning the id of the last update. helps running on all the new messages
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

# get the chat_id of the last message which was sent to the bot, in order to answer specifecly him
# def get_chat_id(updates):
#     num_updates = len(updates["result"])
#     last_update = num_updates - 1
#     chat_id = updates["result"][last_update]["message"]["chat"]["id"]
#     return chat_id

# returning the text on the last message - when you want to read what the user wrote to you.
def get_last_msg_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    try:
        text = updates["result"][last_update]["message"]["text"]
    except KeyError:
        text = None
    return text


# get the last message of the user, understand it, and answer. do not return anything.
def reply_user(user_msg, chat_id):
    lyrics_commands = get_lyrics_commands()
    meaning_commands = get_meaning_commands()
    info_commands = get_info_commands()
    cheers_commands = get_cheers_commands()
    bye_commands = get_bye_commands()

    if user_msg in lyrics_commands:
        send_telegram_message("Working on it... ⌛", CHAT_ID)
        msg = get_msg_for_lyrics(current=True, user_message="!")
    elif user_msg in meaning_commands:
        send_telegram_message("Working on it... ⌛", CHAT_ID)
        msg = get_msg_for_meaning(current=True, user_message="!")
    elif user_msg in info_commands:
        with open("static\info.txt", encoding="utf8") as info_text:
            msg = info_text.read()
    elif user_msg in cheers_commands:
        msg = "I'm perfectly fine! thank you 😎\n\nPress /commands to see what I can do."
    elif user_msg in bye_commands:
        msg = "You can say goodbye but I'm staying here, always awake, waiting to help you like a best friend should ❤"
    elif user_msg[0] == ("\"") and user_msg[len(user_msg) - 1] == ("\""):
        send_telegram_message("Working on it... ⌛", CHAT_ID)
        msg = get_msg_for_lyrics(current=False, user_message=user_msg[1: len(user_msg) - 1])
    elif user_msg[0] == ("{") and user_msg[len(user_msg) - 1] == ("}"):
        send_telegram_message("Working on it... ⌛", CHAT_ID)
        msg = get_msg_for_meaning(current=False, user_message=user_msg[1: len(user_msg) - 1])
    else:
        with open("static\\unrecognized.txt", encoding="utf8") as unrecognized_text:
            msg = unrecognized_text.read()
    send_telegram_message(msg, chat_id)


# this function is called when the script is being keyboardinterrupted. sending the user a message.
def on_bot_sleep(signal, frame):
    send_telegram_message("The Lyrics Bot went to sleep. See you soon 😴", CHAT_ID)
    print("KeyboardInterrupted - bot going to sleep")
    exit(0)


def wait_for_messages():
    last_update_id = None

    # eternal loop checking for new updates every half a second
    while True:
        updates = get_telegram_update(last_update_id)
        if len(updates["result"]) > 0:
            # chat_id = get_chat_id(updates)
            last_update_id = get_last_update_id(updates) + 1
            user_msg_text = get_last_msg_text(updates)
            if user_msg_text is None:
                user_msg_text = "info"
            reply_user(user_msg_text, CHAT_ID)
        time.sleep(0.5)


# main
def main():
    # handle wake up
    print("running ...")
    send_telegram_message("The Lyrics Bot is now awake! 😎", CHAT_ID)

    # handle go to sleep
    signal.signal(signal.SIGINT, on_bot_sleep)

    wait_for_messages()
