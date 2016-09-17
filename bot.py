# -*- coding: utf-8 -*-
import config
import telebot
import random
import botan
from getdata import _read_data, processRequest
import os
import uuid
from collections import defaultdict

_url = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
_key = 'fc40878d47ed438bb7f229f9ebd34802'
DIR = os.getcwd()

from getdata import _read_data, Video

database = _read_data()
botan_token = 'FUYkZeK4x63xg32AJGe44tKFk:_xCBkc'


def get_key_words(text):
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json'
    params = None
    json = {
              "documents": [
                {
                  "language": "en",
                  "id": 'string',
                  "text": text
                }
              ]
            }
    data = None

    result = processRequest('post', _url, json, data, headers, params)
    if result and 'documents' in result:
        return result['documents'][0]["keyPhrases"]
    return None


def get_random_tags():
    f = open(DIR+'/taglist.txt', 'r', encoding='utf-8')
    all_tags = []
    for line in f:
        all_tags.append(line.strip())
    random.shuffle(all_tags)
    final_string = ", ".join(all_tags[:20])
    final_string = 'Here are some topics that might get your attention:\n\n' + final_string
    return final_string


def tag_search(q):
    q = q.lower()
    q = [i.strip() for i in q.split(',')]
    d = {}
    for video in database:
        d[video.URL] = 0
        for n in q:
            if n in video.tags:
                d[video.URL] += 1
    arr = []
    bestchoice = d[sorted(d, key=d.get, reverse=True)[0]]
    if bestchoice == 0:
        return None
    for i in d:
        if d[i] == bestchoice:
            arr.append(i)
    return random.choice(arr)



def description_search(q):
    words = [i.strip().lower() for i in q.split(',')]
    arr = []
    for video in database:
        if all(i in video.description.lower() or i in video.tags for i in words):
            arr.append(video)
    if len(arr) != 0:
        return random.choice(arr)


def author_search(q):
    arr = []
    for video in database:
        if q.lower().strip() in video.speaker_name.lower():
            arr.append(video)
    if len(arr) != 0:
        return random.choice(arr)


def random_video():
    return random.choice(database)


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def nameyourself(message):
    botan.track(config.botan_key, message.chat.id, message, 'start')
    bot.send_message(message.chat.id,
                     "Hi! I can send you an inspirational video from ted.com. Just type any topic. If you can't choose a topic, please type /random. For more instructions type /help.")


@bot.message_handler(commands=['help'])
def help(message):
    botan.track(config.botan_key, message.chat.id, message, 'help')
    bot.send_message(message.chat.id,
                     "You can just input some key words separated by comma (e.g. 'linguistics, math'), and I'll send you a matching video. Or you can use our advanced search, just type your command before the query.\nHere is the list of possible commands:\n/taglist          If you want examples of topics we have.\n/random       Get random video.\n/tags            Search video by tags.\n/description   Search video by words from description.\n/author         Search video by author.")


@bot.message_handler(commands=['random'])
def rand(message):
    botan.track(config.botan_key, message.chat.id, message, 'random')
    bot.send_message(message.chat.id,
                     random_video().URL)


@bot.message_handler(commands=['tags'])
def rand2(message):
    botan.track(config.botan_key, message.chat.id, message, 'search by tags')
    video = tag_search(message.text.replace('/tags', ''))
    if video is None:
        text = 'Sorry, no matching videos. :('
    else:
        text = video.URL
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['author'])
def rand3(message):
    botan.track(config.botan_key, message.chat.id, message, 'search by author')
    video = author_search(message.text.replace('/author', ''))
    if video is None:
        text = 'Sorry, no matching videos. :('
    else:
        text = video.URL
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['description'])
def rand4(message):
    botan.track(config.botan_key, message.chat.id, message, 'search by description')
    video = description_search(message.text.replace('/description', '')).URL
    if video is None:
        text = 'Sorry, no matching videos. :('
    else:
        text = video.URL
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['taglist'])
def rand(message):
    botan.track(config.botan_key, message.chat.id, message, 'taglist')
    bot.send_message(message.chat.id, get_random_tags())


@bot.message_handler(content_types=["text"])
def getvideo(message):
    botan.track(config.botan_key, message.chat.id, message, 'plain search')
    tags, desc  ='', ''
    kw = get_key_words(message.text)
    tosearch = message.text
    if kw:
        tosearch = ','.join(kw)
    bytags = tag_search(tosearch)
    if bytags is None:
        bydesc = description_search(tosearch)
        if bydesc is None:
            text = 'Sorry, no matching videos. :('
        else:
            text = bydesc.URL
            desc = bydesc.description
            tags = ', '.join(bydesc.tags)
    else:
        text = bytags.URL
        tags = ', '.join(bytags.tags)
        desc = bytags.description
    if text == 'Sorry, no matching videos. :(':
        bot.send_message(message.chat.id, text)
    else:
        collect_message = ''
        if tags:
            collect_message += 'Tags in video: ' + tags + ' \r\n\r\n'
        if desc:
            collect_message += 'Description: ' + desc + '\r\n\r\n'
        bot.send_message(message.chat.id, collect_message + text)
    # bot.send_message(message.chat.id, tosearch + '\r\n\r\n' + tags + ' ' + desc + '\r\n\r\n' + text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
