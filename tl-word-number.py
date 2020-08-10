# -*- coding: utf-8 -*-

# All queries to the Telegram Bot API must be served over HTTPS 
# and need to be presented in this form: https://api.telegram.org/bot<token>/METHOD_NAME

# Replace <token> with the bot's HTTP API token

import requests
import json

MY_TOKEN = "1346698532:AAEERcBd6Z4xW0-sqDLLd3bawF_yG5Icc9k"


# Framework


def base_url():
    return "https://api.telegram.org/bot{}/".format(MY_TOKEN)

def get_updates(offset=None):
    url = base_url() + "getUpdates?timeout=100"
    if offset:
        url = url + "&offset={}".format(offset + 1)
    r = requests.get(url)
    return json.loads(r.content)

def send_message(msg, chat_id):
    url = base_url() + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
    if msg != None:
        requests.get(url)


# Functions


def word_counter(msg):
    if not msg:
        return 0
    return len(msg.split())

def line_counter_excluding_empty_lines(msg):
    if not msg:
        return 0
    else:
        count = 0
        for line in msg.splitlines():
            if line != "":
                count += 1
        return count

def line_counter_including_empty_lines(msg):
    if not msg:
        return 0
    else:
        return len(msg.splitlines())

def paragraph_counter(msg):
    if not msg:
        return 0
    else:
        count = 0
        for line in msg.splitlines():
            if line != None and line != "":
                count += 1
        return count

def main():

    update_id = None

    while True:
        updates = get_updates(offset=update_id)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                try:
                    message = str(item["message"]["text"])
                except:
                    message = None
                sender = item["message"]["from"]["id"]
                if message == "/start":
                    reply = "Send me any text and I will send you back statistics about it (words, characters, lines, paragraphs)."
                else:
                    reply = "- Words: {}\n\n- Characters (excluding spaces): {}\n\n- Characters (including spaces): {}\n\n- Lines (excluding empty lines): {}\n\n- Lines (including empty lines): {}\n\n- Paragraphs: {}".format(word_counter(message), 0 if not message else len(message) - message.count(" ") - message.count("\n"), 0 if not message else len(message) - message.count("\n"), line_counter_excluding_empty_lines(message), line_counter_including_empty_lines(message), paragraph_counter(message))
                send_message(reply, sender)

if __name__ == "__main__":
    main()