from _typeshed import Incomplete
from os import PathLike
from typing import List, Dict, Optional, Any

__version__: str


class MainProgram:
    args: Dict[str, str]
    last: List[int]
    new: List[int]
    max: int
    min: int
    runtimes: Optional[int]
    ignore_list: List[int]
    enable_increase: bool
    increase_list: List[int]
    disable_dedup: bool
    enable_save: bool
    enable_cli: bool
    enable_map: bool
    map: Dict[int, Any]
    encoding: str
    map_file: str
    def __init__(self, args) -> None: ...
    def run(self, runtimes: Incomplete | None = ...) -> None: ...
    def __load_map_from_file(self) -> None: ...
    def __main(self) -> int: ...
    def __check_config(self) -> None: ...
    def __save(self, name: str = ...) -> None: ...
    def __cli(self) -> None: ...

def main(args): ...
