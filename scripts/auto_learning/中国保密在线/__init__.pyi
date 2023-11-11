import threading
from _typeshed import Incomplete

class ChildThread(threading.Thread):
    threadID: Incomplete
    name: Incomplete
    url: Incomplete
    video_id: Incomplete
    def __init__(self, threadID, name, url, video_id: Incomplete | None = ...) -> None: ...
    def run(self) -> None: ...

def main(_x: int = ..., _y: int = ..., typing: str = ..., kill: Incomplete | None = ...) -> None: ...
