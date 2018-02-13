
# -*- coding: utf-8 -*- 

# so that it works well with russian

import telebot # best telegram bot api realisation for python
from telebot import types
import os
token = os.environ['BOT_API_TOKEN'] # token stored in environment variable so that you don't steal it
 
bot = telebot.TeleBot(token)
slov = [['а', ')((((('], # this encoding table is flawed, I know. ping me if you want to improve it.
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
['я', '()(())'],
[' ', '()()))']]

i = 0
y = 0
result = "" # this will be refactored in the future


def translate(message): # this method handles translation into russian

    i = 0
    y = 0
    z = 0
    result = ""
    query = message.text

    while i <= len(query):
        for y in range(0,34):
            if query[i:i+6] == slov[y][1]:
                result = result + slov[y][0]
                z = z + 1
                break
            y += 1
        i = i + 6

        #the following trick is very important as trying to send an empty message will result in an error.
        
    if result == "":
        bot.send_message(message.chat.id, "Ой! Кажется, результат перевода не содержит символов. Я могу переводить на русский только с языка скобочек.\nПожалуйста, попробуйте еще раз.")
        try_again(message)

    else:
        bot.send_message(message.chat.id, result)
        what_next(message)

def encd(message): # this method handles encoding the message

    i = 0
    y = 0
    z = 0
    result = ""
    query = message.text

    for i in range(len(query)):
        for y in range(0,34):
            if query[i] == slov[y][0]:
                result = result + slov[y][1]
                break
            y += 1
            
            # again, protection against empty messages.
            
    if result == "":
        bot.send_message(message.chat.id, "Ой! Кажется, результат кодировки не содержит символов. \nЗакодировать можно только строчные русские буквы и пробел.\nПопробуйте еще раз.")
        try_again(message)

    else:
        bot.send_message(message.chat.id, result)
        what_next(message)

@bot.message_handler(commands=['start', 'help']) # this handler handles the welcome message.
def send_welcome(message):

    bot.reply_to(message, "Привет! Этот бот умеет переводить с русского на язык скобочек и наоборот.") # welcome message
    
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Закодировать')
    itembtn2 = types.KeyboardButton('Перевести на русский') # mode selector keyboard 
    itembtn3 = types.KeyboardButton('Показать словарь')
    markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id, "Что нужно сделать?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == u"Закодировать") # encoding mode handling
def encode_handler(message):
    
    nomar = types.ReplyKeyboardRemove() # don't forget to remove the mode selector keyboard so that the user can type 
    msg = bot.send_message(message.chat.id, "Окей. Пришлите следующим сообщением то, что нужно закодировать. \nЯ принимаю только строчные русские буквы и пробелы.", reply_markup=nomar)

    bot.register_next_step_handler(msg, encd) #send next message to encd method


@bot.message_handler(func=lambda message: message.text == u"Перевести на русский") # translate mode handler
def translate_handle(message):
    
    nomar = types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, "Окей. Пришлите следующим сообщением то, что нужно перевести на русский.", reply_markup=nomar)

    bot.register_next_step_handler(msg, perevesti)

@bot.message_handler(func=lambda message: message.text == u"Показать словарь")
def dictionary_handler(message):
    
    result = ""
    for y in range(0,34):
        result = result + slov[y][0] + " — " + slov[y][1] + "\n"
    bot.send_message(message.chat.id, result)
    what_next(message)

@bot.message_handler(func=lambda message: message.text == u"Нет, всё. Пока!") # goodbye handler
def poka(message):
    
    nomar = types.ReplyKeyboardRemove() # don't forget to hide the mode selector keyboard, just in case
    msg = bot.send_message(message.chat.id, "Пока!\nЕсли я понадоблюсь снова, напишите: /start", reply_markup=nomar) # don't forget to let your users get back to the bot

@bot.message_handler(func=lambda message: message.from.id == "TESTER_ID") # respond to automatic testing bot
def respond(message):
    
    cipher = int(message.text)
    bot.send_message(message.chat.id, cipher + 1)
    
def try_again(message):
    
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Закодировать')
    itembtn2 = types.KeyboardButton('Перевести на русский')
    itembtn3 = types.KeyboardButton('Показать словарь')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Что нужно сделать?", reply_markup=markup)

def what_next(message):
    
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Закодировать')
    itembtn2 = types.KeyboardButton('Перевести на русский')
    itembtn3 = types.KeyboardButton('Показать словарь')
    itembtn4 = types.KeyboardButton('Нет, всё. Пока!')
    markup.row(itembtn1, itembtn2)
    markup.row(itembtn3)
    markup.row(itembtn4)
    bot.send_message(message.chat.id, "Что-то еще?", reply_markup=markup)


bot.polling() # start bot
