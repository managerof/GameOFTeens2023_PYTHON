import telebot
import db as utils

bot = telebot.TeleBot('bot api key')

db = utils.Database(utils.USERS_DATA_FILE_PATH)


@bot.message_handler(commands=['start'])
def handle_start(message):
    
    user = utils.User(message.from_user.id,
                      message.from_user.first_name,
                      message.date,
                      message.from_user.language_code)
    
#     if db.IsNewbie(user.id):
#         db.addUser(user)
    
    bot.send_message(user.id, f"{user.name}, ваш індетефіційний телеграм номер - {user.id}")
    
    bot.reply_to(message, "Привіт! Я бот від Lifecell і допоможу вам підібрати найкращий тариф!")

bot.polling()

