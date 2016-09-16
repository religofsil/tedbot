# -*- coding: utf-8 -*-
import config
import telebot
import random, codecs
from getdata import _read_data, Video

database = _read_data()

def get_random_tags():
    f=codecs.open('taglist.txt', 'r', 'utf-8')
    all_tags=[]
    for line in f:
        all_tags.append(line.strip())
    random.shuffle(all_tags)
    final_string=", ".join(all_tags[:20])
    final_string='Here are some topics that might get your attention:\n\n'+final_string
    return final_string

def tag_search(q):
    q=q.lower()
    q=[i.strip() for i in q.split(',')]
    d={}
    for video in database:
        d[video.URL]=0
        for n in q:
            if n in video.tags:
                d[video.URL]+=1
    arr=[]
    bestchoice=d[sorted(d, key=d.get, reverse=True)[0]]
    for i in d:
        if d[i]==bestchoice:
            arr.append(i)
    return random.choice(arr)


def description_search(q):
    arr = []
    for video in database:
        if q.lower().strip() in video.description.lower():
            arr.append(video.URL)
    if len(arr) != 0:
        return random.choice(arr)


def author_search(q):
    arr = []
    for video in database:
        if q.lower().strip() in video.speaker_name.lower():
            arr.append(video.URL)
    if len(arr) != 0:
        return random.choice(arr)


def random_video():
    return random.choice(database).URL


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def nameyourself(message):
    bot.send_message(message.chat.id,
                     "Hi! I can send you an inspirational video from ted.com. Just type any topic. If you can't choose a topic, please type /random. For more instructions type /help.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     "You can just input some key words separated by comma (e.g. 'linguistics, math'), and I'll send you a matching video. Or you can use our advanced search, just type your command before the query.\nHere is the list of possible commands:\n/taglist          If you want examples of topics we have.\n/random       Get random video.\n/tags            Search video by tags.\n/description   Search video by words from description.\n/author         Search video by author.")


@bot.message_handler(commands=['random'])
def rand(message):
    bot.send_message(message.chat.id,
                     random_video())

@bot.message_handler(commands=['tags'])
def rand(message):
    text = tag_search(message.text.replace('/tags', ''))
    if text is None:
        text = 'Sorry, no matching videos. :('
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['author'])
def rand(message):
    text = author_search(message.text.replace('/author', ''))
    if text is None:
        text = 'Sorry, no matching videos. :('
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['description'])
def rand(message):
    text = description_search(message.text.replace('/description', ''))
    if text is None:
        text = 'Sorry, no matching videos. :('
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['taglist'])
def rand(message):
    bot.send_message(message.chat.id, get_random_tags())

@bot.message_handler(content_types=["text"])
def getvideo(message):
    bytags = tag_search(message.text)
    if bytags is None:
        bydesc = description_search(message.text)
        if bydesc is None:
            text = 'Sorry, no matching videos. :('
        else:
            text = bydesc
    else:
        text = bytags
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
