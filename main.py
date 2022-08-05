import telebot
from telebot import types
from cart_collection import *
from random import randint, shuffle

def work():
    TOKEN = '5516287614:AAG6wkTHwQA_54mB8E-cGMXPZf4Mut6lEU8'
    bot = telebot.TeleBot(TOKEN)
    @bot.message_handler(commands=['start'])
    def start(message):

        bot.send_message(message.chat.id, 'РаzРАБ: @kasskaWD')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        to_start_game = types.KeyboardButton('Начать игру')
        rules = types.KeyboardButton('Правила')
        markup.add(to_start_game, rules)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFdUZi6o1uwTeO0HxGj9hCD0KXhcVSiwACUwAD2xPJCRb-UI1thyzcKQQ')
        bot.send_message(message.chat.id, 'Здравствуйте, желаете начать новую игру?', reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def play(message):
        global gamestarted
        global player_score
        global dugin_score
        global deck
        global player_hand
        if message.text == 'Начать игру':
            gamestarted = True
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFdTZi6owTRYiUU9O1zI8YfWUdLeSMVQACTwAD2xPJCQE3k6xcb3b0KQQ', reply_markup=types.ReplyKeyboardRemove())
            deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
            shuffle(deck)
            dugin_hand = []
            while calkulate_score(dugin_hand) < 17:
                cart = randint(1, len(deck)-1)
                if cart in deck:
                    new_cart = deck.pop(cart)
                    dugin_hand.append(carts[new_cart])

            player_hand = []
            while len(player_hand) < 2:
                cart = randint(1, len(deck)-1)
                if cart in deck:
                    new_cart = deck.pop(cart)
                    player_hand.append(carts[new_cart])

            bot.send_message(message.chat.id, 'Ваши карты: ')
            bot.send_sticker(message.chat.id, stickers[player_hand[0]])
            bot.send_sticker(message.chat.id, stickers[player_hand[1]])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            stop = types.KeyboardButton('Хватит')
            take_more = types.KeyboardButton('Взять ещё!')
            markup.add(stop, take_more)
            player_score = calkulate_score(player_hand)
            dugin_score = calkulate_score(dugin_hand)
            bot.send_message(message.chat.id, 'Ваш счёт: ' + str(player_score), reply_markup=markup)
            
        if message.text == 'Правила':
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFdUJi6o1A9lDkAcFBOeqnXGEx7Rc1-AACVQAD2xPJCcr0vjU_HuS9KQQ')
            bot.send_message(message.chat.id, 'Правил нет')

        try:
            if message.text == 'Взять ещё!' and gamestarted:
                new_cart = deck.pop()
                player_hand.append(carts[new_cart])
                player_score = calkulate_score(player_hand)
                bot.send_sticker(message.chat.id, stickers[player_hand[-1]])
                if player_score > 21:
                    gamestarted = False
                    bot.send_message(message.chat.id, f'Ваш счёт: {player_score}, Вы проиграли', reply_markup=types.ReplyKeyboardRemove())
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    to_start_game = types.KeyboardButton('Начать игру')
                    rules = types.KeyboardButton('Правила')
                    markup.add(to_start_game, rules)
                    bot.send_message(message.chat.id, 'Желаете сыграть ещё?', reply_markup=markup)
                elif player_score == 21:
                    gamestarted = False
                    if player_score > dugin_score or dugin_score > 21:
                        bot.send_message(message.chat.id, f'Ваш счёт: {player_score}\nМой счёт: {dugin_score}\nВы выиграли', reply_markup=types.ReplyKeyboardRemove())
                    elif player_score == dugin_score:
                        bot.send_message(message.chat.id, f'Ваш счёт: {player_score}\nМой счёт: {dugin_score}\nНичья', reply_markup=types.ReplyKeyboardRemove())
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    to_start_game = types.KeyboardButton('Начать игру')
                    rules = types.KeyboardButton('Правила')
                    markup.add(to_start_game, rules)
                    bot.send_message(message.chat.id, 'Желаете сыграть ещё?', reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, f'Ваш счёт: {player_score}')
            if message.text == 'Хватит' and gamestarted:
                if player_score > dugin_score or dugin_score > 21:
                    bot.send_message(message.chat.id, f'Ваш счёт: {player_score}\nМой счёт: {dugin_score}\nВы выиграли', reply_markup=types.ReplyKeyboardRemove())
                elif player_score == dugin_score:
                    bot.send_message(message.chat.id, f'Ваш счёт: {player_score}\nМой счёт: {dugin_score}\nНичья', reply_markup=types.ReplyKeyboardRemove())
                else:
                    bot.send_message(message.chat.id, f'Ваш счёт: {player_score}\nМой счёт: {dugin_score}\nВы проиграли', reply_markup=types.ReplyKeyboardRemove())
                gamestarted = False
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                to_start_game = types.KeyboardButton('Начать игру')
                rules = types.KeyboardButton('Правила')
                markup.add(to_start_game, rules)
                bot.send_message(message.chat.id, 'Желаете сыграть ещё?', reply_markup=markup)
        except Exception as e:
            print(e)

    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(e)

def calkulate_score(hand):
    score = 0
    scores = []
    aces = 0
    for cart in hand:
        if cart[0] == 'A':
            aces += 1
        else:
            score += cart_cost[cart[0]]
    if aces > 0:
        for i in range(aces+1):
            cur_score = score + (10 * (aces - i)) + (1 * i)
            if cur_score < 22:
                return cur_score
        return cur_score
    return score

def lose_check(score):
    return score > 21


if __name__ == "__main__":
    gamestarted = False
    work()
