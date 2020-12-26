import os
import time

import pymysql
from botInfo import bot
from telebot import types

def keyboard():
    
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key = types.InlineKeyboardButton(text='Камінь ✊🏻', callback_data='1')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Папір ✋🏻', callback_data='2')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Ножиці ✌🏻', callback_data='3')
    keyboard.add(key)
    return keyboard



conn = pymysql.connect(
                             host='us-cdbr-east-02.cleardb.com',
                             user='bf7c55efe60aa8',
                             password='f5721000',
                             db='heroku_d166a25f7ae34c1',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

arr=["Камінь","Папір","Ножиці"]
next_level = []
wait_for_opp = {}
def game_result(first,last):
    if first == "1":
        if last == "2":
            return -1
        elif last == "3":
            return 1
        else:
            return 0
    if first == "2":
        if last == "1":
            return 1
        elif last == "3":
            return -1
        else:
            return 0
    if first == "3":
        if last == "1":
            return -1
        elif last == "2":
            return 1
        else:
            return 0

class player:
    battle_id = 0
    def __init__(self,chat__id,status,score,user_name):
        self.chat__id = chat__id
        self.status = status
        self.score = score
        self.user_name = user_name

class db_player:
    player_db = {}
    def __init__(self):
        connection = pymysql.connect(
                             host='us-cdbr-east-02.cleardb.com',
                             user='bf7c55efe60aa8',
                             password='f5721000',
                             db='heroku_d166a25f7ae34c1',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        cur.execute("SELECT * FROM players")
        row = cur.fetchall()
        cur.close()
        conn.close()
        for val in row:
            p = player(str(val[1]), "available", int(val[3]), val[2])
            self.player_db[str(val[1])] = p
    def add_player(self,chat__id,status,score,user_name):
        a = player(chat__id,status,score,user_name)
        self.player_db[str(chat__id)] = a
    def exist(self,chat__id):
        if str(chat__id) in self.player_db:
            return True
        else:
            return False

    #This method return an object from player class with chat__id condition
    def find_player_by_id(self,chat__id):
        return self.player_db[str(chat__id)]


player_db = db_player()
class battle:
    p1 = player(0,"",0,"")
    p2 = player(0,"",0,"")
    time_played1 = 0
    time_played2 = 0
    score1 = 0
    score2 = 0
    selected_op1 = 0
    selected_op2 = 0
    forbid_chat = 0
    def __init__(self,player1,player2,max_point):
        self.p1 = player1
        self.p2 = player2
        self.max_point = max_point
        self.p1.status = "in_battle"
        self.p2.status = "in_battle"
    def ended(self):
        if self.score1==self.max_point:
            player_db.add_player(self.p1.chat__id,'available',self.p1.score + self.score1 - self.score2,self.p1.user_name)
            bot.send_message(int(self.p1.chat__id),"Вітаю, ви виграли")
            bot.send_message(int(self.p2.chat__id), "Наступного разу удача буде на вашій стороні...")
            x = player_db.find_player_by_id(self.p1.chat__id)
            next_level.append(x)
        elif self.score2 == self.max_point:
            bot.send_message(int(self.p1.chat__id), "Наступного разу удача буде на вашій стороні...")
            bot.send_message(int(self.p2.chat__id), "Вітаю, ви виграли")
            player_db.add_player(self.p2.chat__id, 'available', self.p2.score + self.score2 - self.score1,
                                 self.p2.user_name)
            x = player_db.find_player_by_id(self.p2.chat__id)
            next_level.append(x)

    def concede(self):
        if self.score1 == self.max_point:
            player_db.add_player(self.p1.chat__id,'available',self.p1.score + self.score1 - self.score2,self.p1.user_name)
            player_db.add_player(self.p2.chat__id, 'available', self.p2.score + self.score2 - self.score1,self.p2.user_name)
        else:
            player_db.add_player(self.p1.chat__id, 'available', self.p1.score + self.score1 - self.score2,
                                 self.p1.user_name)
            player_db.add_player(self.p2.chat__id, 'available', self.p2.score + self.score2 - self.score1,
                                 self.p2.user_name)

        if int(self.p1.chat__id) in wait_for_opp:
            del(wait_for_opp[int(self.p1.chat__id)])
        elif int(self.p2.chat__id) in wait_for_opp:
            del (wait_for_opp[int(self.p2.chat__id)])

    def play(self,selected1,selected2):
        bot.send_message(self.p1.chat__id, "Супротивник Обрав " + str(arr[int(selected2)-1]))
        bot.send_message(self.p2.chat__id, "Супротивник Обрав " + str(arr[int(selected1)-1]))
        if game_result(selected1,selected2) == 1:
            self.score1 += 1
        elif game_result(selected1,selected2) == -1:
            self.score2 += 1

        if self.score1 == self.max_point or self.score2 == self.max_point:
            self.ended()
        else:
            bot.send_message(self.p1.chat__id,"Спробуйте свою удачу", reply_markup=keyboard())
            bot.send_message(self.p2.chat__id, "Спробуйте свою удачу", reply_markup=keyboard())


class db_battle:
    battles = {}
    p1 = player(0, "", 0, "")
    p2 = player(0, "", 0, "")
    b = battle(p1,p2,0)
    def add_battle(self,b):
        self.battles[str(b.p1.chat__id)] = b
        self.battles[str(b.p2.chat__id)] = b

    def del_battle(self,b):
        del(self.battles[b.battle_id])

    def show_battles(self):
        print("Battle Database :")
        for key in self.battles:
            print(str(key) + " :: " + str(self.battles[key].p1.chat__id) + " vs " + str(self.battles[key].p2.chat__id))

    def find(self,chad):
        for key in self.battles:
            if str(key) == str(chad):
                return self.battles[key]
        return 0

allow_to_play = 1
send_to_all = {}
battle_db = db_battle()
wait_room10 = []
wait_room5 = []
wait_room15 = []
response_wait10 = {}
last_message_sent = {}
intro = {}
menu_array=["Вікторина для друзівه 👬","Вікторина рейтингу🏆","Класифікація🏅","Посібник❓","Скасувати❌","Запросити друзів 👥","Нагороди 🎁"]
sub_menu_array=["Безкоштовна гра","Дуель","Швидка гра(8 людей)", "Турнір"]


def start_battle(users, price=0):
    full = len(users)
    for u in users:
        player_db.add_player(u['user_id'], 'in_battle', 0, 'enemy')
    i = 1
    x = 1
    xx = 1
    for u in users:
        if i%2 == 1:
            x = player_db.find_player_by_id(u['user_id'])
        else:
            xx = player_db.find_player_by_id(u['user_id'])
            b = battle(x, xx, 1)
            battle_db.add_battle(b)
            bot.send_message(b.p1.chat__id,  text="Спробуйте свою удачу",
                            reply_markup=keyboard())
            bot.send_message(b.p2.chat__id, text="Спробуйте свою удачу",
                            reply_markup=keyboard())
        i = i + 1

    while full != 1:
        time.sleep(10)
        if len(next_level) == full/2:
            full = len(next_level)
            i = 1
            x = 1
            xx = 1
            for u in users:
                if i % 2 == 1:
                    x = u
                else:
                    xx = u
                    b = battle(x, xx, 1)
                    battle_db.add_battle(b)
                    bot.send_message(b.p1.chat__id, text="Спробуйте свою удачу",
                                     reply_markup=keyboard())
                    bot.send_message(b.p2.chat__id, text="Спробуйте свою удачу",
                                     reply_markup=keyboard())
        else:
            time.sleep(10)
            for key in wait_for_opp:
                wait_for_opp[key]['time'] += 10
                if wait_for_opp[key]['time'] >= 30:
                    try:
                        bat = battle_db.find(key)
                        if int(key) == int(bat.p1.chat__id):
                            bat.score1 = bat.max_point
                            bot.send_message(int(bat.p1.chat__id),"Суперник не грав більше 30 секунд, тож ви отримали шанс")
                            bot.send_message(int(bat.p2.chat__id), "Минуло більше 30 секунд з того часу, як ви зіграли і програли :(")
                            bat.ended()
                        else:
                            bat.score2 = bat.max_point
                            bot.send_message(int(bat.p2.chat__id), "Суперник не грав більше 30 секунд, тож ви отримали шанс")
                            bot.send_message(int(bat.p1.chat__id), "Минуло більше 30 секунд з того часу, як ви зіграли і програли :(")
                            bat.ended()
                        del wait_for_opp[key]
                        break
                    except Exception as e:
                        if 'Forbidden' in e:
                            try:
                                bot.send_message(bat.p1.chat__id,"Суперник повністю здався")
                                bat.score1 = bat.max_point
                                bat.ended()
                                del wait_for_opp[key]
                            except:
                                bot.send_message(bat.p2.chat__id, "Суперник повністю здався")
                                bat.score2 = bat.max_point
                                bat.ended()
                                del wait_for_opp[key]
        win = len(users) * price * 0.9
        with conn.cursor() as cursor:
            sql = "SELECT * FROM `users` WHERE id=%s"
            cursor.execute(sql, next_level[0].chat__id)
            result = cursor.fetchall()
            money = result[0]['money'] + win
            sql = "UPDATE `users` SET money= %s WHERE id=%s"
            cursor.execute(sql, (money, result[0]['id']))
        conn.commit()


def vote_handler(msg):
    query_id = msg.id
    from_id = msg.from_user.id
    query_data = msg.data
    x = player_db.find_player_by_id(str(from_id))
    if x.status == 'in_battle':
        bat = battle_db.find(from_id)
        try:
            if str(from_id) == str(bat.p1.chat__id):
                if int(bat.p2.chat__id) in wait_for_opp:
                    bat.play(query_data,wait_for_opp[int(bat.p2.chat__id)]['selected'])
                    del(wait_for_opp[int(bat.p2.chat__id)])
                else:
                    dicss = {}
                    dicss['selected'] = query_data
                    dicss['time'] = 0
                    wait_for_opp[from_id] = dicss
            else:
                if int(bat.p1.chat__id) in wait_for_opp:
                    bat.play(wait_for_opp[int(bat.p1.chat__id)]['selected'],query_data)
                    del(wait_for_opp[int(bat.p1.chat__id)])
                else:
                    dicss = {}
                    dicss['selected'] = query_data
                    dicss['time'] = 0
                    wait_for_opp[from_id] = dicss
        except Exception as e:
            print("This Error had been occured : in the call back query : " + str(e))

