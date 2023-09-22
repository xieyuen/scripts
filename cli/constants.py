from sys import version as py_version

from .. import info as _info

WELCOME_MESSAGE = """Package version: {0}, Python version: {1}
This is a open source project, u can see it in github: {2}

u can get help massage in github or typing 'help' command.""" \
.format(_info.VERSION, py_version, _info.GITHUB_REPOSITORY)

FIRST_INTERRUPT_MESSAGE = """
Is this interrupt a false touch?
"""

GOODBYE_MESSAGE = "Goodbye!"

AUTHOR = _info.AUTHOR
