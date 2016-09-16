# -*- coding: utf-8 -*-
import config
import telebot
import codecs, random, json

f = codecs.open('database.json', 'r', 'utf-8')
database = json.load(f)


def tag_search(q):
    arr = []
    for i in database:
        if q in database[i]['tags']:
            arr.append(database[i]['URL'])
    if len(arr) != 0:
        return random.choice(arr)
    return 'Sorry, no matching videos. :('


def random_video():
    id = random.randint(2, 2257)
    return database[str(id)]['URL']


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
    bot.send_message(message.chat.id, tag_search(message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
