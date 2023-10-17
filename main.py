import threading

import telebot
import schedule
import time


bot = telebot.TeleBot('Token')

user_settings = {}


def send_notification(user_id, message):
    bot.send_message(user_id, message)


def scheduled_job():
    for user_id, settings in user_settings.items():
        if time.strftime("%H:%M") == settings["time"]:
            send_notification(user_id, "Время для уведомления!")


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    user_settings[user_id] = {"time": None, "interval": None}
    bot.send_message(user_id, "Пожалуйста, укажите время и интервал.")


@bot.message_handler(func=lambda message: message.text is not None)
def handle_text(message):
    user_id = message.chat.id
    text = message.text
    if user_id in user_settings:
        if not user_settings[user_id]["time"]:
            user_settings[user_id]["time"] = text
            bot.send_message(user_id, "Отлично! Теперь укажите интервал в минутах.")
        elif not user_settings[user_id]["interval"]:
            try:
                user_settings[user_id]["interval"] = int(text)
                bot.send_message(user_id, f"Уведомления будут отправляться в {user_settings[user_id]['time']} с интервалом {user_settings[user_id]['interval']} минут.")
                schedule.every(user_settings[user_id]["interval"]).minutes.do(send_notification, user_id, "Время для уведомления!")
            except ValueError:
                bot.send_message(user_id, "Пожалуйста, укажите корректный интервал в минутах.")
    else:
        bot.send_message(user_id, "Чтобы начать, отправьте /start.")


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    bot.polling()
