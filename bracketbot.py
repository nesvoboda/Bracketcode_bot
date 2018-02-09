
# -*- coding: utf-8 -*-

import telebot
from telebot import types

bot = telebot.TeleBot("541518629:AAGB69rWGVIcC4bI9piEGaF-tew8iIDBem0")

slov = [['а', ')((((('],
['б', ')(((()'],
['в', ')((())'],
['г', ')(()))'],
['д', ')())))'],
['е', '))(((('],
['ё', ')))((('],
['ж', '))))(('],
['з', ')))))('],
['и', '))))))'],
['й', '))()))'],
['к', ')))())'],
['л', '))))()'],
['м', ')()((('],
['н', ')(()(('],
['о', ')((()('],
['п', '((((()'],
['р', ')))()('],
['с', '))(()('],
['т', '))()(('],
['у', ')())(('],
['ф', ')()()('],
['х', '))((()'],
['ц', ')(())('],
['ч', '(())(('],
['ш', ')()())'],
['щ', '))())('],
['ъ', ')))(()'],
['ы', '())(()'],
['ь', '())))('],
['э', '()())('],
['ю', '()((()'],
['я', '()(())']]

i = 0
y = 0
result = ""
switch = None

def perevesti(message):

    i = 0
    y = 0
    z = 0
    result = ""
    query = message.text

    while i <= len(query):
        for y in range(0,32):
            if query[i:i+6] == slov[y][1]:
                result = result + slov[y][0]
                z = z + 1
                break
            y += 1
        i = i + 6

    bot.send_message(message.chat.id, result)

def zakodirovat(message):

    i = 0
    y = 0
    z = 0
    result = ""
    query = message.text

    for i in range(len(query)):
        for y in range(0,32):
            if query[i] == slov[y][0]:
                result = result + slov[y][1]
                break
            y += 1

    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    bot.reply_to(message, "Привет! Этот бот умеет переводить с русского на язык скобочек и наоборот.")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Закодировать')
    itembtn2 = types.KeyboardButton('Перевести на русский')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Что нужно сделать?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == u"Закодировать")
def zakod(message):
    switch = 0
    msg = bot.send_message(message.chat.id, "Окей. Говорите, что нужно закодировать")
    bot.send_message(message.chat.id, switch)
    bot.register_next_step_handler(msg, zakodirovat)


@bot.message_handler(func=lambda message: message.text == u"Перевести на русский")
def hui(message):
    switch = 1

    msg = bot.send_message(message.chat.id, "Окей. Говорите, что нужно перевести")
    bot.send_message(message.chat.id, switch)
    bot.register_next_step_handler(msg, perevesti)


def handle_input(message):
    if switch == 0:
        bot.send_message(message.chat.id, zakodirovat(message.text))
    elif switch == 1:
        bot.send_message(message.chat.id, perevesti(message.text))


#@bot.message_handler(func=lambda message: int(message.message_id) >= otschet)
#def poluch(message):
#    bot.reply_to(message, "ура блэд")



bot.polling()
