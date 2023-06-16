import telebot
from telebot import types
import db as utils
import local


bot = telebot.TeleBot('')
db = utils.Database(utils.USERS_DATA_FILE_PATH)


@bot.message_handler(commands=['start'])
def handle_start(message):
    
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
    print(db.IsNewbie(user.id))
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Українська", callback_data='uk'))
    markup.add(types.InlineKeyboardButton("Русский", callback_data='ru'))
    markup.add(types.InlineKeyboardButton("English", callback_data='en'))
    
    if db.IsNewbie(user.id):
        db.UpdateUser(user)
    else:
        user = db.LoadUser(user.id)
    
    # bot.send_message(user.id, f"{user.name}{local.debug[user.language_code]}{user.id}")
    
    bot.reply_to(message, local.greeting[user.language_code])
    bot.send_message(user.id, local.lang_choosing[user.language_code], reply_markup=markup)
    
def get_help_menu(language):
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(local.hm_btn1[language], callback_data='change_tariff'))
    menu.add(types.InlineKeyboardButton(local.hm_btn2[language], callback_data='show_all_tariffs'))
    menu.add(types.InlineKeyboardButton(local.hm_btn3[language], callback_data='hm_btn3'))
    menu.add(types.InlineKeyboardButton(local.hm_btn4[language], callback_data='hm_btn4'))
    
    return menu

def all_tariffs(language):
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(local.all_ts1[language], callback_data='show_and_back_1'))
    menu.add(types.InlineKeyboardButton(local.all_ts2[language], callback_data='show_and_back_1'))
    menu.add(types.InlineKeyboardButton(local.all_ts3[language], callback_data='show_and_back_1'))
    menu.add(types.InlineKeyboardButton(local.all_ts4[language], callback_data='show_and_back_1'))
    link = types.InlineKeyboardButton(local.more_tariffs[language], url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/", callback_data="back_to_menu")
    menu.add(link)
    
    return menu

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    
    user = db.LoadUser(call.from_user.id)
    
    if call.data == "change_tariff":
        bot.send_message(user.id, local.XXX[user.language_code], ...)
    
    if call.data == 'show_all_tariffs':
        bot.send_message(user.id, local.all_tariffs[user.language_code], reply_markup=all_tariffs(user.language_code))
    
    if call.data == 'uk' or call.data == 'ru' or call.data == 'en':
        language_code = call.data
        user = db.LoadUser(call.from_user.id)
        user.language_code = call.data
        db.UpdateUser(user)

        bot.send_message(user.id, local.language_selected[user.language_code])
        
        bot.send_message(user.id, local.help_menu[user.language_code], reply_markup=get_help_menu(user.language_code))
        

bot.polling()

