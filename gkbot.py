import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.chat_join_request.approve()
    print(f"Approved: {update.chat_join_request.from_user.username}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(approve_request))

    # Start the bot
    runner = asyncio.create_task(app.run_polling())

    # Run the bot for 2 minutes (120 seconds)
    await asyncio.sleep(120)

    # Stop the bot after 2 minutes
    await app.shutdown()
    print("Bot stopped after 2 minutes.")

if __name__ == "__main__":
    asyncio.run(main())
