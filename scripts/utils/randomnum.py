"""
这个是我专门为班里写的脚本，可以快速抽人
主要是使用命令行操控
当然，它肯定不止抽人，这只是 random.randint 的一个简单包装
它有什么更多的用法还请自行探索

几个参数以及其默认值:

必须参数：
    --max   最大值
    --min   最小值

可选参数：
    --enable-cli=true       是否启用控制台
    --enable-console        同 --enable-cli
    --save=true             是否保存结果
    -s                      同 --save
    --enable-map=false      是否启用号码与人的映射
        --map={}                号码与人的映射，仅在--enable-map=true时有效
                                请以 python 的字典形式进行输入，例如：--map={1:'张三', 2:'李四'}
    --disable-dedup=false   是否禁用去重
    --ignore-list=[]        忽略列表，仅限整数，并且是在 --min 和 --max 之间的整数，其他的均无效
                            和 --map 一样，请使用 python 格式输入，例如：--ignore-list=[1, 2, 3]
    --ignore                同 --ignore-list

注意：所有的参数都需要输入值，否则为默认值。
但如果你输入了前半部分而没有输入等号及后面的，这将会抛出 ValueError
"""

from random import randint as ri

from scripts.utils.logger import logger


__version__ = '0.1'


def str2bool(obj: str) -> bool:
    if not isinstance(obj, str):
        raise TypeError
    if obj.lower() == 'true':
        return True
    elif obj.lower() == 'false':
        return False
    else:
        raise ValueError(f'{obj} 不是有效的 bool 值')


class MainProgram:
    def __init__(self, args):
        if len(args) == 0 or '-h' in args or '--help' in args:
            print(__doc__)
            exit()
        # 将传入的参数转化为字典
        self.args = {
            k: v
            for item in args
            for k, v in (item.split('='),)
        }

        self.last = []
        self.new = []

        # --- Some important arguments and configs --- #
        self.max = int(self.args['--max'])
        self.min = int(self.args['--min'])
        self.runtimes = self.args.get('--runtimes', None)
        if self.runtimes is not None:
            self.runtimes = int(self.runtimes)
        self.ignore_list = (
            eval(self.args.get('--ignore-list', '[]'))
            + eval(self.args.get('--ignore', '[]'))
        )
        self.disable_dedup = str2bool(self.args.get('--disable-dedup', 'false'))
        self.enable_save = (
            str2bool(self.args.get('--save', 'false'))
            or str2bool(self.args.get('-s', 'false'))
        )
        self.enable_cli = (
            str2bool(self.args.get('--enable-cli', 'false'))
            or str2bool(self.args.get('--enable-console', 'false'))
        )
        self.enable_map = str2bool(self.args.get('--enable-map', 'false'))
        self.map = eval(self.args.get('--map', 'None'))  # TODO: 从文件读取映射表 考虑支持 .py .json .yaml .txt

        self.__check_config()

    def __check_config(self):
        if self.max < self.min:
            raise ValueError('The max number is smaller than the min number.')
        if self.runtimes is not None:
            if self.runtimes < 1:
                raise ValueError('The runtimes must be greater than 0.')
            if self.runtimes > (self.max - self.min + 1) and not self.disable_dedup:
                raise ValueError('Argument:runtimes grater than Argument:max - Argument:min + 1 but enable dedup')
        if self.enable_map:
            if not isinstance(self.map, dict):
                raise TypeError('Argument:map must be a dict.')
            if not all(isinstance(i, int) for i in self.map.keys()):
                if not all(isinstance(i, int) for i in self.map.values()):
                    raise TypeError('Argument:map keys must be int.')
                logger.warning('It seems that the map key is inverse with the value?')
                logger.warning('Program will reverse the key to the value.')
                self.map = {v: k for k, v in self.map.items()}
            if len(self.map) < (self.max - self.min + 1):
                logger.warning('The map is not enough.')
                logger.warning('This may result in drawn numbers cannot matching')
                logger.warning('The program will ignore this error')

    def __load_map_from_file(self):
        # TODO: 从文件读取映射表
        #       考虑支持 .py .json .yaml .txt
        pass

    def __main(self) -> int:
        r = ri(self.min, self.max)
        while (
            (not self.disable_dedup and r in self.new)
            or r in self.ignore_list
        ):
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
                json.dump(
                    obj=dict(last=self.last, new=self.new),
                    fp=f,
                )
        else:
            with open(f'{name}.yaml', 'w') as f:
                yaml.dump(
                    data=dict(last=self.last, new=self.new),
                    stream=f,
                )

    def __cli(self):
        logger.info('Console has been started.')
        while True:
            times = int(input('请输入抽取次数: '))
            for _ in range(times):
                self.__main()
                logger.info(
                    f'恭喜第 {self.new[-1]} 号被抽中！'
                    + (f'TA 是 {self.map[self.new[-1]]}' if self.enable_map else '')
                )

    def run(self, runtimes=None):
        self.last = self.new.copy()
        self.new = []
        if self.enable_cli:
            self.__cli()
            if self.enable_save:
                self.__save()
            return
        if runtimes is None:
            if self.runtimes is None:
                raise ValueError('No runtimes provided.')
            runtimes = self.runtimes
        for _ in range(runtimes):
            r = self.__main()
            logger.info(f'恭喜第 {r} 号被抽中！' + (f'TA 是 {self.map[r]}' if self.enable_map else ''))
        if self.enable_save:
            self.__save()


def main(args):
    try:
        program = MainProgram(args)
        program.run()
    except KeyboardInterrupt:
        exit(0)
    except BaseException as e:
        logger.critical('出现了一个异常')
        logger.exception(e)
        exit(1)


if __name__ == '__main__':
    main(__import__('sys').argv[1:])
