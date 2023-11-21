import requests
import json
from http import HTTPStatus

from telebot import types

from tokens import API, bot

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nНапиши название города, что бы узнать погоду.')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == HTTPStatus.OK:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        image = 'hot.png' if temp > 5.0 else 'cold.png'
        file = open('images/' + image, 'rb')

        
        bot.send_message(message.chat.id, f'Сейчас на улице: {"{:.1f}".format(temp)}C\nОщущается как: {"{:.1f}".format(feels_like)}С\nВлажность: {humidity}%\nСкорость ветра: {wind_speed}м/с')
        bot.send_photo(message.chat.id, file)


    else:
        bot.send_message(message.chat.id, 'Вы ввели некорректное название города.\nПопробуйте еще раз.')



bot.polling(none_stop=True)
