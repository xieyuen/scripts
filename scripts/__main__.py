import platform
import sys

from scripts.cli import cli_entry


__all__ = ['entry_point']


def __env_check():
    py_version = sys.version_info.major + sys.version_info.minor / 10
    if py_version < 3.7:
        print("To run this script, Python 3.7 or higher is required.")
        print("Current Python version {} is too old".format(platform.python_version()))
        sys.exit(1)


def entry_point():
    """
    This is the entry point for the script.
    """
    __env_check()

    cli_entry.cli_dispatch()

