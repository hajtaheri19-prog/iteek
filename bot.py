import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# بارگذاری متغیرها از فایل .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# تعیین URL وب‌اپ (تَب‌دیلا Mini App)
WEBAPP_URL = "https://epic-calm-reports-d9f9cb01.base44.app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # دکمه کنار کادر تایپ
    reply_keyboard = [[{"text": "📝 ثبت گزارش کار", "web_app": {"url": WEBAPP_URL}}]]

    # دکمه زیر پیام
    inline_keyboard = [
        [InlineKeyboardButton("📝 ثبت گزارش کار", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]

    await update.message.reply_text(
        "سلام 👋 خوش آمدی 🌿\nبرای ثبت گزارش روزانه روی یکی از دکمه‌ها کلیک کن.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard)
    )

    await update.message.reply_text(
        "برای شروع گزارش روی دکمه زیر کلیک کن:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 Tabdila Bot started and listening...")
    app.run_polling()
