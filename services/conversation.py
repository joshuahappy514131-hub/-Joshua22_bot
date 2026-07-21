import time
from collections import defaultdict, deque
from typing import Dict, List, Tuple
from config import MAX_HISTORY, CONVERSATION_TIMEOUT_MINUTES, RATE_LIMIT_SECONDS

class ConversationService:
    def __init__(self):
        # chat_id -> deque of dicts {"role": str, "content": str}
        self.store: Dict[int, deque] = defaultdict(lambda: deque(maxlen=MAX_HISTORY))
        # chat_id -> timestamp of last activity
        self.last_active: Dict[int, float] = {}
        # user_id -> timestamp of last request for rate limiting
        self.last_request_time: Dict[int, float] = {}

    def _check_timeout(self, chat_id: int) -> None:
        """Cleans history if conversation has timed out due to inactivity."""
        if chat_id in self.last_active:
            elapsed_minutes = (time.time() - self.last_active[chat_id]) / 60
            if elapsed_minutes > CONVERSATION_TIMEOUT_MINUTES:
                self.clear(chat_id)

    def add_message(self, chat_id: int, role: str, content: str) -> None:
        self._check_timeout(chat_id)
        self.store[chat_id].append({"role": role, "content": content})
        self.last_active[chat_id] = time.time()

    def get_history(self, chat_id: int) -> List[Dict[str, str]]:
        self._check_timeout(chat_id)
        return list(self.store[chat_id])

    def clear(self, chat_id: int) -> None:
        if chat_id in self.store:
            self.store[chat_id].clear()
        if chat_id in self.last_active:
            del self.last_active[chat_id]

    def check_rate_limit(self, user_id: int) -> Tuple[bool, float]:
        """Returns (is_limited, time_remaining)."""
        now = time.time()
        last_time = self.last_request_time.get(user_id, 0.0)
        diff = now - last_time
        if diff < RATE_LIMIT_SECONDS:
            return True, round(RATE_LIMIT_SECONDS - diff, 1)
        self.last_request_time[user_id] = now
        return False, 0.0
