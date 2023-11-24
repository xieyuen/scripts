from _typeshed import Incomplete
from pathlib import Path

from scripts.utils.jsobj import JSObject
from typing import Any, Callable, Optional, TextIO, IO


class FileReader:
    __consts: JSObject
    TYPES: JSObject
    __file: Path
    __file_name: str
    __file_type: str
    __file_io: Optional[IO[Any]]
    def __init__(self, path: str, file_type: str = ...) -> None:         ...
    def change_file_type(self, value: str): ...
    def read(
            self,
            reader: Optional[Callable] = ...,
            *,
            encoding: str = ...,
            load_to_pyobj_first: bool = ...
    ) -> Any: ...
    @staticmethod
    def __read(file_io: TextIO, file_type: str) -> Any: ...
    def open(
            self,
            mode: str,
            buffering: int = ...,
            encoding: str | None = ...,
            errors: str | None = ...,
            newline: str | None = ...,
            closefd: bool = ...,
            opener: Callable[[str, int] ,int] | None = ...,
    ) -> IO[Any]: ...
    class __States:
        isOpened: bool
        isClosed: bool
        isExists: bool
        def __init__(self, file_reader): ...