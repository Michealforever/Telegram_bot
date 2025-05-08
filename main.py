import json
import logging
import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive

# Load config
with open("config.json") as f:
    config = json.load(f)

BOT_TOKEN = "7701491191:AAHPGbItoh5S4zsulCCOVzkq0CRdRQxnwxU"
CHANNEL_USERNAME = config["channel_username"]
ADMINS = config["admins"]

logging.basicConfig(level=logging.INFO)

# Watermark as caption
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username
    if f"@{user}" not in ADMINS:
        return
    
    file = update.message.document or update.message.video or update.message.audio or update.message.photo[-1]
    caption = (update.message.caption or "") + f"\n\n📌 From: {CHANNEL_USERNAME}"
    
    # Forward the file to the channel
    if hasattr(file, 'file_id'):
        await context.bot.send_document(chat_id=CHANNEL_USERNAME, document=file.file_id, caption=caption)
    else:
        await update.message.reply_text("Unsupported file type.")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is ready. Send files to forward with watermark!")

if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_file))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 8080)),
        webhook_url=f"https://<https://telegram-bot-2-404g.onrender.com>.onrender.com"
    )
  
