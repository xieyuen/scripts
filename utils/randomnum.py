"""
这个是我专门为班里写的脚本，可以快速抽人
主要是使用命令行操控
当然，它肯定不止抽人，这只是 random.randint 的一个简单包装
它有什么更多的用法还请自行探索

你可以新写一个类从`MainProgram`继承

几个参数以及其默认值:

--max=62                学号最大值
--min=1                 学号最小值
--enable-cli=true       是否启用控制台
--enable-map=false      是否启用学号与人的映射
--map={}                学号与人的映射，仅在--enable-map=true时有效
                        请使用 python 格式输入，例如：{1:'张三', 2:'李四'}
--disable-dedup=false   是否启用去重
--ignore-list=[]        忽略列表，仅限整数，并且是在 --min 和 --max 之间的整数，其他的均无效
                        和 --map 一样，请使用 python 格式输入，例如：[1, 2, 3]

注意：所有的参数都需要输入值，否则为默认值。但如果你输入了前半部分而没有输入等号及后面的，
这将会抛出 ValueError
"""

from random import randint as ri

from . import logger


__version__ = '0.1'


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
        self.runtimes = self.args.get('--runtimes')
        self.ignore_list = eval(self.args.get('--ignore-list', '[]')) + eval(self.args.get('--ignore', '[]'))
        self.disable_dedup = self.args.get('--disable-dedup', 'false').lower() == 'true'
        self.enable_save = self.args.get('--enable-save', 'false').lower() == 'true' or self.args.get('-save', 'false').lower() == 'true'
        self.enable_cli = self.args.get('--enable-cli', 'false').lower() == 'true' or self.args.get('--enable-console', 'false').lower() == 'true'
        self.enable_map = self.args.get('--enable-map', 'false').lower() == 'true'
        self.map = eval(self.args.get('--map', 'None'))

        # --- temp vars --- #
        self.last = []
        self.new = []

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
                logger.info(
                    f'恭喜第 {self.new[-1]} 号被抽中！',
                    f'TA 是 {self.map[self.new[-1]]}' if self.enable_map else '',
                    sep='',
                )

    def run(self, runtimes=None):
        self.last = self.new.copy()
        self.new = []
        if self.enable_cli:
            self.__cli()
            if self.enable_save:
                self.__save()
            return
        while runtimes is None:
            if self.runtimes is not None:
                break
            raise ValueError('No runtimes provided.')
        for _ in range(runtimes):
            r = self.__main()
            logger.info(f'恭喜第 {r} 号被抽中！', f'TA 是 {self.map[r]}' if self.enable_map else '')
        if self.enable_save:
            self.__save()


if __name__ == '__main__':
    import sys
    MainProgram(sys.argv).run()
