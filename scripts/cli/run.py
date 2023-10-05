import sys

from scripts.constants import core_constant
from scripts.cli.main import ScriptConsole


def run():
    print('{} {} is starting up'.format(core_constant.NAME, core_constant.VERSION))
    print('{} is open source, u can find it here: {}'.format(core_constant.NAME, core_constant.GITHUB_URL))

    try:
        console = ScriptConsole()
    except Exception as e:
        print('Fail to initialize Script Console: ({}) {}'.format( type(e), e), file=sys.stderr)
        raise

    if console.is_initialized():
        console.run()
    else:
        # If it's not initialized, config file or permission file is missing
        # Just don't do anything to let the user check the files
        pass
