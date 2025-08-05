import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.chat_join_request.approve()
    user = update.chat_join_request.from_user
    print(f"✅ Approved join request from: {user.full_name} (@{user.username})")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(approve_request))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
