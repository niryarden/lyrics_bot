import json
import requests
from libs.utils.utils import get_base_url

BASE_URL = get_base_url()


# get the new updates from the bot, the new messages it got
def get_telegram_update(offset=None):
    url = f"{get_base_url()}getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    response = requests.get(url)
    content = response.content.decode("utf-8")
    return json.loads(content)


# returning the id of the last update. helps running on all the new messages
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# returning the text on the last message - when you want to read what the user wrote to you.
def get_last_msg_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    try:
        text = updates["result"][last_update]["message"]["text"]
    except KeyError:
        text = None
    return text
