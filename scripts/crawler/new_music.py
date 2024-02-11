from threading import Thread
from typing import TypedDict, Literal, Optional, Tuple, List

import jsonpath
import requests

from scripts.utils.config_manager import ConfigurationManager
from scripts.utils.logger import logger


class ParamDict(TypedDict):
    input: str
    filter: Literal['name']
    type: Literal['netease', 'qq', 'kugou', 'kuwo', 'baidu', 'ximalaya']
    page: int


class Temp:
    def __init__(self):
        self.__ignore = None

    @property
    def ignore(self):
        return self.__ignore

    @ignore.setter
    def ignore(self, value):
        self.__ignore = value


class Constants:
    MUSIC_NOT_FOUND_MESSAGE = "对不起，暂无搜索结果!"
    SEARCH_URL = 'https://music.liuzhijin.cn/'
    HEADERS = {
        "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/87.0.4280.141 Safari/537.36",
        # 判断请求是异步还是同步
        "x-requested-with": "XMLHttpRequest",
    }
    PLATFORM_INFORMATION = (
        "1.网易云:netease\n"
        "2.QQ:qq\n"
        "3.酷狗:kugou\n"
        "4.酷我:kuwo\n"
        "5.百度:baidu\n"
        "6.喜马拉雅:ximalaya"
    )
    PLATFORM_MAP = {
        k: v for keys, v in (
            (
                (
                    '1', 'n', 'net', 'wy', 'wyy', 'wangyi', 'wangyiyun', 'netease', '网易', '网易云', '网易云音乐'
                ), 'netease'
            ), (
                (
                    '2', 'q', 'qq', 'qqmusic', 'qqyinyue', 'qq音乐', 'qq 音乐'
                ), 'qq'
            ), (
                (
                    '3', 'kg', 'ku', 'kou', 'gou', 'kugou', '酷狗'
                ), 'kugou'
            ), (
                (
                    '4', 'kw', 'ko', 'wo', 'kuwo', '酷我'
                ), 'kuwo'
            ), (
                (
                    '5', 'b', 'bd', 'bu', 'baidu', '百度'
                ), 'baidu'
            ), (
                (
                    '6', 'x', 'xi', 'xmly', 'xmla', 'ximalaya', '喜马拉雅'
                ), 'ximalaya'
            ),
        ) for k in keys
    }
    PLATFORM_NAMES_MAP = {
        'netease': '网易云音乐',
        'qq': 'QQ音乐',
        'kugou': '酷狗音乐',
        'kuwo': '酷我音乐',
        'baidu': '百度',
        'ximalaya': '喜马拉雅',
    }
    DEFAULT_CONFIGURATION = {
        "timeout": 10,
        "save_path": "./crawler",
    }


def get_param(name: str, platform: str) -> ParamDict:
    return {
        "input": name,
        "filter": "name",
        "type": Constants.PLATFORM_MAP[platform],
        "page": 1,
    }


def get_platform_name(platform):
    return Constants.PLATFORM_NAMES_MAP[Constants.PLATFORM_MAP[platform]]


class DownloadThread(Thread):
    def __init__(self, url, author, title, *, path):
        super().__init__()
        self.args = (url, author, title, path)

    def run(self):
        url, author, title, path = self.args
        logger.info(f'正在下载 {author}-{title} ...')
        try:
            with open(f"{path}/{title}-{author}.mp3", mode='wb') as f:
                f.write(requests.get(url).content)
            logger.info(f'{author}-{title} 下载完成!')
        except Exception as e:
            logger.error(f'{author}-{title} 下载失败: {e}')


class SearchThread(Thread):
    def __init__(self, name, platform, timeout):
        super().__init__()
        self.name = name
        self.platform = platform
        self.timeout = timeout
        self.__result = None  # type: Optional[Tuple[List[str], List[str], List[str]]]

    @property
    def result(self):
        return self.__result

    def run(self):
        logger.info(f'正在{get_platform_name(self.platform)}平台查询中')
        param = get_param(self.name, self.platform)
        try:
            res = requests.post(
                url=Constants.SEARCH_URL,
                data=param,
                headers=Constants.HEADERS,
                timeout=self.timeout
            ).json()
        except TimeoutError:
            logger.error(f'在{get_platform_name(self.platform)}中搜索超时')
            return
        titles = jsonpath.jsonpath(res, '$..title')
        authors = jsonpath.jsonpath(res, '$..author')
        urls = jsonpath.jsonpath(res, '$..url')

        if not titles:
            logger.error(f'在{get_platform_name(self.platform)}中的搜索结果为空')
            return

        assert urls, '未获得下载url'

        self.__result = titles, authors, urls


class Crawler:
    def __init__(self):
        self.__cm = ConfigurationManager(
            './config.yml',
            default=Constants.DEFAULT_CONFIGURATION
        )
        self.timeout = self.__cm.config['timeout']
        self.save_path = self.__cm.config['save_path']

    def run(self):
        logger.info("欢迎使用python音乐自助下载脚本")
        name = input("请输入歌曲名:")
        platforms = input(
            "脚本支持以下平台:\n"
            f"{Constants.PLATFORM_INFORMATION}\n"
            "请选择平台(可多个,用英文逗号隔开): "
        ).split(',')
        assert platforms, "请选择至少一个平台"

        # 搜索线程
        search_threads = [
            SearchThread(platform, name, self.timeout)
            for platform in platforms
        ]
        for st in search_threads:
            st.start()
        for st in search_threads:
            st.join()

        # 打印结果
        index = 1
        titles, authors, urls = [], [], []
        for st in search_threads:
            if st.result is None:
                continue
            print(f"{get_platform_name(st.platform)}平台:")
            for title, author, _ in zip(*st.result):
                print(f'{index} | {title} - {author}')
                index += 1
            titles.extend(st.result[0])
            authors.extend(st.result[1])
            urls.extend(st.result[2])

        download_index = [int(i) for i in input("请输入要下载的歌曲序号(可多个,用英文逗号隔开): ").split(',')]
        assert download_index, "请选择至少一首歌曲"

        download_threads = [
            DownloadThread(urls[i - 1], titles[i - 1], authors[i - 1], path=self.save_path)
            for i in download_index
        ]
        for dt in download_threads:
            dt.start()
        for dt in download_threads:
            dt.join()

        logger.success("下载完成！")


if __name__ == '__main__':
    Crawler().run()
