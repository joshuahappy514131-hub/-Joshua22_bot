import asyncio
from openai import AsyncOpenAI
from config import OPENAI_API_KEY, MODEL
from services.logger import get_logger

logger = get_logger("OpenAIService")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are Joshua AI, an advanced conversational AI assistant. Your goal is to provide accurate, "
    "helpful, natural, and engaging responses. Understand the user's intent before answering. "
    "Maintain conversation context throughout the chat. Be friendly, professional, and concise "
    "unless the user requests more detail. If you are uncertain, acknowledge it rather than inventing facts."
)

async def fetch_ai_response(history: list) -> str:
    """Fetches AI response with exponential backoff on failure."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    max_retries = 3
    delay = 1.0

    for attempt in range(1, max_retries + 1):
        try:
            response = await client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"OpenAI attempt {attempt} failed: {e}")
            if attempt == max_retries:
                logger.error("All OpenAI retry attempts exhausted.")
                raise e
            await asyncio.sleep(delay)
            delay *= 2
