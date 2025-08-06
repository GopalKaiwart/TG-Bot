import asyncio
import os
import nest_asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Enable nested event loop support (needed for some platforms like GitHub Actions)
nest_asyncio.apply()

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running! It will stop automatically in 2 minutes.")

# Function to stop the bot after a delay
async def stop_after_delay(application):
    await asyncio.sleep(120)  # Wait for 2 minutes
    print("⏱️ 2 minutes passed. Stopping bot...")
    await application.shutdown()
    await application.stop()

# Main function
async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("❌ BOT_TOKEN environment variable not set!")

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    async with application:
        # Start the bot and stop it after 2 minutes
        asyncio.create_task(stop_after_delay(application))
        await application.run_polling()

# Start everything
asyncio.run(main())
