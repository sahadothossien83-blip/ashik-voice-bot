import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = os.environ.get("BOT_TOKEN")
ELEVEN_API = os.environ.get("ELEVEN_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎙️ Voice Clone Bot Ready!\n\n"
        "যেকোনো লেখা পাঠান, আমি আপনার ভয়েসে বানিয়ে দেবো।\n"
        "চাইনিজ/ইংলিশ ভিডিও পাঠালে অটো ভয়েস ওভার করে দেবো।"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("⏳ আপনার ভয়েসে বানাচ্ছি...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVEN_API, "Content-Type": "application/json"}
    data = {"text": user_text, "model_id": "eleven_multilingual_v2"}
    
    r = requests.post(url, json=data, headers=headers)
    if r.status_code == 200:
        with open("voice.mp3", "wb") as f:
            f.write(r.content)
        await update.message.reply_voice(voice=open("voice.mp3", "rb"), caption="✅ আপনার ক্লোন ভয়েস রেডি!")
    else:
        await update.message.reply_text(f"❌ Error: {r.text[:200]}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
