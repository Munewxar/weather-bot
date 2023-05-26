from dotenv import load_dotenv
import os

import logging

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from get_weather import get_weather
from convert_voice_to_text import convert_voice_to_text


load_dotenv()
API_TOKEN = os.getenv("TELGRAM_API_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi &#128400;&#10;" 
        "My name is Weather Bot. I will tell you a weather cast &#x26C5;&#10;"
        "Enter City name to get weather info:",
        reply_markup=ForceReply(selective=True),
    )


# Write help command logic
async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("To get weather cast, type or record voice message with the name of the city.")


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    weather_data = get_weather(update.message.text)

    await update.message.reply_html(
        f"{weather_data['city']}, {weather_data['country']}&#10;" 
        f"Утром +{weather_data['morning_temp']}&#10;"
        f"Днем +{weather_data['day_temp']}&#10;"
        f"Вечером +{weather_data['evening_temp']}&#10;"
        f"Восход +{weather_data['sunrise']}&#10;"
        f"Закат +{weather_data['sunset']}&#10;",
        reply_markup=ForceReply(selective=True),
    )


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_file = await context.bot.get_file(update.message.voice.file_id)
    
    voice_file_path = 'test-source/voice.oga'
    await msg_file.download_to_drive(voice_file_path)

    text = convert_voice_to_text(voice_file_path)

    weather_data = get_weather(text)

    await update.message.reply_html(
        f"{weather_data['city']}, {weather_data['country']}&#10;" 
        f"Утром +{weather_data['morning_temp']}&#10;"
        f"Днем +{weather_data['day_temp']}&#10;"
        f"Вечером +{weather_data['evening_temp']}&#10;"
        f"Восход +{weather_data['sunrise']}&#10;"
        f"Закат +{weather_data['sunset']}&#10;",
        reply_markup=ForceReply(selective=True),
    )


def main() -> None:
    application = Application.builder().token(API_TOKEN).build()

    # on different commands
    application.add_handler(CommandHandler("start", handle_start_command))
    application.add_handler(CommandHandler("help", handle_help_command))

    # on non command 
    application.add_handler(MessageHandler(filters.TEXT, handle_text_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    application.run_polling()


if __name__ == '__main__':
    main()
