import requests
import json
from http import HTTPStatus
from aiogram import Bot, Dispatcher, executor, types
from tokens import API, BOT_API

bot = Bot(BOT_API)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Я запустился!')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Привет!\nНапиши название города, что бы узнать погоду.')


@dp.message_handler(content_types=['text'])
async def get_weather(message: types.Message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == HTTPStatus.OK:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        await message.answer(f'Сейчас на улице: {"{:.1f}".format(temp)}C\nОщущается как: {"{:.1f}".format(feels_like)}С\nВлажность: {humidity}%\nСкорость ветра: {wind_speed}м/с')
        await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAJeZWVeZhEun5yfBiq27U6qgY4rMI3oAALaAANSiZEjXPocKNYC-60zBA')


    else:
        await message.answer('Вы ввели некорректное название города.\nПопробуйте еще раз.')



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
