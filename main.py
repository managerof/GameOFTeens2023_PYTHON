import telebot            # -_________________________________________________________________-
from telebot import types # for markup buttons
import db as utils        # data structures
from menus import *       # import pre-designed menus
#import callbacks          # callbacks handler


bot = telebot.TeleBot('BOT_API')
db = utils.Database(utils.USERS_DATA_FILE_PATH) # db object to handle user data (save, load, init user)

temp_users_data = {}

@bot.message_handler(commands=['lang'])
def choose_language(message):
    # initialize user object
    user = db.LoadUser(message.from_user.id)
    
    # show buttons
    bot.send_message(user.id, local.lang_choosing[user.language_code], reply_markup=get_lang_menu())

@bot.message_handler(commands=['menu'])
def help_menu(message):
    # initialize user
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
    bot.send_message(user.id, local.help_menu[user.language_code], reply_markup=get_help_menu(user.language_code))

@bot.message_handler(commands=['lang'])
def help_menu(message):
    # initialize user
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
    bot.send_message(user.id, local.help_menu[user.language_code], reply_markup=get_help_menu(user.language_code))


@bot.message_handler(commands=['start'])
def handle_start(message):
    
    # initialize user
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
    # debug
    print(db.IsNewbie(user.id), message, user.name)
    
    # load data about current user
    if db.IsNewbie(user.id):
        db.UpdateUser(user)
    else:
        user = db.LoadUser(user.id)
    
    # bot.send_message(user.id, f"{user.name}{local.debug[user.language_code]}{user.id}")
    
    # greetings
    bot.reply_to(message, local.greeting[user.language_code])
    
    # languages choose buttons
    bot.send_message(user.id, local.lang_choosing[user.language_code], reply_markup=get_lang_menu())


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    
    # initialize user object
    user = db.LoadUser(call.from_user.id)
    
    # yeah switches was a good idea but i didn't had enough time for restructuring it ;)
    
    if call.data == "help_menu":
        bot.send_message(user.id, local.help_menu[user.language_code], reply_markup=get_help_menu(user.language_code))
        return
    
    if call.data == "auth":
        menu = types.InlineKeyboardMarkup(row_width=1)
        
        link = types.InlineKeyboardButton(local.login[user.language_code],
                                          url="https://auth.lifecell.ua/auth/realms/lifecell/login-actions/authenticate?execution=262f793c-c567-4528-bb06-4ca3c73b63ad&client_id=lifecell-js&tab_id=Gwg3pH8dyBg",
                                          callback_data="back_to_menu")
        menu.add(link)
        
        bot.send_message(user.id, local.auth[user.language_code], reply_markup=menu)
        return
        
    if call.data == "my_tariff":
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(local.yes[user.language_code], callback_data='auth'))
        menu.add(types.InlineKeyboardButton(local.no[user.language_code], callback_data='help_menu'))
        
        bot.send_message(user.id, local.sign_in[user.language_code], reply_markup=menu)
        return
    
    if call.data == "choose_tariff":
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(local.lets_go[user.language_code], callback_data='lets_choose_tariff'))
        menu.add(types.InlineKeyboardButton(local.go_back[user.language_code], callback_data='help_menu'))
        bot.send_message(user.id, local.ask_for_asking[user.language_code], reply_markup=menu)
        return
    
    if call.data == "lets_choose_tariff":
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(local.internet_usually_use_answer1[user.language_code], callback_data='choose_tariff_step2'))
        menu.add(types.InlineKeyboardButton(local.internet_usually_use_answer2[user.language_code], callback_data='choose_tariff_step2'))
        menu.add(types.InlineKeyboardButton(local.internet_usually_use_answer3[user.language_code], callback_data='choose_tariff_step2'))
        
        bot.send_message(user.id, local.internet_usually_use[user.language_code], reply_markup=menu) #callback_data="choose_tariff_step2"
        
    
    if call.data == "choose_tariff_step2":
        
        return
    
    
    if call.data == "show_all_tariffs":
        bot.send_message(user.id, local.all_tariffs[user.language_code], reply_markup=all_tariffs(user.language_code))
        return
        
    if call.data == 'uk' or call.data == 'ru' or call.data == 'en':
        user = db.LoadUser(call.from_user.id)
        user.language_code = call.data
        db.UpdateUser(user)

        bot.send_message(user.id, local.language_selected[user.language_code])
        
        bot.send_message(user.id, local.help_menu[user.language_code], reply_markup=get_help_menu(user.language_code))
        return
    
    if call.data == "change_language":
        # show buttons
        bot.send_message(user.id, local.lang_choosing[user.language_code], reply_markup=get_lang_menu())
        return


bot.polling()

