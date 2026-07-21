import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN, validate_config

logger = logging.getLogger("App")

def main() -> None:
    validate_config()
    
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    from handlers import (
        start_command,
        help_command,
        about_command,
        clear_command,
        ping_command,
        handle_message
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("ping", ping_command))

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("Starting @Joshua22_bot polling service...")
    application.run_polling(allowed_updates=["message", "edited_message"])

if __name__ == "__main__":
    main()
