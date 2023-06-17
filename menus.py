from telebot import types # for markup buttons
import local              # localization


def get_lang_menu():
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(types.InlineKeyboardButton("Українська", callback_data='uk'))
    menu.add(types.InlineKeyboardButton("Русский", callback_data='ru'))
    menu.add(types.InlineKeyboardButton("English", callback_data='en'))
    
    return menu

def get_help_menu(language):
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(local.hm_btn1[language], callback_data='choose_tariff'))
    menu.add(types.InlineKeyboardButton(local.hm_btn2[language], callback_data='show_all_tariffs'))
    menu.add(types.InlineKeyboardButton(local.hm_btn3[language], callback_data='my_tariff'))
    menu.add(types.InlineKeyboardButton(local.hm_btn4[language], callback_data='change_language'))
    
    return menu

def all_tariffs(language):
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(local.all_ts1[language], callback_data='show_and_back_1'))
    menu.add(types.InlineKeyboardButton(local.all_ts2[language], callback_data='show_and_back_2'))
    menu.add(types.InlineKeyboardButton(local.all_ts3[language], callback_data='show_and_back_3'))
    menu.add(types.InlineKeyboardButton(local.all_ts4[language], callback_data='show_and_back_4'))
    menu.add(types.InlineKeyboardButton(local.go_back[language], callback_data='help_menu'))
    link = types.InlineKeyboardButton(local.more_tariffs[language], url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/", callback_data="back_to_menu")
    menu.add(link)
    
    return menu