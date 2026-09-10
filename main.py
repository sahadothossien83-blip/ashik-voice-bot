import os
import asyncio
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Ashik Voice Bot is Running!"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হাই! আমি আশিক ভয়েস বট 🤖\nতুমি ভয়েস পাঠাও, আমি রিপ্লাই দিবো।")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("তোমার ভয়েস পেয়েছি! ❤️ ভয়েস ক্লোন প্রসেসিং চালু আছে...")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"তুমি বললে: {update.message.text}")

async def run_bot():
    if not BOT_TOKEN:
        print("BOT_TOKEN পাওয়া যায়নি!")
        return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
   
