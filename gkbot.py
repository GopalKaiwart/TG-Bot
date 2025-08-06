import asyncio
import os
import nest_asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Fix for nested event loops (for GitHub Actions, etc.)
nest_asyncio.apply()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running! I will auto-stop in 2 minutes.")

# Schedule auto-stop using application lifecycle hook
async def stop_after_delay(app):
    await asyncio.sleep(120)
    print("⏱️ 2 minutes passed. Stopping bot...")
    await app.stop()  # Gracefully stops polling

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    # Start auto-stop task after app starts
    app.post_init = lambda app: asyncio.create_task(stop_after_delay(app))

    await app.run_polling()

# Run with nested loop support
asyncio.get_event_loop().run_until_complete(main())
