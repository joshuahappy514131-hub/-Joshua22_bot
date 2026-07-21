from typing import List

def split_long_message(text: str, max_length: int = 4000) -> List[str]:
    """Splits a long string into chunks respecting maximum Telegram text lengths."""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break
        
        # Try to find a newline or space to split cleanly
        split_index = text.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = text.rfind(' ', 0, max_length)
        if split_index == -1:
            split_index = max_length
            
        chunks.append(text[:split_index])
        text = text[split_index:].lstrip()
        
    return chunks
