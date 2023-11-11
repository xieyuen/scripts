from _typeshed import Incomplete
from scripts.utils.file_reader import FileReader as FileReader
from scripts.utils.logger import logger as logger
from scripts.utils.string_to import str2bool as str2bool

__version__: str

class MainProgram:
    args: Incomplete
    last: Incomplete
    new: Incomplete
    max: Incomplete
    min: Incomplete
    runtimes: Incomplete
    ignore_list: Incomplete
    enable_increase: Incomplete
    increase_list: Incomplete
    disable_dedup: Incomplete
    enable_save: Incomplete
    enable_cli: Incomplete
    enable_map: Incomplete
    map: Incomplete
    encoding: Incomplete
    map_file: Incomplete
    def __init__(self, args) -> None: ...
    def run(self, runtimes: Incomplete | None = ...) -> None: ...

def main(args): ...
