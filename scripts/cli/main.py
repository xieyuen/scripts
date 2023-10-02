import sys

from . import constants
from ..utils import logger
from ..utils.exceptions import PythonVersionError

if sys.version_info < (3, 7):
    raise PythonVersionError('Python 3.7 or higher is required.')
del sys


class MainProgram:
    def interrupt(self):
        if self._interrupt:
            for line in constants.GOODBYE_MESSAGE.split('\n'):
                if line:
                    logger.info(line)
                else:
                    print()
            _interrupt = True
            return
        for line in constants.FIRST_INTERRUPT_MESSAGE.split('\n'):
            if line:
                logger.info(line)
            else:
                print()
        sys.exit(-1)

    def __init__(self):
        self._interrupt = False
        if len(sys.argv) > 1:
            self.args = sys.argv[1:]

    def main(self):
        for line in constants.WELCOME_MESSAGE.split('\n'):
            logger.info(line)
        while True:
            try:
                command = input('>>> ')
                command.list = command.split()
            except KeyboardInterrupt:
                self.interrupt()


if __name__ == '__main__':
    pass
