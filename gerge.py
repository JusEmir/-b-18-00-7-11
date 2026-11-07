import telebot
import requests
import pyttsx3
import os
import uuid

# --- Вставьте свой токен ---
TOKEN = '9201351649:AAExCfhQESPtReSOsIXAMHvHm_GJaLRSChUpip install pyTelegramBotAPI requests pyttsx3'
bot = telebot.TeleBot(TOKEN)

# Этап 2: Функция получения факта
def get_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "Не удалось найти текст факта.")
        else:
            return f"Ошибка API: статус {response.status_code}"
    except Exception as e:
        return f"Ошибка при запросе: {e}"

# Этап 3: Функция озвучивания (сохраняет в файл и возвращает путь)
def speak(text):
    # Инициализируем движок внутри функции (избегаем проблем с потоками)
    engine = pyttsx3.init()
    
    # Генерируем уникальное имя файла, чтобы не было конфликтов
    filename = f"fact_{uuid.uuid4().hex}.mp3"
    
    # Сохраняем аудио
    engine.save_to_file(text, filename)
    engine.runAndWait()
    engine.stop()
    
    return filename

# Этап 1: Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот с фактами. Напиши !fact, чтобы получить интересный факт.")

# Этап 2 + 3: Обработчик команды !fact
@bot.message_handler(func=lambda message: message.text == '!fact')
def send_fact(message):
    # 1. Получаем факт
    fact_text = get_fact()
    
    # 2. Отправляем текстовое сообщение
    bot.reply_to(message, f"📝 Факт:\n{fact_text}")
    
    # 3. Озвучиваем и отправляем аудио
    try:
        audio_path = speak(fact_text)
        
        # Отправляем как голосовое сообщение (или как audio, если нужен плеер)
        with open(audio_path, 'rb') as audio:
            bot.send_voice(message.chat.id, audio, caption="🔊 Озвучка факта")
        
        # Удаляем временный файл
        os.remove(audio_path)
    except Exception as e:
        bot.reply_to(message, f"Не удалось создать аудио: {e}")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()