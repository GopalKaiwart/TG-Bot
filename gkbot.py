import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Allow nested event loops (fix for GitHub Actions)
nest_asyncio.apply()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running...")

# Auto-stop function
async def stop_after_delay(app, delay: int):
    await asyncio.sleep(delay)
    print("⏱️ Auto-stopping after 2 minutes.")
    await app.shutdown()

async def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))

    # Schedule shutdown
    asyncio.create_task(stop_after_delay(app, delay=120))

    # Start polling
    await app.run_polling()

# Run the bot inside current loop (GitHub Actions safe)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
