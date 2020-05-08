import telebot
import matplotlib.pyplot as plt
from IPython import get_ipython
import requests 
import json
import os


bot = telebot.TeleBot("1176385319:AAE5wGQgIAwR-UdXnNRQToa4goQ9W6Ug9vY")


@bot.message_handler(commands=['start'])
def start(message):
    send_message = """Приветик
    у меня есть статистика короновируса в РФ
    /today - число заразившихся за последний день
    /last5 - число заразивщихся за последние пять дней
    /plot - график за все время"""
    bot.send_message(message.chat.id, send_message, parse_mode='html')


@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "/today":
        parameters = {"Country": "Russian Federation"}
        response = requests.get('https://api.covid19api.com/live/country/russia/status/confirmed/date/2020-03-21T13:13:30Z',params=parameters)
        json_response = response.json()
        last_day = len(json_response)
        today_confirmed = json_response[last_day-1]['Confirmed']
        yesterday_confirmed = json_response[last_day-2]['Confirmed']
        result = today_confirmed - yesterday_confirmed
        final_message = "За последний день подтвержденных случаев : " + str(result)
        bot.send_message(message.chat.id, final_message, parse_mode='html')
    elif get_message_bot == "/last5":
        parameters = {"Country": "Russian Federation"}
        response = requests.get('https://api.covid19api.com/live/country/russia/status/confirmed/date/2020-03-21T13:13:30Z',params=parameters)
        json_response = response.json()
        last_day = len(json_response)
        last_day_confirmed = json_response[last_day-1]['Confirmed']
        first_day_confirmed = json_response[last_day-5]['Confirmed']
        confirmed_in_five_days = last_day_confirmed - first_day_confirmed
        final_message = "За последние пять дней подтвержденных случаев : " +str(confirmed_in_five_days)
        bot.send_message(message.chat.id, final_message, parse_mode='html')
    elif get_message_bot == "/plot":
        days = []
        confirmed_by_day = []
        parameters = {"Country": "Russian Federation"}
        response = requests.get('https://api.covid19api.com/live/country/russia/status/confirmed/date/2020-03-21T13:13:30Z',params=parameters)
        json_response = response.json()
        days_counter = len(json_response)
        days.extend(range(1, days_counter))
        for i in range (days_counter):
            try:
                temp = json_response[days_counter-(days_counter-i-1)]['Confirmed'] - json_response[days_counter-(days_counter-i)]['Confirmed']
                print(temp)
                confirmed_by_day.append(temp)
            except:
                print("bruh")
        for i in confirmed_by_day:
            try:
                if i == 0:
                    confirmed_by_day.remove(i)
            except:
                print("bruh")
        confirmed_by_day.sort()
        del confirmed_by_day[len(confirmed_by_day)-1]
        if (len(days) > len(confirmed_by_day)):
            days = days[:len(confirmed_by_day)]
        elif (len(days) < len(confirmed_by_day)):
            confirmed_by_day = confirmed_by_day[:len(days)]
        print(confirmed_by_day)
        plt.xticks(days)
        plt.plot(days,confirmed_by_day,color='red')
        plt.savefig('plot.png', dpi=200, bbox_inches='tight')
        photo = open('plot.png', 'rb')
        final_message = "графичек"
        bot.send_message(message.chat.id, final_message, parse_mode='html')
        bot.send_photo(message.chat.id, photo)
        photo = ""
        os.remove("plot.png")
    else:
        final_message = "не понял че ты хочешь "
        bot.send_message(message.chat.id, final_message, parse_mode='html')
        send_message = """
        вот что у меня есть
        /today - число заразившихся за последний день
        /last5 - число заразивщихся за последние пять дней
        /plot - график за все время"""
        bot.send_message(message.chat.id, send_message, parse_mode='html')


bot.polling(none_stop=True)

