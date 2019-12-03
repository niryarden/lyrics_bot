import time
import signal
from functools import partial
import logging
from libs.bot.listen import get_telegram_update, get_last_update_id, get_last_msg_text
from libs.bot.respond import send_telegram_message, reply_user

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


# this function is called when the script is being keyboardinterrupted. sending the user a message.
def on_bot_sleep(chat_id, signal, frame):
    send_telegram_message("The Lyrics Bot went to sleep. See you soon 😴", chat_id)
    logging.info("KeyboardInterrupted - bot going to sleep")
    exit(0)


def wait_for_messages(chat_id):
    last_update_id = None

    # eternal loop checking for new updates every half a second
    while True:
        updates = get_telegram_update(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            user_msg_text = get_last_msg_text(updates)
            if user_msg_text is None:
                user_msg_text = "/info"
            reply_user(user_msg_text, chat_id)
        time.sleep(0.5)


# main
def main(chat_id):
    # handle wake up
    logging.info("running ...")
    send_telegram_message("The Lyrics Bot is now awake! 😎", chat_id)

    # handle go to sleep
    signal.signal(signal.SIGINT, partial(on_bot_sleep, chat_id))

    wait_for_messages(chat_id)
