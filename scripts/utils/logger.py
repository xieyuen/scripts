import sys
from typing import Literal, Tuple

from loguru._logger import Core, Logger

__all__ = ["logger"]
Levels = (
    'trace', 'debug', 'info',
    'warning', 'warn', 'error',
    'critical', 'crit'
)
LevelsLiteral = Literal[
    'trace', 'debug', 'info',
    'warning', 'warn', 'error',
    'critical', 'crit'
]


class FormatKeys:
    ELAPSED = "{elapsed}"
    EXCEPTION = "{exception}"
    EXTRA = "{extra}"
    FILE = "{file}"
    FUNCTION = "{function}"
    LEVEL = "{level}"
    LINE = "{line}"
    MESSAGE = "{message}"
    MODULE = "{module}"
    NAME = "{name}"
    PROCESS = "{process}"
    THREAD = "{thread}"


class GenericFormatString:
    def __init__(self, start_with: str = '[{time:YYYY-MM-DD HH:mm:ss}]'):
        self.__format_string = start_with

    def addElapsed(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.ELAPSED + bracket_with[1]
        return self

    def addException(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.EXCEPTION + bracket_with[1]
        return self

    def addExtra(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.EXTRA + bracket_with[1]
        return self

    def addFile(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.FILE + bracket_with[1]
        return self

    def addFunction(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.FUNCTION + bracket_with[1]
        return self

    def addLevel(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.LEVEL + bracket_with[1]
        return self

    def addLine(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.LINE + bracket_with[1]
        return self

    def addMessage(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.MESSAGE + bracket_with[1]
        return self

    def addModule(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.MODULE + bracket_with[1]
        return self

    def addName(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.NAME + bracket_with[1]
        return self

    def addProcess(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.PROCESS + bracket_with[1]
        return self

    def addThread(self, bracket_with: Tuple[str, str]):
        self.__format_string += bracket_with[0] + FormatKeys.THREAD + bracket_with[1]
        return self

    def getFormatString(self):
        return self.__format_string

    end = getFormatString


class GenericHelper:
    square_bracket = (' [', ']')
    angle_bracket = (' <', '>')
    parenthesis = (' <', '>')
    space = ' '
    empty = ''


FORMAT = (
    GenericFormatString(start_with='[{time:YYYY-MM-DD HH:mm:ss}]')
    .addLevel(GenericHelper.square_bracket)
    .addModule(GenericHelper.square_bracket)
    .addFunction(GenericHelper.square_bracket)
    .addMessage((' | ', ''))
    .getFormatString()
)  # '[{time:YYYY-MM-DD HH:mm:ss}] [{level}] [{module}] [{function}] | {message}'


class logger:
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
            format=FORMAT,
            level="DEBUG",
        )
        self._logger.add(
            "logs/latest.log",
            format=FORMAT,
            level="DEBUG",
            rotation="1 MB",
            retention="10 weeks",
            encoding="utf-8",
            compression="zip"
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

    def log_lines(self, msg: str, level: LevelsLiteral):
        """记录多行字符串"""
        if level.lower() not in Levels:
            raise ValueError('Arg:level must be one of the following.')
        level = level.lower()
        for m in msg.splitlines():
            self.__dict__[level](m)


logger = logger()
