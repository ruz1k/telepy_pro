import telebot
import mysql.connector

db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="root",
      port="3306",
      database="telebot",
)

cursor = db.cursor()

# cursor.execute("SELECT * FROM customers")
# cursor.execute("CREATE TABLE telepy (id INT AUTO_INCREMENT PRIMARY KEY, date_otpravki DATETIME, date_otveta DATETIME)")
# myresult = cursor.fetchall()
# #cursor.execute("DROP TABLE user_date")
# cursor.execute("INSERT INTO telepy SET date_otpravki = NOW(), date_otveta = NOW()")
# db.commit()
# print(myresult)


bot = telebot.TeleBot('1203996678:AAGgShbFSxIsJTIG5OKpuOLRXEL2JTR73_8')

@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user.first_name
    bot.send_message(message.chat.id, "Hello {}".format(user))

@bot.message_handler(commands=['table'])
def table_command(message):
    msg = bot.send_message(message.chat.id, "How many days do you want to see the information?")
    bot.register_next_step_handler(msg, table_week)

def table_week(message):
    try:
        val = message.text
        sql = "SELECT \
        DATE_FORMAT(`date_otpravki`, '%d %M %H:%i') AS 'date', \
        IF(TIMEDIFF(`date_otveta`, `date_otpravki`) >= 0, TIMEDIFF(`date_otveta`, `date_otpravki`), 'Нет ответа') AS 'diff'\
        FROM `telepy` \
        WHERE `date_otpravki` > DATE_SUB(NOW(), INTERVAL %s DAY)"
        cursor.execute(sql, (val, ))
        result = cursor.fetchall()
        for x in result:
            bot.send_message(message.chat.id, "{}".format(x))
    except Exception as e:
        bot.reply_to(message, "Error! \nEnter the number! {}".format(e))

bot.polling(none_stop=True)