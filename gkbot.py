import asyncio
import os
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Allow nested event loops (fix for GitHub Actions)
nest_asyncio.apply()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running! It will stop after 2 minutes.")

# Auto-stop the bot
async def stop_after_delay(app, delay: int):
    await asyncio.sleep(delay)
    print("⏱️ 2 minutes completed. Stopping bot.")
    await app.shutdown()
    await app.stop()

# Main bot runner
async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    # Schedule auto-shutdown after 2 minutes (120 seconds)
    asyncio.create_task(stop_after_delay(app, delay=120))

    await app.run_polling()

# Run bot in existing event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
