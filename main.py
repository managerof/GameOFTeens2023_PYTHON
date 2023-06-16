import telebot
from telebot import types
import db as utils
import local


bot = telebot.TeleBot('BOT_API')

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
    
    print(message)
    
    if db.IsNewbie(user.id):
        db.UpdateUser(user)
    else:
        user = db.LoadUser(user.id)
    
    # bot.send_message(user.id, f"{user.name}{local.debug[user.language_code]}{user.id}")
    
    bot.reply_to(message, local.greeting[user.language_code])
    bot.send_message(user.id, local.lang_choosing[user.language_code], reply_markup=markup)
    print(user.language_code)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    
    if call.data == 'uk' or call.data == 'ru' or call.data == 'en':
        language_code = call.data
        user = db.LoadUser(call.from_user.id)
        user.language_code = call.data
        db.UpdateUser(user)

        bot.send_message(call.from_user.id, local.language_selected[user.language_code])
        
        bot.send


bot.polling()

