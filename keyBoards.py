from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Грати', 'Правила')
    markup.row('Профіль', "Зворотній зв'язок", )
    return markup


def language_select_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='Українська', callback_data='language_ua')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Русский', callback_data='language_ru')
    keyboard.add(key)
    return keyboard


def game_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='Безкоштовна гра', callback_data='free_game')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Дуель', callback_data='duel')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Швидка гра( 8 людей)', callback_data='fast_game')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Турнір', callback_data='turnir');
    keyboard.add(key)
    return keyboard


def free_game_keyboard():
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key = types.InlineKeyboardButton(text='1x1', callback_data='free_game_1_1')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='8x8', callback_data='free_game_8_8')
    keyboard.add(key)
    return keyboard


def play_keyboard_free():
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key = types.InlineKeyboardButton(text='папір', callback_data='paper_free_1_1')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='ножниці', callback_data='scissors_free_1_1')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Камінь', callback_data='stone_free_1_1')
    keyboard.add(key)
    return keyboard


def play_keyboard_free_8_8():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='папір', callback_data='paper_free_8_8')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='ножниці', callback_data='scissors_free_8_8')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Камінь', callback_data='stone_free_8_8')
    keyboard.add(key)
    return keyboard


def profile_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='Поповнити', callback_data='add_some_money')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Вивести', callback_data='withdraw_money')
    keyboard.add(key)
    return keyboard

def duel_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='25 тунгриків', callback_data='duel25')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='50 тунгриків', callback_data='duel50')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='100 тунгриків', callback_data='duel100')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='1000 тунгриків', callback_data='duel1000')
    keyboard.add(key)
    return keyboard

def fastgame_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='25 тунгриків', callback_data='fastgame25')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='50 тунгриків', callback_data='fastgame50')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='100 тунгриків', callback_data='fastgame100')
    keyboard.add(key)
    return keyboard

def turnir_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='16 на 16', callback_data='turnir16')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='32 на 32', callback_data='turnir32')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='64 на 64', callback_data='turnir64')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='256 на 256', callback_data='turnir256')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='1024 на 1024', callback_data='turnir1024')
    keyboard.add(key)
    return keyboard

def  turnir16_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='25 тунгриків', callback_data='turnir1625')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='50 тунгриків', callback_data='turnir1650')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='100 тунгриків', callback_data='turnir16100')
    keyboard.add(key)
    return keyboard

def turnir32_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='25 тунгриків', callback_data='turnir3225')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='50 тунгриків', callback_data='turnir3250')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='100 тунгриків', callback_data='turnir32100')
    keyboard.add(key)
    return keyboard

def turnir64_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='25 тунгриків', callback_data='turnir6425')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='50 тунгриків', callback_data='turnir6450')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='100 тунгриків', callback_data='turnir64100')
    keyboard.add(key)
    return keyboard

def turnir256_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='25 тунгриків', callback_data='turnir25625')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='50 тунгриків', callback_data='turnir25650')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='100 тунгриків', callback_data='turnir256100')
    keyboard.add(key)
    return keyboard

def turnir1024_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='25 тунгриків', callback_data='turnir102425')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='50 тунгриків', callback_data='turnir102450')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='100 тунгриків', callback_data='turnir1024100')
    keyboard.add(key)
    return keyboard
