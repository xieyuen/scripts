import asyncio
from typing import TypedDict, Literal, Optional, Tuple, List

import aiohttp
import jsonpath

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


class Crawler:
    def __init__(self):
        pass

    async def download(self, url, author, title):
        logger.info(f'正在下载 {author}-{title} ...')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(connect=self.timeout)) as response:
                    data = await response.read()

            with open(f"{self.save_path}/{author}-{title}.mp3", 'wb') as f:
                f.write(data)

            logger.success(f'{author}-{title} 下载完成!')

        except Exception as e:
            logger.error(f'{author}-{title} 下载失败: {e}')

    async def search(self, name, platform) -> Optional[Tuple[List[str], List[str], List[str]]]:
        platform_name = get_platform_name(platform)
        timeout = aiohttp.ClientTimeout(connect=self.timeout)
        param = get_param(name, platform)

        logger.info(f'正在{platform_name}平台查询中')

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(Constants.SEARCH_URL, params=param, timeout=timeout) as response:
                    data = await response.json()

        except asyncio.TimeoutError:
            logger.error(f'{platform_name}平台查询超时')
            return

        titles = jsonpath.jsonpath(data, '$..title')
        authors = jsonpath.jsonpath(data, '$..author')
        urls = jsonpath.jsonpath(data, '$..url')

        if not titles:
            logger.error(f'在{platform_name}中的搜索结果为空')
            return

        assert urls, '未获得下载url'

        return titles, authors, urls

    async def main(self):
        logger.info("欢迎使用python音乐自助下载脚本")
        name = input("请输入歌曲名:")
        platforms = input(
            "脚本支持以下平台:\n"
            f"{Constants.PLATFORM_INFORMATION}\n"
            "请选择平台(可多个,用英文逗号隔开): "
        ).split(',')
        assert platforms, "请选择至少一个平台"

        # 搜索&打印信息
        logger.info('正在查找...')
        result = await asyncio.gather(
            *(self.search(name, platform) for platform in platforms)
        )

        titles = []
        authors = []
        urls = []
        index = 1
        for platform, res in zip(platforms, result):
            pn = get_platform_name(platform)
            print(f"{pn}平台：")
            for title, author, url in zip(*res):
                print(f"{index} | {title} - {author}")
                titles.append(title)
                authors.append(author)
                urls.append(url)

        download_index = [
            int(i) - 1
            for i in input(
                "请输入要下载的歌曲序号(可多个,用英文逗号隔开): "
            ).split(',')
        ]
        assert download_index, "请选择至少一首歌曲"

        await asyncio.gather(*(
            asyncio.create_task(self.download(url, title, author))
            for url, title, author in zip(urls, titles, authors)
        ))

        logger.success("下载完成！")

    @classmethod
    def run(cls):
        asyncio.run(cls().main())


if __name__ == '__main__':
    Crawler.run()
