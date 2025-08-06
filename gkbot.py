import asyncio
import os
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Fix nested event loops issue
nest_asyncio.apply()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running! It will stop after 2 minutes.")

# Auto-stop function after delay
async def stop_after_delay(app, delay: int):
    await asyncio.sleep(delay)
    print("⏱️ 2 minutes completed. Stopping bot...")
    await app.stop()       # Stop the polling loop
    await app.shutdown()   # Then shutdown the app

# Main function
async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    # Start background auto-shutdown task
    asyncio.create_task(stop_after_delay(app, delay=120))

    # Start polling loop
    await app.run_polling()

# Run in the current event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
