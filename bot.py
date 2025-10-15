import os
from flask import Flask, request
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Bot
)
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
MINIAPP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

bot = Bot(token=TOKEN)
app = Flask(__name__)

# ساختن Application بدون Updater (سازگار با Python 3.13)
application = Application(bot=bot)

# --- /start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # دکمه داخل پیام (Inline)
    inline_button = InlineKeyboardButton(
        "🔹 ثبت گزارش کار",
        web_app={"url": MINIAPP_URL}
    )
    inline_markup = InlineKeyboardMarkup([[inline_button]])

    # دکمه دائمی پایین کادر تایپ (Reply Keyboard)
    open_app_button = KeyboardButton(
        "🔹 باز کردن Mini App",
        web_app={"url": MINIAPP_URL}
    )
    reply_markup = ReplyKeyboardMarkup(
        [[open_app_button]], resize_keyboard=True, one_time_keyboard=False
    )

    welcome_text = (
        "سلام 👋 خوش اومدی به ربات آی‌تاب 🌿\n"
        "از اینجا می‌تونی گزارش روزانه‌ات رو در Mini App وارد کنی."
    )

    # ارسال پیام خوش‌آمد با هر دو نوع دکمه
    await bot.send_message(chat_id=chat_id, text=welcome_text, reply_markup=inline_markup)
    await bot.send_message(
        chat_id=chat_id,
        text="برای ورود سریع، روی دکمه کنار کادر تایپ بزن 👇",
        reply_markup=reply_markup
    )

application.add_handler(CommandHandler("start", start))

# --- Flask Webhook routes ---
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    application.create_task(application.process_update(update))
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "AiTab Bot running successfully 🌿"

if __name__ == "__main__":
    bot.delete_webhook()  # حذف وب‌هوک قبلی در صورت وجود
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=10000)
