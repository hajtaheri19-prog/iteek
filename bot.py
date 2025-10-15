import os
from flask import Flask, request
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
MINIAPP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

# --- Create Flask app ---
app = Flask(__name__)

# --- Correct way to create Application in PTB 20.x ---
application = Application.builder().token(TOKEN).build()


# --- /start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    #  دکمه زیر پیام (Inline)
    inline_button = InlineKeyboardButton(
        "🔹 ثبت گزارش کار", web_app={"url": MINIAPP_URL}
    )
    inline_markup = InlineKeyboardMarkup([[inline_button]])

    # دکمه دائمی کنار کادر تایپ (Reply Keyboard)
    open_app_button = KeyboardButton(
        "🔹 باز کردن Mini App", web_app={"url": MINIAPP_URL}
    )
    reply_markup = ReplyKeyboardMarkup(
        [[open_app_button]], resize_keyboard=True, one_time_keyboard=False
    )

    welcome_text = (
        "سلام 👋 خوش اومدی به ربات آی‌تاب 🌿\n"
        "از اینجا می‌تونی گزارش روزانه‌ات رو در Mini App وارد کنی."
    )

    await update.message.reply_text(welcome_text, reply_markup=inline_markup)
    await update.message.reply_text(
        "برای ورود سریع، روی دکمه کنار کادر تایپ بزن 👇", reply_markup=reply_markup
    )


# --- Register command handler ---
application.add_handler(CommandHandler("start", start))


# --- Flask route to receive webhooks ---
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.create_task(application.process_update(update))
    return "ok"


@app.route("/", methods=["GET"])
def home():
    return "AiTab Bot is running successfully 🌿"


if __name__ == "__main__":
    # set webhook (delete previous first)
    bot = application.bot
    bot.delete_webhook()
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

    app.run(host="0.0.0.0", port=10000)
