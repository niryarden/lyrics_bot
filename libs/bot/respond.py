import urllib
import json
import os
import requests
from libs.research.research import generate_answer
from libs.utils.utils import get_base_url


# the basic function for sending a message to the user. just send it the text you want
def send_telegram_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = f"{get_base_url()}sendMessage?text={text}&chat_id={chat_id}"
    url = url + "&parse_mode=Markdown"
    requests.get(url)


def understand_and_generate_answer(user_msg):
    with open(os.path.join('data', 'user_inputs.json'), 'r') as file_content:
        commands = json.loads(file_content.read())
    if user_msg.lower() in commands["lyrics"]:
        return generate_answer(from_itunes=True, wished_output="lyrics", user_message=user_msg)
    elif user_msg.lower() in commands["meaning"]:
        return generate_answer(from_itunes=True, wished_output="meaning", user_message=user_msg)
    elif user_msg.lower() in commands["info"]:
        with open(os.path.join("data", "info.txt"), encoding="utf8") as info_text:
            return info_text.read()
    elif user_msg.lower() in commands["cheers"]:
        return "I'm perfectly fine! thank you 😎\n\nPress /commands to see what I can do."
    elif user_msg.lower() in commands["bye"]:
        return "You can say goodbye but I'm staying here, always awake, waiting to help you like a best friend should ❤"
    elif user_msg[0] == "\"" and user_msg[len(user_msg) - 1] == "\"":
        return generate_answer(from_itunes=False, wished_output="lyrics", user_message=user_msg[1: len(user_msg) - 1])
    elif user_msg[0] == "{" and user_msg[len(user_msg) - 1] == "}":
        return generate_answer(from_itunes=False, wished_output="meaning", user_message=user_msg[1: len(user_msg) - 1])
    else:
        with open(os.path.join("data", "unrecognized.txt"), encoding="utf8") as unrecognized_text:
            return unrecognized_text.read()


# get the last message of the user, understand it, and answer. do not return anything.
def reply_user(user_msg, chat_id):
    send_telegram_message("Working on it... ⌛", chat_id)
    answer = understand_and_generate_answer(user_msg)
    send_telegram_message(answer, chat_id)
