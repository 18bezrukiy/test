import os  # Модуль для работы с операционной сис-мой
import logging  # Модуль для ведения журнала логов

from google.cloud import dialogflow
from aiogram import Bot, Dispatcher, executor, types

telegram_token = '5541534058:AAGvbXLGRdsQT1PcDpsuDLvdbnYzRYn1PiA'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "my--assistant-c788c-b251eed3d8f6.json"

session_client = dialogflow.SessionsClient()
project_id = 'my--assistant-c788c'
session_id = 'sessions'
language_code = 'ru'
session = session_client.session_path(project_id, session_id)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=telegram_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'Салам')


@dp.message_handler()
async def lzt_dialogflow(message: types.Message):
    text_input = dialogflow.TextInput(text=message.text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    if response.query_result.fulfillment_text:
        await bot.send_message(message.from_user.id, response.query_result.fulfillment_text)
    else:
        await bot.send_message(message.from_user.id, "Я тебя не понимаю")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)