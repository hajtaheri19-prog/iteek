import os
from flask import Flask, request
from telegram import (
    Update, KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
MINIAPP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    inline_button = InlineKeyboardButton("🔹 ثبت گزارش کار", web_app={"url": MINIAPP_URL})
    inline_markup = InlineKeyboardMarkup([[inline_button]])

    open_app_button = KeyboardButton("🔹 باز کردن Mini App", web_app={"url": MINIAPP_URL})
    reply_markup = ReplyKeyboardMarkup([[open_app_button]], resize_keyboard=True)

    welcome = "سلام 👋 خوش اومدی به ربات آی‌تاب 🌿\nاز اینجا می‌تونی گزارش روزانه‌ات رو وارد کنی."
    await update.message.reply_text(welcome, reply_markup=inline_markup)
    await update.message.reply_text("برای ورود سریع، روی دکمه کنار کادر تایپ بزن 👇", reply_markup=reply_markup)

application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.create_task(application.process_update(update))
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "AiTab Bot running successfully 🌿"

if __name__ == "__main__":
    bot = application.bot
    bot.delete_webhook()
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=10000)
