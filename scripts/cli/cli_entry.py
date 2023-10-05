import sys
from argparse import ArgumentParser

from scripts.cli.run import run


__all__ = ['cli_dispatch']


def cli_dispatch():
    if len(sys.argv) == 1:
        run()
        return
