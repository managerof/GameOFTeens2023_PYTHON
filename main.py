import telebot
from telebot import types # for markup buttons
import db as utils        # data structures
from menus import *       # import pre-designed menus
#import callbacks          # callbacks handler


bot = telebot.TeleBot('BOT_API_TOKEN')
db = utils.Database(utils.USERS_DATA_FILE_PATH) # db object to handle user data (save, load, init user)

temp_users_data = {}

@bot.message_handler(commands=['lang'])
def choose_language(message):
    # initialize user
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
    if db.IsNewbie(user.id):
        db.UpdateUser(user)
    else:
        user = db.LoadUser(user.id)
    
    # show buttons
    bot.send_message(user.id, local.lang_choosing[user.language_code], reply_markup=get_lang_menu())

@bot.message_handler(commands=['menu'])
def help_menu(message):
    # initialize user
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
    if db.IsNewbie(user.id):
        db.UpdateUser(user)
    else:
        user = db.LoadUser(user.id)
    
    bot.send_message(user.id, local.help_menu[user.language_code], reply_markup=get_help_menu(user.language_code))

@bot.message_handler(commands=['lang'])
def help_menu(message):
    # initialize user
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
    if db.IsNewbie(user.id):
        db.UpdateUser(user)
    else:
        user = db.LoadUser(user.id)
    
    bot.send_message(user.id, local.help_menu[user.language_code], reply_markup=get_help_menu(user.language_code))

@bot.message_handler(commands=['start'])
def handle_start(message):
    
    # initialize user
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
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

# Handle any other messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # initialize user
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
    # load data about current user
    if db.IsNewbie(user.id):
        db.UpdateUser(user)
    else:
        user = db.LoadUser(user.id)
    
    # Process and respond to user messages here
    bot.reply_to(message, local.unknown_command[user.language_code])

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    
    # initialize user
    user = utils.User(call.from_user.id,
                      call.from_user.first_name,
                      call.message.date,
                      call.from_user.language_code)

    # load data about current user
    if db.IsNewbie(user.id):
        db.UpdateUser(user)
    else:
        user = db.LoadUser(user.id)
    
    if not user.id in temp_users_data:
        temp_users_data[user.id] = {"internet":0,
                                    "calls":0,
                                    "socials":0,
                                    "pay":0}
    
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
        menu.add(types.InlineKeyboardButton(local.lets_go[user.language_code], callback_data='lets_choose_tariff_'))
        menu.add(types.InlineKeyboardButton(local.go_back[user.language_code], callback_data='help_menu'))
        bot.send_message(user.id, local.ask_for_asking[user.language_code], reply_markup=menu)
        return
    
    if call.data == "show_and_back_1":
        photo_path = './img/smart_life3.png'
        caption = local.caption1[user.language_code]
        img = open(photo_path, 'rb')
        
        menu = types.InlineKeyboardMarkup(row_width=2)
        menu.add(types.InlineKeyboardButton(local.go_back[user.language_code], callback_data='show_all_tariffs'))
        link = types.InlineKeyboardButton(local.apply_tariff[user.language_code], url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/smart-life-2021/")
        menu.add(link)
        
        bot.send_photo(call.message.chat.id, img, caption=caption, reply_markup=menu)
        
    if call.data == "show_and_back_2":
        photo_path = './img/smart_family.png'
        caption = local.caption2[user.language_code]
        img = open(photo_path, 'rb')
        
        menu = types.InlineKeyboardMarkup(row_width=2)
        menu.add(types.InlineKeyboardButton(local.go_back[user.language_code], callback_data='show_all_tariffs'))
        link = types.InlineKeyboardButton(local.apply_tariff[user.language_code], url="https://www.lifecell.ua/uk/mobilnij-zvyazok/smart-simya-series/")
        menu.add(link)
        
        bot.send_photo(call.message.chat.id, img, caption=caption, reply_markup=menu)
    
    if call.data == "show_and_back_3":
        photo_path = './img/smart_life3.png'
        caption = local.caption3[user.language_code]
        img = open(photo_path, 'rb')
        
        menu = types.InlineKeyboardMarkup(row_width=2)
        menu.add(types.InlineKeyboardButton(local.go_back[user.language_code], callback_data='show_all_tariffs'))
        link = types.InlineKeyboardButton(local.apply_tariff[user.language_code], url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/shkilniy/")
        menu.add(link)
        
        bot.send_photo(call.message.chat.id, img, caption=caption, reply_markup=menu)
    
    if call.data == "show_and_back_4":
        photo_path = './img/smart_life3.png'
        caption = local.caption4[user.language_code]
        img = open(photo_path, 'rb')
        
        menu = types.InlineKeyboardMarkup(row_width=2)
        menu.add(types.InlineKeyboardButton(local.go_back[user.language_code], callback_data='show_all_tariffs'))
        link = types.InlineKeyboardButton(local.apply_tariff[user.language_code], url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/vilniy-life-2021/")
        menu.add(link)
        
        bot.send_photo(call.message.chat.id, img, caption=caption, reply_markup=menu)
    
    # handle user chooses and save to temporary storage
    if "-" in call.data:
        datta = call.data.split("-")[1]
        
        if "1." in datta:
            temp_users_data[user.id]["internet"] = datta[2]
        elif "2." in datta:
            temp_users_data[user.id]["calls"] = datta[2]
        elif "3." in datta:
            temp_users_data[user.id]["socials"] = datta[2]
        elif "4." in datta:
            temp_users_data[user.id]["pay"] = datta[2]
    
    # debug
    print(user.name, user.id, temp_users_data[user.id])
    
    # internet asks
    if "lets_choose_tariff_" in call.data:
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(local.internet_usually_use_answer1[user.language_code], callback_data='choose_tariff_step2-1.1'))
        menu.add(types.InlineKeyboardButton(local.internet_usually_use_answer2[user.language_code], callback_data='choose_tariff_step2-1.2'))
        menu.add(types.InlineKeyboardButton(local.internet_usually_use_answer3[user.language_code], callback_data='choose_tariff_step2-1.3'))
        
        bot.send_message(user.id, local.internet_usually_use[user.language_code], reply_markup=menu)
        
    
    # minutes asks
    if "choose_tariff_step2" in call.data:
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(local.minutes_usually_use_answer1[user.language_code], callback_data='choose_tariff_step3-2.1'))
        menu.add(types.InlineKeyboardButton(local.minutes_usually_use_answer2[user.language_code], callback_data='choose_tariff_step3-2.2'))
        menu.add(types.InlineKeyboardButton(local.minutes_usually_use_answer3[user.language_code], callback_data='choose_tariff_step3-2.3'))
        
        bot.send_message(user.id, local.usually_use1[user.language_code], reply_markup=menu)
        return
    
    # social media asks
    if "choose_tariff_step3" in call.data:
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(local.socials_usually_use_answer1[user.language_code], callback_data='choose_tariff_step4-3.1'))
        menu.add(types.InlineKeyboardButton(local.socials_usually_use_answer2[user.language_code], callback_data='choose_tariff_step4-3.2'))
        menu.add(types.InlineKeyboardButton(local.socials_usually_use_answer3[user.language_code], callback_data='choose_tariff_step4-3.3'))
        
        bot.send_message(user.id, local.usually_use2[user.language_code], reply_markup=menu)
        return
    
    # tariff price asks
    if "choose_tariff_step4" in call.data:
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(types.InlineKeyboardButton(local.pay_usually_use_answer1[user.language_code], callback_data='choose_tariff_step5-4.1'))
        menu.add(types.InlineKeyboardButton(local.pay_usually_use_answer2[user.language_code], callback_data='choose_tariff_step5-4.2'))
        menu.add(types.InlineKeyboardButton(local.pay_usually_use_answer3[user.language_code], callback_data='choose_tariff_step5-4.3'))
        
        bot.send_message(user.id, local.usually_use3[user.language_code], reply_markup=menu)
        return
    
    if "choose_tariff_step5" in call.data:
        bot.send_message(user.id, "ну якшо ті вже все знаеш чому просто не перейдеш на сайт на підключиш потрібний тариф???")
    
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

