# -*- coding: utf-8 -*-
import config
import telebot
import random
from getdata import _read_data, processRequest
import uuid
from collections import defaultdict

_url = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
_key = 'fc40878d47ed438bb7f229f9ebd34802'

database = _read_data()


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


def tag_search(q):
    q=[i.strip() for i in q.split(',')]
    d=defaultdict(int)
    for video in database:
        for n in q:
            if n in video.tags:
                d[video]+=1
    arr=[]
    if d:
        bestchoice=d[sorted(d, key=lambda x: d[x], reverse=True)[0]]
        for i in d:
            if d[i]==bestchoice:
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


@bot.message_handler(commands=['start', 'help'])
def nameyourself(message):
    bot.send_message(message.chat.id,
                     "Hi! I can send you an inspirational video from ted.com. Just type any topic. If you can't choose a topic, please type /random.")


@bot.message_handler(commands=['random'])
def rand(message):
    bot.send_message(message.chat.id,
                     random_video().URL)

@bot.message_handler(commands=['tags'])
def rand2(message):
    video = tag_search(message.text.replace('/tags', ''))
    if video is None:
        text = 'Sorry, no matching videos. :('
    else:
        text = video.URL
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['author'])
def rand3(message):
    video = author_search(message.text.replace('/author', ''))
    if video is None:
        text = 'Sorry, no matching videos. :('
    else:
        text = video.URL
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['description'])
def rand4(message):
    video = description_search(message.text.replace('/description', '')).URL
    if video is None:
        text = 'Sorry, no matching videos. :('
    else:
        text = video.URL
    bot.send_message(message.chat.id, text)



@bot.message_handler(content_types=["text"])
def getvideo(message):
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
