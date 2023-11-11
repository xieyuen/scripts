from _typeshed import Incomplete
from scripts.utils.jsobj import JSObject as JSObject
from typing import Any, Callable, Optional

class FileReader:
    constants: Incomplete
    TYPES: Incomplete
    file: Incomplete
    file_name: Incomplete
    file_type: Incomplete
    def __init__(self, path: str, file_type: str = ...) -> None: ...
    def change_file_type(self, value: str): ...
    def read(self, reader: Optional[Callable] = ..., *, encoding: str = ..., load_to_pyobj_first: bool = ...) -> Any: ...
