import sys
from types import FunctionType

from scripts.constants import cli as constants
from scripts.utils.logger import ConsoleLogger
from scripts.utils.exceptions import PythonVersionError
from scripts.cli.script_register.script_register import ScriptRegister

if sys.version_info < (3, 7):
    raise PythonVersionError('Python 3.7 or higher is required.')


class ScriptConsole:
    def __init__(self):
        self.__interrupted = False  # type: bool
        self.__initialized = True  # type: bool
        self.logger = ConsoleLogger()
        self.script_register = ScriptRegister(self)

    def is_initialized(self) -> bool:
        return self.__initialized

    def __interrupt(self):
        if self.__interrupted:
            print()
            for line in constants.GOODBYE_MESSAGE.split('\n'):
                if line:
                    self.logger.info(line)
            sys.exit()
        for line in constants.FIRST_INTERRUPT_MESSAGE.split('\n'):
            if line:
                self.logger.info(line)
            else:
                print()
        self.__interrupted = True

    @staticmethod
    def __command_parser(command: str | list, cmd_map: dict):
        if not (isinstance(command, str) or isinstance(command, list)):
            raise TypeError("Wrong command type!")
        if not isinstance(cmd_map, dict):
            raise TypeError("Wrong command map type!")

        if isinstance(command, str):
            command = command.split()

        def recursive_parser(cmd_node: str, others, relative_map: dict):
            if len(others) == 0:
                return relative_map[cmd_node[0]], None

            if cmd_node[0] in relative_map:

                if isinstance(relative_map[cmd_node], FunctionType):
                    return relative_map[cmd_node], others

                return recursive_parser(others[0], others[1:], relative_map[cmd_node[0]])

        return recursive_parser(command[0], command[1:], cmd_map)

    def __main_loop(self):
        for line in constants.WELCOME_MESSAGE.split('\n'):
            self.logger.info(line)
        while True:
            try:
                command = input('>>> ')
                res = self.__command_parser(command, ...,)
                if res[1] is None:
                    res[0]()
                else:
                    res[0](res[1])
                print()
            except KeyboardInterrupt:
                self.__interrupt()
            except Exception as e:
                self.logger.exception(e)

    def run(self):
        if self.__initialized:
            self.__main_loop()
