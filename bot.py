# -*- coding: utf-8 -*-
import config
import telebot
import random
from getdata import _read_data, Video

database = _read_data()


def tag_search(q):
    arr = []
    for video in database:
        if q in video.tags:
            arr.append(video.URL)
    if len(arr) != 0:
        return random.choice(arr)
    return 'Sorry, no matching videos. :('


def random_video():
    return random.choice(database).URL


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def nameyourself(message):
    bot.send_message(message.chat.id,
                     "Hi! I can send you an inspirational video from ted.com. Just type any topic. If you can't choose a topic, please type /random.")


@bot.message_handler(commands=['random'])
def rand(message):
    bot.send_message(message.chat.id,
                     random_video())


@bot.message_handler(content_types=["text"])
def getvideo(message):
    bot.send_message(message.chat.id, tag_search(message.text.lower()))


if __name__ == '__main__':
    bot.polling(none_stop=True)
