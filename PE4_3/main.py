import telebot
import config
import os
import warnings
from voice import get_all_voices, generate_audio
from pydub import AudioSegment
from pydub.utils import which

# 🛠 Принудительно добавляем путь к ffmpeg/ffprobe в PATH
os.environ["PATH"] += os.pathsep + r"C:\Tools\ffmpeg\bin"

# 🔇 Убираем предупреждения от pydub
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub")

# Явно указываем путь к ffmpeg и ffprobe
AudioSegment.converter = r"C:\Tools\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\Tools\ffmpeg\bin\ffprobe.exe"

# Проверка наличия файлов
if not os.path.isfile(AudioSegment.converter) or not os.path.isfile(AudioSegment.ffprobe):
    print("❗ ffmpeg или ffprobe не найдены по заданным путям!")
    print("Проверь наличие файлов или переменные среды.")
    exit(1)

# Инициализация бота
API_TOKEN = config.bot_token
bot = telebot.TeleBot(API_TOKEN)

# Получаем голоса
voices = get_all_voices()

# Кнопки выбора голосов
voice_buttons = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
for voice in voices:
    voice_buttons.add(telebot.types.KeyboardButton(voice['name']))

# Хранилища состояния пользователя
selected_voice = {}
last_audio = {}
awaiting_download = {}
awaiting_format = {}

# Кнопки "Да / Нет"
yes_no_buttons = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes_no_buttons.add("Да", "Нет")

# Кнопки форматов
format_buttons = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
format_buttons.add("mp3", "ogg", "wav")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    bot.reply_to(
        message,
        "Привет! Я бот для озвучки текста. Выбери голос:",
        reply_markup=voice_buttons
    )


@bot.message_handler(func=lambda message: message.text in [v['name'] for v in voices])
def voice_selected(message):
    user_id = message.from_user.id
    selected_voice[user_id] = message.text
    bot.send_message(user_id, f"Выбран голос: {message.text}. Введите текст для озвучивания.")


@bot.message_handler(func=lambda m: awaiting_download.get(m.from_user.id, False))
def handle_download_choice(message):
    user_id = message.from_user.id
    awaiting_download[user_id] = False

    if message.text.lower() == "да":
        awaiting_format[user_id] = True
        bot.send_message(user_id, "В каком формате сохранить?", reply_markup=format_buttons)
    else:
        bot.send_message(user_id, "Окей, не сохраняю 😉", reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda m: awaiting_format.get(m.from_user.id, False))
def handle_format_choice(message):
    user_id = message.from_user.id
    awaiting_format[user_id] = False
    chosen_format = message.text.lower()

    if chosen_format not in ["mp3", "ogg", "wav"]:
        bot.send_message(user_id, "Формат не поддерживается.")
        return

    input_path = last_audio.get(user_id)
    if not input_path or not os.path.exists(input_path):
        bot.send_message(user_id, "Файл не найден.")
        return

    # Конвертация через pydub
    audio = AudioSegment.from_file(input_path)
    output_path = input_path.replace(".mp3", f".{chosen_format}")
    audio.export(output_path, format=chosen_format)

    with open(output_path, "rb") as file:
        bot.send_document(user_id, file, visible_file_name=os.path.basename(output_path))

    bot.send_message(user_id, "Файл отправлен ✅", reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def generate_and_ask_download(message):
    user_id = message.from_user.id
    text = message.text

    voice_name = selected_voice.get(user_id, voices[0]['name'])
    voice_id = next(v['id'] for v in voices if v['name'] == voice_name)

    mp3_path = generate_audio(text, voice_id)
    last_audio[user_id] = mp3_path

    with open(mp3_path, "rb") as voice_file:
        bot.send_voice(user_id, voice_file)

    awaiting_download[user_id] = True
    bot.send_message(user_id, "Хочешь скачать файл?", reply_markup=yes_no_buttons)


if __name__ == '__main__':
    bot.polling(none_stop=True)
