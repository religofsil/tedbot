# -*- coding: utf-8 -*-
import os
import re
import telebot
import random
import logging

import config
import botan
import stickers
import phrases

from utils import read_data, get_key_words
from collections import defaultdict

telebot.logger.setLevel(logging.INFO)  # Outputs info messages to console. Change to DEBUG to see debug messages.

regRus = re.compile('[а-яёА-ЯЁ]+')

DIR = os.path.dirname(os.path.realpath(__file__))

DATABASE = read_data()  # actually, not a database - just a list of Video instances

bot = telebot.TeleBot(config.TOKEN)

with open(DIR + config.WORDLIST, 'r', encoding='utf-8') as f:
    swords = f.readlines()  # list of swear words


def swearwords(text):
    """
    Check for swear words.
    Args:
        text: string with some text
    Returns:
        True if the text contains swear words, else False
    """
    for line in swords:
        line = line.strip()
        if line in text.lower():
            return True
    return False


def get_random_tags():
    """
    Return a string with a random message and 20 random tags from tag list, tags are separated by comma.
    """
    with open(DIR + config.TAGLIST, 'r', encoding='utf-8') as f:
        all_tags = []
        for line in f:
            all_tags.append(line.strip())
    random.shuffle(all_tags)
    final_string = ", ".join(all_tags[:20])
    final_string = random.choice(phrases.topics) + final_string
    return final_string


def tag_search(q):
    """
    Find a ted-talk that has query words among its tags.
    Args:
        q: string with user query
    Returns:
        Video instance or None
    """
    q = q.lower()
    q = [i.strip() for i in q.split(',')]
    d = defaultdict(int)
    for video in DATABASE:
        for n in q:
            if n in video.tags:
                d[video] += 1
    if d:
        arr = []
        bestchoice = d[sorted(d, key=d.get, reverse=True)[0]]
        if bestchoice == 0:
            return None
        for i in d:
            if d[i] == bestchoice:
                arr.append(i)
        return random.choice(arr)


def description_search(q):
    """
    Find a ted-talk that has query words among in its description.
    Args:
        q: string with user query
    Returns:
        Video instance or None
    """
    words = [i.strip().lower() for i in q.split(',')]
    arr = []
    for video in DATABASE:
        if all(i in video.description.lower() or i in video.tags for i in words):
            arr.append(video)
    if len(arr) != 0:
        return random.choice(arr)


def author_search(q):
    """
    Find a ted-talk that has query words among in the name of the speaker..
    Args:
        q: string with user query
    Returns:
        Video instance or None
    """
    arr = []
    for video in DATABASE:
        if q.lower().strip() in video.speaker_name.lower():
            arr.append(video)
    if len(arr) != 0:
        return random.choice(arr)


def random_video():
    """
    Return random ted talk (instance of Video).
    """
    return random.choice(DATABASE)


@bot.message_handler(commands=['start'])
def start_command(message):  # reacts to /start command
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'start')
    bot.send_message(message.chat.id, phrases.start)


@bot.message_handler(commands=['help'])
def help_command(message):  # reacts to /help command
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'help')
    bot.send_message(message.chat.id, phrases.help)


@bot.message_handler(commands=['random'])
def random_video_command(message):  # reacts to /random command - sends a random ted talk
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'random')
    send_video(message.chat.id, random_video())


@bot.message_handler(commands=['tags'])
def tags_command(message):  # reacts to /tags command - search a ted talk with listed tags
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'search by tags')
    message_text = message.text.replace('/tags', '').strip()
    if not message_text:
        bot.send_message(message.chat.id, 'Please, provide some tags after the command /tags:\n' + get_random_tags())
        return
    video = tag_search(message_text)
    send_video(message.chat.id, video)


@bot.message_handler(commands=['author'])
def author_command(message):  # reacts to /author command - search a ted talk of a given author
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'search by author')
    message_text = message.text.replace('/author', '').strip()
    if not message_text:
        bot.send_message(message.chat.id, 'Please, provide the author\'s name after the command /author, e.g.:\n/author Elon Musk')
        return
    video = author_search(message_text)
    send_video(message.chat.id, video)


@bot.message_handler(commands=['description'])
def description_command(message):  # reacts to /description command - search a ted talk with given words in description
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'search by description')
    message_text = message.text.replace('/description', '').strip()
    if not message_text:
        bot.send_message(message.chat.id, 'Please, provide some words after the command /description.')
        return
    video = description_search(message_text)
    send_video(message.chat.id, video)


@bot.message_handler(commands=['taglist'])
def taglist_command(message):  # reacts to /taglist command - returns 20 random tags
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'taglist')
    bot.send_message(message.chat.id, get_random_tags())


@bot.message_handler(regexp="(?i)thank.*")
def handle_message_thanks(message):  # reacts to thanks
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'thanks')
    bot.send_message(message.chat.id, "You're welcome. :)")


@bot.message_handler(regexp="(?i).*?your name.*")
def handle_message_name(message):  # reacts to any message with words "your name"
    botan.track(config.BOTAN_KEY, message.chat.id, message, 'name')
    bot.send_message(message.chat.id, "A bot has no name.")


@bot.message_handler(content_types=["text"])
def get_video_by_text(message):  # reacts to any text message
    # if the message is in Russian, the bot says it knows no Russian and sends a sticker
    if regRus.search(message.text) is not None:
        botan.track(config.BOTAN_KEY, message.chat.id, message, 'Russian: ' + message.text)
        bot.send_message(message.chat.id, random.choice(phrases.russian))
        bot.send_sticker(message.chat.id, random.choice(stickers.fish))
    else:
        # if the message contains swearwords, the bot reacts angrily and sends a sticker
        if swearwords(message.text):
            botan.track(config.BOTAN_KEY, message.chat.id, message, 'Swearword: ' + message.text)
            bot.send_message(message.chat.id, random.choice(phrases.swear))
            bot.send_sticker(message.chat.id, random.choice(stickers.gnidogadoids))
            return True
        # get key phrases from cognitive services and search database
        kw = get_key_words(message.text)
        to_search = message.text
        if kw:
            to_search = ','.join(kw)
        video = tag_search(to_search)
        if video is None:
            video = description_search(to_search)
        send_video(message.chat.id, video)


def send_video(chat_id, video):
    """
    Send info about ted talk and URL to user or say that nothing was found.
    Args:
        chat_id:  id of a telegram chat
        video:  Video instance
    """
    if not video:
        bot.send_message(chat_id, random.choice(phrases.no_match))
    else:
        collect_message = random.choice(phrases.found_something)
        collect_message += video.headline + '\r\nBy ' + video.speaker_name + ' \r\n\r\n'
        collect_message += 'Tags in video: ' + ', '.join(video.tags) + ' \r\n\r\n'
        collect_message += 'Description: ' + video.description + '\r\n\r\n'
        bot.send_message(chat_id, collect_message + video.URL)


if __name__ == '__main__':
    bot.polling(none_stop=True)
