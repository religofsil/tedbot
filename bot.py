# -*- coding: utf-8 -*-
import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def nameyourself(message):
    bot.send_message(message.chat.id, "Hi! I can send you an inspirational video from ted.com. Just type any topic. If you can't choose a topic, please type /random.")

@bot.message_handler(commands=['random'])
def nameyourself(message):
    bot.send_message(message.chat.id, "Hi! I can send you an inspirational video from ted.com. Just type any topic. If you can't choose a topic, please type /random.")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.polling(none_stop=True)