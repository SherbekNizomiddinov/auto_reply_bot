import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# .env fayldan o‘qish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /start buyrug‘i kelganda """
    await send_auto_reply(update, context)


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Har qanday matnli xabarga avtomatik javob """
    await send_auto_reply(update, context)



async def send_auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user

    if message is None or user is None:
        return

    if message.chat.type != "private":
        return

    name = user.full_name or "do'stim"

    text = (
        f"Assalomu alaykum, {name}!\n\n"
        "Tez orada ho‘jayin yozganingizga javob beradi... ⏳"
    )

    await message.reply_text(text)



def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

    # Botni yaratish
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
    MessageHandler(
        filters.TEXT
        & ~filters.COMMAND
        & filters.ChatType.PRIVATE
        & ~filters.User(user_id=OWNER_ID),
        auto_reply
    )
)

    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()