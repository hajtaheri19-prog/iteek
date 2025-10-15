import os
from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

# --- /start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Inline button linking to Mini‑App (Base44)
    inline_button = InlineKeyboardButton(
        "ثبت گزارش کار", web_app={"url": "https://epic-calm-reports-d9f9cb01.base44.app"}
    )
    inline_markup = InlineKeyboardMarkup([[inline_button]])

    # Reply (persistent) button linking to Mini‑App
    reply_button = KeyboardButton(
        "ثبت گزارش کار", web_app={"url": "https://epic-calm-reports-d9f9cb01.base44.app"}
    )
    reply_markup = ReplyKeyboardMarkup([[reply_button]], resize_keyboard=True)

    # Welcome message
    welcome_text = (
        "سلام 👋 خوش اومدی به ربات آی‌تاب 🌿\n"
        "از اینجا می‌تونی گزارش روزانه‌ات رو در Mini App وارد کنی."
    )

    await context.bot.send_message(
        chat_id=chat_id, text=welcome_text, reply_markup=inline_markup
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text="برای راحتی، می‌تونی از دکمه پایین هم به فرم گزارش کار وارد بشی.",
        reply_markup=reply_markup,
    )

# --- Telegram Application ---
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# --- Flask routes for Webhook ---
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.update_queue.put(update)
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "AiTab Bot running successfully 🌿"

if __name__ == "__main__":
    application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=10000)
