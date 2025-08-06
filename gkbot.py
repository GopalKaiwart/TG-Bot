import asyncio
import os
import nest_asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

nest_asyncio.apply()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running! Auto-stopping in 2 minutes...")

# Stop bot after 2 minutes
async def stop_after_delay(application):
    await asyncio.sleep(120)
    print("⏱️ 2 minutes passed. Stopping bot...")
    await application.shutdown()
    await application.stop()

# Main entry point
async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set.")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    # Start polling manually (non-blocking)
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Schedule stop after 2 minutes
    asyncio.create_task(stop_after_delay(application))

    # Wait until application is stopped
    await application.updater.wait_for_stop()
    await application.shutdown()
    await application.stop()

# Run the bot
asyncio.run(main())
