# -*- coding: utf8 -*-

import json
import os

import telebot
from botInfo import bot
import pymysql.cursors
from keyBoards import main_menu, game_keyboard, free_game_keyboard, play_keyboard_free, language_select_keyboard, \
    profile_keyboard, play_keyboard_free_8_8, duel_keyboard, fastgame_keyboard, turnir16_keyboard, turnir32_keyboard, \
    turnir64_keyboard, turnir256_keyboard, turnir1024_keyboard, turnir_keyboard
from telebot.types import LabeledPrice, ShippingOption
import time
from turnir import turnir
from texts import rules
from datetime import datetime
import random
from battle import start_battle, vote_handler
from sendEmail import default_email, default_password, send_email1, default_receive
from duel import duel
from fastgame import fastgame
from threading import Timer
from battle import battle


# def main(ev, req):
#     request_body_dict = req.get_json()
#     update = telebot.types.Update.de_json(request_body_dict)
#     bot.process_new_messages([update.message])

connection = pymysql.connect(
                             host='us-cdbr-east-02.cleardb.com',
                             user='bf7c55efe60aa8',
                             password='f5721000',
                             db='heroku_d166a25f7ae34c1',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



provider_token = '410694247:TEST:1a003bbe-0045-41f0-91bf-5fd08b143463'
name = ''
language = ''
number_of_money = 0


def check_user_win(users, type):
    result = ''
    if users['first_user_check'] == 1 and users['second_user_check'] == 1:
        result = 'draw'
    elif users['first_user_check'] == 1 and users['second_user_check'] == 2:
        result = 'first_lose'
    elif users['first_user_check'] == 1 and users['second_user_check'] == 3:
        result = 'first_win'

    if users['first_user_check'] == 2 and users['second_user_check'] == 1:
        result = 'first_win'
    elif users['first_user_check'] == 2 and users['second_user_check'] == 2:
        result = 'draw'
    elif users['first_user_check'] == 2 and users['second_user_check'] == 3:
        result = 'first_lose'

    if users['first_user_check'] == 3 and users['second_user_check'] == 1:
        result = 'first_lose'
    elif users['first_user_check'] == 3 and users['second_user_check'] == 2:
        result = 'first_win'
    elif users['first_user_check'] == 3 and users['second_user_check'] == 3:
        result = 'draw'

    if result == 'draw':
        time.sleep(15)
        with connection.cursor() as cursor:
            sql = "DELETE FROM `current_game`  WHERE id=%s"
            cursor.execute(sql, users['id'])
        connection.commit()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `current_game` (`first_user`, `second_user`, ) VALUES (%s, %s)"
            cursor.execute(sql, (users['first_user'], users['second_user']))
        connection.commit()
        bot.send_message(users['first_user'], text='Нічия спробуйте знову...', reply_markup=play_keyboard_free())
        bot.send_message(users['second_user'], text='Нічия спробуйте знову...', reply_markup=play_keyboard_free())
    if result == 'first_lose':
        time.sleep(15)
        bot.send_message(users['first_user'], text='Ви програли!')
        bot.send_message(users['second_user'], text='Ви виграли!')
        with connection.cursor() as cursor:
            sql = "DELETE FROM `current_game`  WHERE id=%s"
            cursor.execute(sql, users['id'])
        connection.commit()
    if result == 'first_win':
        time.sleep(15)
        bot.send_message(users['first_user'], text='Ви виграли!')
        bot.send_message(users['second_user'], text='Ви програли!')
        with connection.cursor() as cursor:
            sql = "DELETE FROM `current_game`  WHERE id=%s"
            cursor.execute(sql, users['id'])
        connection.commit()


@bot.callback_query_handler(func=lambda call: 'free_8_8' in call.data)
def callback_worker(call):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `free_game_8_8` WHERE user_id=%s"
        cursor.execute(sql, call.message.chat.id)
        result = cursor.fetchall()
    if result[0]['user_select'] is None:
        if call.data == "paper_free_8_8":
            with connection.cursor() as cursor:
                sql = "UPDATE `free_game_8_8` SET user_select= %s WHERE user_id=%s"
                cursor.execute(sql, (1, result[0]['user_id']))
                sql = "UPDATE `free_game_8_8` SET enemy_select= %s WHERE enemy_id=%s"
                cursor.execute(sql, (1, result[0]['enemy_id']))
            connection.commit()
        elif call.data == 'scissors_free_8_8':
            with connection.cursor() as cursor:
                sql = "UPDATE `free_game_8_8` SET user_select= %s WHERE user_id=%s"
                cursor.execute(sql, (2, result[0]['second_user']))
                sql = "UPDATE `free_game_8_8` SET enemy_select= %s WHERE enemy_id=%s"
                cursor.execute(sql, (2, result[0]['enemy_id']))
            connection.commit()
        elif call.data == 'stone_free_8_8':
            with connection.cursor() as cursor:
                sql = "UPDATE `free_game_8_8` SET user_select= %s WHERE user_id=%s"
                cursor.execute(sql, (3, result[0]['second_user']))
                sql = "UPDATE `free_game_8_8` SET enemy_select= %s WHERE enemy_id=%s"
                cursor.execute(sql, (3, result[0]['enemy_id']))
            connection.commit()
    else:
        bot.send_message(call.message.chat.id, text='Ви уже зробили свій вибір.')


@bot.callback_query_handler(func=lambda call: 'free_1_1' in call.data)
def callback_worker(call):
    global language
    if call.data == "paper_free_1_1":
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `current_game` WHERE first_user=%s"
            cursor.execute(sql, call.message.chat.id)
            result = cursor.fetchall()
        if result.__len__() == 0:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `current_game` WHERE second_user=%s"
                cursor.execute(sql, call.message.chat.id)
                result = cursor.fetchall()
            if result.__len__() == 0:
                bot.send_message(call.message.chat.id, text='Ви не берете участь у жодній грі', reply_markup=game_keyboard())
            else:
                if result[0]['first_user_check'] is None and result[0]['second_user_check'] is None:
                    with connection.cursor() as cursor:
                        sql = "UPDATE `current_game` SET second_user_check= %s WHERE second_user=%s"
                        cursor.execute(sql, (1, result[0]['second_user']))
                    connection.commit()
                    bot.send_message(call.message.chat.id,
                                     text='Ваша відповідь врахована очікуйте ходу від суперника')
                elif result[0]['first_user_check'] is None:
                    bot.send_message(call.message.chat.id, text='Ви уже зробили свій вибір, очікуйте поки суперник зробить свій вибір.')
                else:
                    result[0]['second_user_check'] = 1
                    check_user_win(result[0], 'free_1_1')
        else:
            if result[0]['first_user_check'] is None and result[0]['second_user_check'] is None:
                with connection.cursor() as cursor:
                    sql = "UPDATE `current_game` SET first_user_check= %s WHERE second_user=%s"
                    cursor.execute(sql, (1, result[0]['second_user']))
                connection.commit()
                bot.send_message(call.message.chat.id,
                                 text='Ваша відповідь врахована очікуйте ходу від суперника')
            elif result[0]['second_user_check'] is None:
                bot.send_message(call.message.chat.id,
                                 text='Ви уже зробили свій вибір, очікуйте поки суперник зробить свій вибір.')
            else:
                result[0]['first_user_check'] = 1
                check_user_win(result[0], 'free_1_1')
    elif call.data == 'scissors_free_1_1':
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `current_game` WHERE first_user=%s"
            cursor.execute(sql, call.message.chat.id)
            result = cursor.fetchall()
        if result.__len__() == 0:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `current_game` WHERE second_user=%s"
                cursor.execute(sql, call.message.chat.id)
                result = cursor.fetchall()
            if result.__len__() == 0:
                bot.send_message(call.message.chat.id, text='Ви не берете участь у жодній грі', reply_markup=game_keyboard())
            else:
                if result[0]['first_user_check'] is None and result[0]['second_user_check'] is None :
                    with connection.cursor() as cursor:
                        sql = "UPDATE `current_game` SET second_user_check= %s WHERE second_user=%s"
                        cursor.execute(sql, (2, result[0]['second_user']))
                    connection.commit()
                    bot.send_message(call.message.chat.id,
                                     text='Ваша відповідь врахована очікуйте ходу від суперника')
                elif result[0]['first_user_check'] is None:
                    bot.send_message(call.message.chat.id, text='Ви уже зробили свій вибір, очікуйте поки суперник зробить свій вибір.')
                else:
                    result[0]['second_user_check'] = 2
                    check_user_win(result[0], 'free_1_1')
        else:
            if result[0]['first_user_check'] is None and result[0]['second_user_check'] is None:
                with connection.cursor() as cursor:
                    sql = "UPDATE `current_game` SET first_user_check= %s WHERE second_user=%s"
                    cursor.execute(sql, (2, result[0]['second_user']))
                connection.commit()
                bot.send_message(call.message.chat.id,
                                 text='Ваша відповідь врахована очікуйте ходу від суперника')
            elif result[0]['second_user_check'] is None:
                bot.send_message(call.message.chat.id,
                                 text='Ви уже зробили свій вибір, очікуйте поки суперник зробить свій вибір.')
            else:
                result[0]['first_user_check'] = 2
                check_user_win(result[0], 'free_1_1')


    elif call.data == 'stone_free_1_1':
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `current_game` WHERE first_user=%s"
            cursor.execute(sql, call.message.chat.id)
            result = cursor.fetchall()
        if result.__len__() == 0:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `current_game` WHERE second_user=%s"
                cursor.execute(sql, call.message.chat.id)
                result = cursor.fetchall()
            if result.__len__() == 0:
                bot.send_message(call.message.chat.id, text='Ви не берете участь у жодній грі', reply_markup=game_keyboard())
            else:
                if result[0]['first_user_check'] is None and result[0]['second_user_check'] is None :
                    with connection.cursor() as cursor:
                        sql = "UPDATE `current_game` SET second_user_check= %s WHERE second_user=%s"
                        cursor.execute(sql, (3, result[0]['second_user']))
                    connection.commit()
                elif result[0]['first_user_check'] is None:
                    bot.send_message(call.message.chat.id, text='Ви уже зробили свій вибір, очікуйте поки суперник зробить свій вибір.')
                else:
                    result[0]['second_user_check'] = 3
                    check_user_win(result[0], 'free_1_1')
        else:
            if result[0]['first_user_check'] is None and result[0]['second_user_check'] is None:
                with connection.cursor() as cursor:
                    sql = "UPDATE `current_game` SET first_user_check= %s WHERE second_user=%s"
                    cursor.execute(sql, (3, result[0]['second_user']))
                connection.commit()
            elif result[0]['second_user_check'] is None:
                bot.send_message(call.message.chat.id,
                                 text='Ви уже зробили свій вибір, очікуйте поки суперник зробить свій вибір.')
            else:
                result[0]['first_user_check'] = 3
                check_user_win(result[0], 'free_1_1')





@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `users` WHERE `id`=%s"
            cursor.execute(sql, (message.from_user.id,))
            result = cursor.fetchall()
        if result.__len__() == 0:
            bot.send_message(message.from_user.id, "Оберіть мову:", reply_markup=language_select_keyboard())
        else:
            bot.send_message(message.chat.id, 'Меню:', reply_markup=main_menu())
    elif message.text == 'Грати':
        bot.send_message(message.from_user.id, text='За що змагаємося: ', reply_markup=game_keyboard())
    elif message.text == 'Профіль':
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `users` WHERE `id`=%s"
                cursor.execute(sql, (message.from_user.id,))
                result = cursor.fetchall()
        finally:
            name = result[0]['name']
            money = result[0]['money']
            reserved = result[0]['reserv_to_withdraw']
            text = f'Ім\'я: {name}\nГаманець: {money} тунгрики(need change) \nРезерв на виведення: {reserved}'
            bot.send_message(message.from_user.id, text=text, reply_markup=profile_keyboard())
    elif message.text == 'Правила':
        bot.send_message(message.from_user.id, text=rules, reply_markup=main_menu())
    elif message.text == "Зворотній зв'язок":
        bot.send_message(message.from_user.id, text='Введіть текст який хочете нам надіслати:',)
        bot.register_next_step_handler(message, callback=send_email)


def send_email(message):
    send_email1(default_email, default_password, default_receive, "Call back", message.text)

def get_language(message):
    global language

def get_name(message):
    global name
    name = message.text
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `users` (`id`, `name`, `money`, `language`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (message.from_user.id, name, '0', language))
        connection.commit()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `users`"
            cursor.execute(sql)
    finally:
     bot.send_message(message.from_user.id, text='Меню:', reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: 'free_game' in call.data)
def callback_worker(call):
    if call.data == "free_game":
        bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=free_game_keyboard())
    if call.data == 'free_game_1_1':
        free_game_1_1(call)
    if call.data == 'free_game_8_8':
        free_game_8_8(call)

@bot.callback_query_handler(func=lambda call: 'duel' in call.data)
def callback_worker(call):
    if call.data == "duel":
        bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=duel_keyboard())
    if call.data == 'duel25':
        turnir(call, 2, 25)
    elif call.data == 'duel50':
        turnir(call, 2, 50)
    elif call.data == 'duel100':
        turnir(call, 2, 100)
    elif call.data == 'duel1000':
        turnir(call, 2, 1000)


@bot.callback_query_handler(func=lambda call: 'turnir' in call.data)
def callback_worker(call):
    if call.data == 'turnir':
        bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=turnir_keyboard())
    elif 'turnir16' in call.data:
        if call.data == 'turnir16':
            bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=turnir16_keyboard())
        elif call.data == 'turnir1625':
            turnir(call, 16, 25)
        elif call.data == 'turnir1650':
            turnir(call, 16, 50)
        elif call.data == 'turnir16100':
            turnir(call, 16, 100)
    elif 'turnir32' in call.data:
        if call.data == 'turnir32':
            bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=turnir32_keyboard())
        elif call.data == 'turnir3225':
            turnir(call, 32, 25)
        elif call.data == 'turnir3250':
            turnir(call, 32, 50)
        elif call.data == 'turnir32100':
            turnir(call, 32, 100)
    elif 'turnir64' in call.data:
        if call.data == 'turnir64':
            bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=turnir64_keyboard())
        elif call.data == 'turnir6425':
            turnir(call, 64, 25)
        elif call.data == 'turnir6450':
            turnir(call, 64, 50)
        elif call.data == 'turnir64100':
            turnir(call, 64, 100)
    elif 'turnir256' in call.data:
        if call.data == 'turnir256':
            bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=turnir256_keyboard())
        elif call.data == 'turnir25625':
            turnir(call, 256, 25)
        elif call.data == 'turnir25650':
            turnir(call, 256, 50)
        elif call.data == 'turnir256100':
            turnir(call, 256, 100)
    elif 'turnir1024' in call.data:
        if call.data == 'turnir1024':
            bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=turnir1024_keyboard())
        elif call.data == 'turnir102425':
            turnir(call, 1024, 25)
        elif call.data == 'turnir102450':
            turnir(call, 1024, 50)
        elif call.data == 'turnir1024100':
            turnir(call, 1024, 100)

@bot.callback_query_handler(func=lambda call: 'fastgame' in call.data)
def callback_worker(call):
    if call.data == "fastgame":
        bot.send_message(call.message.chat.id, text='Оберіть: ', reply_markup=fastgame_keyboard())
    if call.data == 'fastgame25':
        turnir(call, 8, 25)
    elif call.data == 'fastgame50':
        turnir(call, 8, 50)
    elif call.data == 'fastgame100':
        turnir(call, 8, 100)


@bot.callback_query_handler(func=lambda call: 'language' in call.data)
def callback_worker(call):
    global language
    if call.data == "language_ua":
        language = 'ua'
        bot.send_message(call.message.chat.id, text='Як вас називати?')
        bot.register_next_step_handler(call.message, callback=get_name)
    if call.data == 'language_ru':
        language = 'ru'
        bot.send_message(call.message.chat.id, text='Как вас называть?')
        bot.register_next_step_handler(call.message, callback=get_name)

@bot.callback_query_handler(func=lambda call: 'money' in call.data)
def callback_worker(call):
    if call.data == 'add_some_money':
        bot.send_message(call.message.chat.id, text='Введіть суму:')
        bot.register_next_step_handler(call.message, callback=get_number_of_money)
    elif call.data == 'withdraw_money':
        bot.send_message(call.message.chat.id, text='Введіть суму:')
        bot.register_next_step_handler(call.message, callback=credit_card_input)

def credit_card_input(message):
    global number_of_money
    try:
        number_of_money = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, text='Помилка при введені суми')
        bot.register_next_step_handler(message, callback=credit_card_input)
    else:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `users` WHERE id=%s"
            cursor.execute(sql, (message.from_user.id))
            result = cursor.fetchall()
        if result[0]['credit_card'] is None:
            bot.send_message(message.from_user.id, text='Введіть кредитну карту')
            bot.register_next_step_handler(message, callback=withdraw_money)
        else:
            withdraw_money(message, default=False)

def withdraw_money(message, default = True):
    global number_of_money
    if default:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `users` WHERE id=%s"
            cursor.execute(sql, (message.from_user.id))
            result = cursor.fetchall()
            money = result[0]['money'] - number_of_money
            reserv = result[0]['reserv_to_withdraw'] + number_of_money
            sql = "UPDATE `users` SET money= %s, reserv_to_withdraw = %s, credit_card = %s WHERE id=%s"
            cursor.execute(sql, (money, reserv, message.text, result[0]['id']))
        connection.commit()
        bot.send_message(message.from_user.id, text='Запит на виведення коштів відправлено')
    else:
        try:
            number_of_money = int(message.text)
        except ValueError:
            bot.send_message(message.from_user.id, text='Помилка при введені суми')
            bot.register_next_step_handler(message, callback=withdraw_money)
        else:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `users` WHERE id=%s"
                cursor.execute(sql, (message.from_user.id))
                result = cursor.fetchall()
            if result[0]['money'] < number_of_money:
                bot.send_message(message.from_user.id, text='У вас недостатньо коштів')
                bot.register_next_step_handler(message, callback=withdraw_money)
            else:
                with connection.cursor() as cursor:
                    money = result[0]['money'] - number_of_money
                    reserv = result[0]['reserv_to_withdraw'] + number_of_money
                    sql = "UPDATE `users` SET money= %s, reserv_to_withdraw = %s WHERE id=%s"
                    cursor.execute(sql, (money, reserv, result[0]['id']))
                connection.commit()
                bot.send_message(message.from_user.id, text='Запит на виведення коштів відправлено')


@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3'])
def callback_worker(call):
    vote_handler(call)


def get_number_of_money(message):
    global number_of_money
    try:
        number_of_money = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, text='Помилка при введені суми')
        bot.register_next_step_handler(message, callback=get_number_of_money)
    else:
        prices = [LabeledPrice(label='Поповнення рахунку', amount=number_of_money*100)]
        bot.send_message(message.chat.id,
                         "Зараз платежі приймаються лише в тестовому режимі"
                         "\n\nВаш тестовий платіж:", parse_mode='Markdown')
        bot.send_invoice(message.chat.id, title='Working Time Machine',
                         description=' Поповнення рахунку',
                         provider_token=provider_token,
                         currency='UAH',
                         photo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQP9bwtPnfeODkt-vJyBYpYDjStfrRMB5UQ4w&usqp=CAU',
                         photo_height=0,  # !=0/None or picture won't be shown
                         photo_width=0,
                         photo_size=0,
                         is_flexible=False,  # True If you need to set up Shipping Fee
                         prices=prices,
                         start_parameter='time-machine-example',
                         invoice_payload='HAPPY FRIDAYS COUPON')


def free_game_8_8(call):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `free_game_8_8`"  # WHERE game_id is NULL"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `free_game_8_8` WHERE user_id = %s"
            cursor.execute(sql, call.message.chat.id )
            result_user_exist = cursor.fetchall()
        if result_user_exist.__len__() != 0:
            bot.send_message(call.message.chat.id, text="""Ви уже зареєстровані очікуйте всіх гравців""")
        else:
            if result.__len__() < 7: #must be 7
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `free_game_8_8` (`user_id`) VALUES (%s)"
                    cursor.execute(sql, call.message.chat.id)
                connection.commit()
                bot.send_message(call.message.chat.id, text="""Коли всі зберуться ми повідомимо тебе  за годину до початку.
                Поки чекаєш — заходь в наш - чат, де можна поспілкуватися з іншими учасниками!""")
            else:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `free_game_8_8` (`user_id`) VALUES (%s)"
                    cursor.execute(sql, call.message.chat.id)
                connection.commit()
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `free_game_8_8`"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                time.sleep(3540)
                send_message_one_ours_ready(result)
                time.sleep(60)
                send_message_one_minutes_ready(result)
                start_battle(result)



def send_message_one_ours_ready(users):
    for u in users:
        bot.send_message(u['user_id'], text=f"""Старт через годину.""")


def send_message_one_minutes_ready(users):
    for u in users:
        bot.send_message(u['user_id'], text=f"""Старт через годину.""")


def send_message_ready(dateOfStart, databaseName, gameId, users, pause):
    dt_object = datetime.fromtimestamp(dateOfStart)
    for u in users:
        bot.send_message(u['user_id'], text=f"""Розіграш на який ви зареєструвались, набрав необхідну кількість людей 
        Старт заплановано на : {dt_object}.""")
    time.sleep(pause)
    send_message_one_ours_ready(users)
    time.sleep(3540)
    send_message_one_minutes_ready(users)
    time.sleep(60)
    for u in users:
        bot.send_message(u['user_id'], text=f"""Турнір на який ви зареєструвалися розпочався, у вас є лише 30 
        секунд щоб зробити свій вибір""", reply_markup=play_keyboard_free_8_8())
    time.sleep(30)
    make_function(databaseName, gameId, play_keyboard_free_8_8, 0)


def check_user_vote(users, database):
    for u in users:
        if u['user_select'] is None:
            select = random.randint(1, 3)
            with connection.cursor() as cursor:
                sql = f"UPDATE {database} SET user_select= %s WHERE user_id=%s"
                cursor.execute(sql, (select, u['user_id']))
                sql = f"UPDATE {database} SET enemy_select= %s WHERE enemy_id=%s"
                cursor.execute(sql, (select, u['user_id']))
            connection.commit()


def check_user_win_db(users, database, key_board):
    result = ''
    for u in users:
        u_select = u['user_select']
        e_select = u['enemy_select']
        if u_select == 1 and e_select == 1:
            result = 'draw'
        elif u_select == 1 and e_select == 2:
            result = 'first_lose'
        elif u_select == 1 and e_select == 3:
            result = 'first_win'

        if u_select == 2 and e_select == 1:
            result = 'first_win'
        elif u_select == 2 and e_select == 2:
            result = 'draw'
        elif u_select == 2 and e_select == 3:
            result = 'first_lose'

        if u_select == 3 and e_select == 1:
            result = 'first_lose'
        elif u_select == 3 and e_select == 2:
            result = 'first_win'
        elif u_select == 3 and e_select == 3:
            result = 'draw'
        time.sleep(15)
        if result == 'first_win':
            bot.send_message(u['user_id'], text='Ви пройшли в наступний раунд( модифікувати)', reply_markup=key_board)
            with connection.cursor() as cursor:
                sql = f"UPDATE {database} SET user_select= %s, enemy_select = %s, enemy_id = %s WHERE user_id=%s"
                cursor.execute(sql, (None, None, None, u['user_id']))
            connection.commit()
        elif result == 'first_lose':
            bot.send_message(u['user_id'], text='Ви програли( модифікувати)')
            with connection.cursor() as cursor:
                sql = f"DELETE FROM {database} WHERE user_id=%s"
                cursor.execute(sql, (None, None, None, u['user_id']))
            connection.commit()
        elif result == 'draw':
            bot.send_message(u['user_id'], text='Ви пройшли в наступний раунд( модифікувати)') # TODO add draw function
            with connection.cursor() as cursor:
                sql = f"UPDATE {database} SET user_select= %s, enemy_select = %s, enemy_id = %s WHERE user_id=%s"
                cursor.execute(sql, (None, None, None, u['user_id']))
            connection.commit()


def make_function(database, gameId, key_board, price):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM {database} WHERE game_id=%s"
        cursor.execute(sql, gameId)
        result = cursor.fetchall()
    check_user_vote(result, database, key_board)
    if result.__len__() > 2:
        u_select = result[0]['user_select']
        e_select = result[0]['enemy_select']
        if u_select == 1 and e_select == 1:
            result = 'draw'
        elif u_select == 1 and e_select == 2:
            result = 'first_lose'
        elif u_select == 1 and e_select == 3:
            result = 'first_win'

        if u_select == 2 and e_select == 1:
            result = 'first_win'
        elif u_select == 2 and e_select == 2:
            result = 'draw'
        elif u_select == 2 and e_select == 3:
            result = 'first_lose'

        if u_select == 3 and e_select == 1:
            result = 'first_lose'
        elif u_select == 3 and e_select == 2:
            result = 'first_win'
        elif u_select == 3 and e_select == 3:
            result = 'draw'
        time.sleep(15)
        if result == 'first_win':
            if 'free' in database:
                bot.send_message(result[0]['user_id'], text="Вітаю, ви перемогли!")
                bot.send_message(result[0]['enemy_id'], text="Не засмучуйся наступного разу удача буде на твоїй стороні!")
            else:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `users` WHERE id=%s"
                    cursor.execute(sql, (result[0]['user_id']))
                    result = cursor.fetchall()
                    money = result[0]['money'] + price
                    sql = "UPDATE `users` SET money= %s WHERE id=%s"
                    cursor.execute(sql, (money, result[0]['id']))
                connection.commit()
                bot.send_message(result[0]['user_id'], text="Вітаю, ви перемогли! Ващ виграш уже на вашому рахунку.")
                bot.send_message(result[0]['enemy_id'],
                                 text="Не засмучуйся, наступного разу удача буде на твоїй стороні!")
        elif result == 'first_lose':
            if 'free' in database:
                bot.send_message(result[0]['enemy_id'], text="Вітаю, ви перемогли!")
                bot.send_message( result[0]['user_id'], text="Не засмучуйся наступного разу удача буде на твоїй стороні!")
            else:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `users` WHERE id=%s"
                    cursor.execute(sql, (result[0]['enemy_id']))
                    result = cursor.fetchall()
                    money = result[0]['money'] + price
                    sql = "UPDATE `users` SET money= %s WHERE id=%s"
                    cursor.execute(sql, (money, result[0]['id']))
                connection.commit()
                bot.send_message(result[0]['enemy_id'], text="Вітаю, ви перемогли! Ващ виграш уже на вашому рахунку.")
                bot.send_message(result[0]['user_id'],
                                 text="Не засмучуйся, наступного разу удача буде на твоїй стороні!")
        elif result == 'draw':
            print(1)

      # TODO Check winner
    else:
        check_user_win_db(result, database, key_board)


def make_user_enemy(data, database, game_id):
    for d, i in enumerate(data):
        index = d + 1
        if index % 2 == 1:
            with connection.cursor() as cursor:
                sql = f"UPDATE {database} SET enemy_id= %s, game_id=%S WHERE user_id=%s"
                cursor.execute(sql, (data[index]['user_id'], game_id, data[d]['user_id']))
            connection.commit()
        else:
            with connection.cursor() as cursor:
                sql = f"UPDATE {database} SET enemy_id= %s, game_id=%S WHERE user_id=%s"
                cursor.execute(sql, (data[d-1]['user_id'], game_id, data[d]['user_id']))
            connection.commit()


def free_game_1_1(call):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `current_game` WHERE id=(SELECT MAX(id) FROM `current_game`)"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        if result.__len__() != 0:
            if result[0]["second_user"] is None:
                if result[0]['user_id'] == call.message.chat.id:
                    bot.send_message(call.message.chat.id, text='Ви уже зареєстровані на гру. Очікуйте суперника....')
                else:
                    with connection.cursor() as cursor:
                        sql = "SELECT * FROM `current_game`"
                        cursor.execute(sql)
                        result = cursor.fetchall()
                    for u in result:
                        with connection.cursor() as cursor:
                            sql = "DELETE FROM `current_game`  WHERE id=%s"
                            cursor.execute(sql, u['id'])
                    connection.commit()
                    result.append({'user_id': call.message.chat.id})
                    start_battle(result, 0)

            else:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `current_game` (`user_id`) VALUES (%s)"
                    cursor.execute(sql, call.message.chat.id)
                connection.commit()
                bot.send_message(call.message.chat.id, text='Очікуйте суперника...')
        else:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `current_game` (`user_id`) VALUES (%s)"
                cursor.execute(sql, call.message.chat.id)
            connection.commit()
            bot.send_message(call.message.chat.id, text='Очікуйте суперника...')


# Buy parts
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Помилка при спробі оплати, спробуйте знову")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` WHERE id=%s"
        cursor.execute(sql, (message.from_user.id))
        result = cursor.fetchall()
        money = result[0]['money'] + message.successful_payment.total_amount / 100
        sql = "UPDATE `users` SET money= %s WHERE id=%s"
        cursor.execute(sql, (money, result[0]['id']))
    connection.commit()
    bot.send_message(message.chat.id,
                     'Ваш рахунок поповнено на `{} {}`'.format(
                         message.successful_payment.total_amount / 100, 'Тунгриків(need to change)'),
                     parse_mode='Markdown')


bot.skip_pending = True


if __name__ == '__main__':
    bot.polling(none_stop=True)
