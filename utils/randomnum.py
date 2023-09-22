from random import randint as ri

from . import logger


class MainProgram:
    def __init__(self, sys_argv):
        self.args = {
            k: v
            for item in sys_argv[1:]
            for k, v in item.split('=')
        }

        # --- Some important arguments and configs --- #
        self.max = int(self.args.get('--max', 62))
        self.min = int(self.args.get('--min', 1))
        self.ignore_list = eval(self.args.get('--ignore-list', '[]')) + eval(self.args.get('--ignore', '[]'))
        self.disable_dedup = self.args.get('--disable-dedup', 'false').lower() == 'true'
        self.enable_save = self.args.get('--enable-save', 'false').lower() == 'true'
        self.enable_cli = self.args.get('--enable-cli', 'false').lower() == 'true' or self.args.get('--enable-console', 'false').lower() == 'true'
        self.enable_map = self.args.get('--enable-map', 'false').lower() == 'true'
        self.map = eval(self.args.get('--map', 'None'))

        # --- temp vars --- #
        self.last = self.new = []

    def __main(self) -> int:
        r = ri(self.min, self.max)
        while r in self.new and not self.disable_dedup and r in self.ignore_list:
            r = ri(self.min, self.max)
        self.new.append(r)
        return r

    def __save(self, name='return'):
        try:
            import yaml
        except ModuleNotFoundError:
            logger.error('YAML module not found.')
            logger.debug('Instead of YAML, JSON is used.')
            import json
            with open(f'{name}.json', 'w') as f:
                json.dump([self.last, self.new], f)
        else:
            with open(f'{name}.yaml', 'w') as f:
                yaml.dump(dict(last=self.last, new=self.new), f)

    def __cli(self):
        logger.info('Console has been started.')
        while True:
            times = int(input('请输入抽取次数: '))
            for _ in range(times):
                self.__main()

    def run(self, runtimes=None):
        if self.enable_cli:
            self.__cli()
            if self.enable_save:
                self.__save()
            return
        if runtimes is None:
            raise ValueError('No runtimes provided.')
        for _ in range(runtimes):
            logger.info(f'恭喜第 {self.__main()} 号被抽中！')
        if self.enable_save:
            self.__save()


if __name__ == '__main__':
    import sys
    MainProgram(sys.argv).run()
