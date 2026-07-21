import time
import logging
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from ai import fetch_ai_response
from memory import conversation_service
from utils import split_long_message

logger = logging.getLogger("Handlers")
start_time = time.time()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "👋 **Welcome to Joshua AI!**\n\n"
        "I'm your intelligent AI assistant.\n"
        "I can read, understand, and reply to any message naturally.\n\n"
        "I can help with:\n"
        "• General questions\n"
        "• Coding\n"
        "• Writing\n"
        "• Homework\n"
        "• Translation\n"
        "• Business ideas\n"
        "• Summaries\n"
        "• Brainstorming\n"
        "• Technology\n"
        "• Everyday conversations\n\n"
        "Simply send me a message to get started."
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🤖 **Joshua AI Command Directory**\n\n"
        "• Send any text message to start chatting.\n"
        "• `/start` - Launch the welcome message\n"
        "• `/help` - View command guide\n"
        "• `/about` - Learn about @Joshua22_bot\n"
        "• `/clear` - Reset your session history\n"
        "• `/ping` - Check response latency"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = (
        "ℹ️ **About @Joshua22_bot**\n\n"
        "Joshua AI is a state-of-the-art conversational assistant designed to provide fast, accurate, "
        "and contextual responses securely across chat platforms."
    )
    await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    conversation_service.clear(chat_id)
    await update.message.reply_text("🧹 Your conversation history has been cleared.")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await update.message.reply_text(f"🏓 Pong! Bot status: Online\n⏱️ Uptime: {hours}h {minutes}m {seconds}s")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_text = update.message.text

    # Rate limiting check
    is_limited, wait_time = conversation_service.check_rate_limit(user_id)
    if is_limited:
        await update.message.reply_text(f"⏳ Please slow down. Try again in {wait_time} seconds.")
        return

    try:
        # Show Telegram typing action
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

        # Update conversation context memory
        conversation_service.add_message(chat_id, "user", user_text)
        history = conversation_service.get_history(chat_id)

        # Fetch OpenAI response
        ai_reply = await fetch_ai_response(history)

        # Store AI reply in context
        conversation_service.add_message(chat_id, "assistant", ai_reply)

        # Dispatch response chunks safely supporting long messages and Markdown
        for chunk in split_long_message(ai_reply):
            try:
                await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                # Fallback to plain text if Markdown syntax fails parsing
                await update.message.reply_text(chunk)

    except Exception as e:
        logger.error(f"Error handling user message: {e}")
        error_msg = "⚠️ An error occurred processing your request. Please try again shortly."
        await update.message.reply_text(error_msg)
