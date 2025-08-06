import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running...")

async def stop_after_delay(app, delay=120):  # 2 minutes
    await asyncio.sleep(delay)
    print("Stopping bot after 2 minutes.")
    await app.shutdown()
    await app.stop()

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Schedule shutdown task
    asyncio.create_task(stop_after_delay(app, delay=120))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
