import json
from telegram import Update, InputMediaDocument
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

TOKEN = os.getenv("BOT_TOKEN")

with open("config.json") as f:
    CONFIG = json.load(f)

CHANNEL_USERNAME = CONFIG["channel_username"]
ADMINS = CONFIG["admins"]
FILES_DB = "files.json"

# Load existing files
if not os.path.exists(FILES_DB):
    with open(FILES_DB, "w") as f:
        json.dump([], f)

def load_files():
    with open(FILES_DB) as f:
        return json.load(f)

def save_file(data):
    files = load_files()
    files.append(data)
    with open(FILES_DB, "w") as f:
        json.dump(files, f)

def is_admin(user_id):
    return str(user_id) in ADMINS

def handle_file(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return

    file = update.message.document or update.message.video or update.message.audio
    caption = (update.message.caption or "") + f"\n\n📌 {CHANNEL_USERNAME}"

    file_info = {
        "file_id": file.file_id,
        "file_name": file.file_name,
        "caption": caption
    }

    save_file(file_info)

    context.bot.send_document(chat_id=CHANNEL_USERNAME, document=file.file_id, caption=caption)

def search(update: Update, context: CallbackContext):
    query = " ".join(context.args).lower()
    files = load_files()
    results = [f for f in files if query in f["file_name"].lower()]

    if not results:
        update.message.reply_text("No results found.")
        return

    for f in results[:10]:
        update.message.reply_document(document=f["file_id"], caption=f["caption"])

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /search <filename> to find files.")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.audio, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
  
