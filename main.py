import telebot
import mysql.connector
from telebot import types

bot = telebot.TeleBot('***')

@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_one = types.KeyboardButton(text="1")
    button_two = types.KeyboardButton(text="2")
    button_three = types.KeyboardButton(text="3")
    button_seven = types.KeyboardButton(text="7")
    keyboard.add(button_one, button_two, button_three, button_seven)
    msg = bot.send_message(message.chat.id, "How many days do you want to see the information?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, table_week)

@bot.message_handler(func=lambda message:True)
def table_week(message):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="bet2u_db",
            password="2V6e5R8g",
            port="3306",
            database="test"
            )
        cursor = mydb.cursor()
        val = message.text
        sql = "SELECT \
        DATE_FORMAT(`request`, '%d %M %H:%i') AS 'date', \
        IF( ( TIMEDIFF(`response`, `request`) >= 0 && TIMEDIFF(`response`, `request`) < '00:30:00'), TIMEDIFF(`response`, `request`), 'Нет ответа') AS 'diff'\
        FROM `maksBot` \
        WHERE `request` > DATE_SUB(NOW(), INTERVAL %s DAY)"
        cursor.execute(sql, (val, ))
        result = cursor.fetchall()
        for x in result:
                bot.send_message(message.chat.id, "{}".format(x))
        mydb.close()
        return start_command(message)
    except Exception as e:
        bot.reply_to(message, "Error! \nEnter the number! {}".format(e))

bot.polling(none_stop=True)
