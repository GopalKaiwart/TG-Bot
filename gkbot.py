import asyncio
import os
import nest_asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Fix nested loop for environments like GitHub Actions
nest_asyncio.apply()

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running! I will auto-stop in 2 minutes.")

# Graceful stop after delay
async def stop_after_delay(app):
    await app.running_wait()  # ✅ Wait until bot is fully running
    await asyncio.sleep(120)
    print("⏱️ 2 minutes passed. Stopping bot...")
    await app.stop()

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    # ⏱️ Schedule auto-stop task after app starts
    asyncio.create_task(stop_after_delay(app))

    await app.run_polling()

# Run main with nested asyncio
asyncio.get_event_loop().run_until_complete(main())
