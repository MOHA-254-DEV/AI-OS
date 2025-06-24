# File: core/memory_manager/utils.py

import hashlib
import re
from typing import List

def generate_key(data: str) -> str:
    """
    Generate a unique SHA-256 hash key from input data.
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def compress_memory(data: str, max_length: int = 1000) -> str:
    """
    Compress memory data by stripping whitespace, flattening lines, and truncating.
    """
    clean = re.sub(r'\s+', ' ', data.strip())
    return clean[:max_length]

def tokenize(text: str) -> List[str]:
    """
    Tokenize input text into a list of words.
    """
    return text.strip().split()
