import os
import time

import pymysql.cursors
from botInfo import bot
from battle import start_battle
connection = pymysql.connect(
                             host='us-cdbr-east-02.cleardb.com',
                             user='bf7c55efe60aa8',
                             password='f5721000',
                             db='heroku_d166a25f7ae34c1',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def send_message_one_ours_ready(users):
    for u in users:
        bot.send_message(u['user_id'], text=f"""Старт через годину.""")


def send_message_one_minutes_ready(users):
    for u in users:
        bot.send_message(u['user_id'], text=f"""Старт через хвилину.""")

def turnir(call, person ,price):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` WHERE id=%s"
        cursor.execute(sql, call.message.chat.id)
        result = cursor.fetchall()
    if result[0]['money'] < price:
        bot.send_message(call.message.chat.id, text='На вашому рахунку недостатньо коштів, поповіність рахунок в профілі')
    else:
        money = result[0]['money'] - price
        with connection.cursor() as cursor:
            sql = "UPDATE `users` SET money= %s WHERE id=%s"
            cursor.execute(sql, (money, call.message.chat.id))
        connection.commit()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `turnir` WHERE user_count=%s and price=%s"
            cursor.execute(sql, (person, price))
            result = cursor.fetchall()

        if len(result) == person - 1:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `turnir` (`user_id`, `user_count`, `price`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (call.message.chat.id, person, price))
            connection.commit()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `turnir` WHERE user_count=%s and price=%s"
                cursor.execute(sql, (person, price))
                result = cursor.fetchall()
            for u in result:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM `turnir`  WHERE id=%s"
                    cursor.execute(sql, (u['id']))
                connection.commit()
            if person == 2:
                start_battle(result, price)
            else:
                send_message_one_ours_ready(result)
                time.sleep(3540)
                send_message_one_minutes_ready(result)
                time.sleep(60)
                start_battle(result, price)
        else:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `turnir` (`user_id`, `user_count`, `price`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (call.message.chat.id, person, price))
                sql = "UPDATE `users` SET money= %s WHERE id=%s"
                cursor.execute(sql, (money, call.message.chat.id))
            connection.commit()
            bot.send_message(call.message.chat.id, text="""Коли всі зберуться ми повідомимо тебе  за 0000 до початку.
            Поки чекаєш — заходь в наш - чат, де можна поспілкуватися з іншими учасниками!""")

