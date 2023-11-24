from _typeshed import Incomplete
from typing import Literal

from loguru._logger import Logger


class ConsoleLogger:
    trace: Incomplete
    debug: Incomplete
    info: Incomplete
    success: Incomplete
    warning: Incomplete
    warn: Incomplete
    error: Incomplete
    critical: Incomplete
    crit: Incomplete
    catch: Incomplete
    exception: Incomplete

    _logger: Logger

    def log_lines(self, msg: str, level: Literal[
        'trace', 'debug', 'info',
        'warning', 'warn', 'error',
        'critical', 'crit'
    ]): ...


logger: Incomplete
