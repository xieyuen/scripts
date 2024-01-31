"""
Music Crawler

支持网易云、QQ、酷狗、酷我、百度和喜马拉雅
搜索技术由 `https://music.liuzhijin.cn/` 提供支持
"""

import os
from typing import TypedDict, Literal, List

import requests
from jsonpath import jsonpath

from scripts.utils.decorators import curry
from scripts.utils.exceptions import MusicNotFoundError, PathNotExistsError
from scripts.utils.logger import logger


class Constants:
    MUSIC_NOT_FOUND_MESSAGE = "对不起，暂无搜索结果!"
    DEFAULT_SAVE_PATH = './'
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


class Temp:
    def __init__(self):
        self.__ignore = None

    @property
    def ignore(self):
        return self.__ignore

    @ignore.setter
    def ignore(self, value):
        self.__ignore = value


class Param(TypedDict):
    input: str
    filter: Literal['name']
    type: Literal['netease', 'qq', 'kugou', 'kuwo', 'baidu', 'ximalaya']
    page: int


class Crawler:

    def __init__(self):
        self.temp = Temp()

    @staticmethod
    def getParam(name: str, platform: str) -> Param:
        return {
            "input": name,
            "filter": "name",
            "type": Constants.PLATFORM_MAP[platform],
            "page": 1,
        }

    @staticmethod
    def getPlatformName(platform):
        return Constants.PLATFORM_NAMES_MAP[Constants.PLATFORM_MAP[platform]]

    @staticmethod
    @curry
    def download(url, author, title, *, path):
        logger.info(f'{author}-{title} 正在下载...')
        try:
            with open(f"{path}/{title}-{author}.mp3", mode='wb') as f:
                f.write(requests.get(url).content)
            logger.info(f'{author}-{title} 下载完成!')
        except Exception as e:
            logger.error(f'{author}-{title} 下载失败: {e}')

    @staticmethod
    def getIgnoredArgs(ignored_indexes, *args) -> List:
        def _get(a):
            res = []
            for index, item in enumerate(a):
                if index in ignored_indexes:
                    continue
                for i in item:
                    res.append(i)

        return [_get(i) for i in args]

    def printSearchedInfo(
            self,
            platforms: List[str],
            titles: List[str],
            authors: List[str],
            urls: List[str],
    ):
        """
        打印搜索到的音乐信息并将搜索失败的平台索引记录在 self.temp.ignore 中
        """
        index = 1
        ignoredIndexes = []
        for i, (platform, tits, authors_in_plat, u) in enumerate(zip(platforms, titles, authors, urls)):
            platform = self.getPlatformName(platform)
            if not authors_in_plat:
                logger.warning(f'未在{platform}平台查询到歌曲')
                ignoredIndexes.append(i)
                continue
            if not u:
                logger.error(f'{platform}平台解析出现问题，可以进入网站{Constants.SEARCH_URL}查看此歌曲是否有下载链接')
                continue
            logger.info(f"{platform}平台:")
            for t, a in zip(tits, authors_in_plat):
                print(f"{index} | {t} - {a}")
                index += 1  # index++
        self.temp.ignore = ignoredIndexes

    def getSearchedInfo(self, name, platforms):
        titles = []
        authors = []
        urls = []

        for platform in platforms:
            param = self.getParam(
                name=name,
                platform=platform
            )
            json_text = requests.post(
                url=Constants.SEARCH_URL,
                data=param,
                headers=Constants.HEADERS,
            ).json()

            titles.append(jsonpath(json_text, '$..title'))
            authors.append(jsonpath(json_text, '$..author'))
            urls.append(jsonpath(json_text, '$..url'))

        if not all((not not i) for u in urls for i in u):
            assert False, '未获得下载url'

        return titles, authors, urls

    def main(self):
        logger.info("欢迎使用python音乐自助下载脚本")
        name = input("请输入歌曲名:")
        platforms = input(
            f"脚本支持以下平台:\n{Constants.PLATFORM_INFORMATION}\n请选择平台(可多个,用英文逗号隔开): "
        ).split(',')

        titles, authors, urls = self.getSearchedInfo(name, platforms)

        if not titles[0]:
            raise MusicNotFoundError(Constants.MUSIC_NOT_FOUND_MESSAGE)

        print("-------------------------------------------------------\n查找到以下歌曲:\n")

        self.printSearchedInfo(platforms, titles, authors, urls)

        titles, authors, urls = self.getIgnoredArgs(self.temp.ignore, titles, authors, urls)

        indexes = input("请输入您想下载的歌曲版本(填序号,多个用英文逗号隔开):").split(',')

        if not hasattr(Constants, 'savePath'):
            savePath = input("请输入保存路径(空则为脚本所在路径):")
        else:
            savePath = None

        if savePath:
            if not os.path.exists(savePath):
                raise PathNotExistsError(f'不存在的路径: {savePath}')
            download = self.download(path=savePath)
        else:
            download = self.download(path=Constants.DEFAULT_SAVE_PATH)

        for i in indexes:
            i = int(i) - 1
            download(urls[i], authors[i], titles[i])

    @staticmethod
    def run():
        import sys

        args = {
            key: value
            for item in sys.argv[1:]
            for key, value in [item.split('=')]
        }
        if '--path' in args:
            Constants.savePath = args['--path']

        instance = Crawler()
        instance.main()


if __name__ == '__main__':
    Crawler.run()
