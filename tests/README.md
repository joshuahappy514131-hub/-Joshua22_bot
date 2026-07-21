# 🤖 @Joshua22_bot - Production-Ready Telegram AI Assistant

A resilient, scalable, and production-grade Telegram AI assistant built using **Python 3.12**, **python-telegram-bot v21+**, and the latest **OpenAI Responses API**. Designed with full thread-safe conversation memory, inactivity timeouts, rate limiting, and long-message splitting.

---

## Features

- **Natural AI Conversational Engine:** Powered by OpenAI models (`gpt-4o`).
- **Sliding-Window Memory & Timeouts:** Preserves individual chat history per user and auto-clears inactive sessions.
- **Rate Limiting & Spam Protection:** Protects bot resources from request flooding.
- **Long Message Support:** Automatically slices replies exceeding character limits into clean consecutive messages.
- **Typing Indicator Support:** Displays dynamic typing animation during generation steps.
- **Cloud Ready:** Fully optimized for seamless deployment on Railway and hosting via GitHub.

---

## Commands Reference

- `/start` - Launches introductory greeting
- `/help` - Lists bot menu instructions
- `/about` - Information about Joshua AI
- `/clear` - Clears conversation history context
- `/ping` - Checks bot response latency and uptime

---

## Local Installation

1. **Clone repository:**
   ```bash
   git clone [https://github.com/your-username/Joshua22-Bot.git](https://github.com/your-username/Joshua22-Bot.git)
   cd Joshua22-Bot
