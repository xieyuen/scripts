"""
导入时用 `from scripts.crawler import *` 就可以了
"""

from .music import main as music_crawler
from .picture import main as picture_crawler


__all__ = [
    "music_crawler",
    "picture_crawler",
]
