import pytest
from utils import split_long_message

def test_split_long_message():
    short_text = "Hello world"
    assert split_long_message(short_text) == [short_text]

    long_text = "a" * 5000
    chunks = split_long_message(long_text, max_length=4000)
    assert len(chunks) > 1
    assert "".join(chunks) == long_text
