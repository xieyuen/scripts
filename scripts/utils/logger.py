import sys

from loguru._logger import Core, Logger

__all__ = ["ConsoleLogger", "logger"]


class ConsoleLogger:
    def __init__(self):
        self._logger = Logger(
            core=Core(),
            exception=None,
            depth=0,
            record=False,
            lazy=False,
            colors=False,
            raw=False,
            capture=True,
            patchers=[],
            extra={},
        )
        self._logger.remove()
        self._logger.add(
            sys.stdout,
            format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] | {message}",
            level="DEBUG",
        )
        self._logger.add(
            "logs/latest.log",
            format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] | {message}",
            level="DEBUG",
            rotation="1 week",
            retention="100 days",
            encoding="utf-8",
        )

        self.trace = self._logger.trace
        self.debug = self._logger.debug
        self.info = self._logger.info
        self.success = self._logger.success
        self.warning = self._logger.warning
        self.warn = self._logger.warning
        self.error = self._logger.error
        self.critical = self._logger.critical
        self.crit = self._logger.critical
        self.catch = self._logger.catch
        self.exception = self._logger.exception


logger = ConsoleLogger()
