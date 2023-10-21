"""
音乐爬虫 awa
使用爬虫请调用`Crawler.Music.main_program()`这个函数awa
支持：
    1.网易云:netease
    2.QQ:qq
    3.酷狗:kugou
    4.酷我:kuwo
    5.百度:baidu
    6.喜马拉雅:ximalaya
"""

import os

import jsonpath
import requests

from scripts.utils.logger import logger
from scripts.constants.crawler import URL, HEADERS, DEFAULT_SAVE_PATH


"""
编程思路：
    1.url
    2.模拟浏览器请求
    3.解析网页源代码
    4.保存数据
"""


def get_music_platform():
    logger.info("音乐平台列表")
    print(
        "1.网易云: netease\n"
        "2.QQ: qq\n"
        "3.酷狗: kugou\n"
        "4.酷我: kuwo\n"
        "5.百度: baidu\n"
        "6.喜马拉雅: ximalaya"
    )
    logger.info("你可以输入数字来选择平台，也可以直接输入平台名称、平台缩写或英文来选择 awa")
    _input = input(":")
    logger.trace(f"用户输入: {_input}")
    return invert_platform(_input)


def invert_platform(platform: str = "n"):
    """
    检测并转换平台参数(大小写均可识别)
    """
    if not isinstance(platform, str):
        platform = str(platform)

    match platform.lower():
        # 网易云 netease
        case "1" | "n" | "net" | "wy" | \
             "wyy" | "wangyi" | "wangyiyun" | "netease" | \
             "网易" | "网易云" | "网易云音乐":

            return "netease"

        # QQ qq
        case "2" | "q" | "qq" | "qqmusic" | \
             "qqyinyue" | "qq音乐" | "qq 音乐":

            return "qq"

        # 酷狗 kugou
        case "3" | "kg" | "ku" | "kou" | "gou" | "kugou" | "酷狗":

            return "kugou"

        # 酷我 kuwo
        case "4" | "kw" | "ko" | "wo" | "kuwo" | "酷我":

            return "kuwo"

        # 百度 baidu
        case "5" | "b" | "bd" | "bu" | "baidu" | "百度":

            return "baidu"

        # 喜马拉雅 ximalaya
        case "6" | "x" | "xi" | "xmly" | "xmla" | "ximalaya" | "喜马拉雅":

            return "ximalaya"

        # 无法识别
        case _:
            logger.error(f'无法识别到你输入的 "{platform}" 平台')
            __check = int(input("请选择操作："
                                "  [1]重新输入参数\n"
                                "  [2]使用默认值"))
            print("-------------------------------------------------------")
            if __check == 1:
                get_music_platform()
            if __check == 2:
                return "netease"


def download_music(url, title, author, *, path: str = DEFAULT_SAVE_PATH):
    # 创建文件夹(如果不存在的话)
    if not os.path.exists(path):
        os.makedirs("music", exist_ok=True)
    logger.info("歌曲:{0}-{1},正在下载...".format(title, author))

    # 下载（这种读写文件的下载方式适合少量文件的下载）
    content = requests.get(url).content
    with open(
        file=path + title + " " + author + ".mp3",
        mode="wb"
    ) as f:
        f.write(content)

    logger.success(f"下载完毕,{title}-{author},请注意检查文件是否正常可用")


def main(
    name: str = None,
    platform: str = None,
    *, path: str = DEFAULT_SAVE_PATH
) -> bool:

    """
    音乐爬虫主程序
    :param name: 歌曲名称
    :param platform: 搜索平台
    :param path: 下载路径

    :return bool: 是否成功
    """

    # 获取相关信息
    if name is None:
        name = input("请输入歌曲名称:")
    if platform is None:
        platform = get_music_platform()  # 获取搜索的平台
    else:
        platform = invert_platform(platform)

    logger.info("正在搜索...")

    # 请求参数
    param = {
        "input": name,
        "filter": "name",
        "type": platform,
        "page": 1,
    }

    # 发起请求
    res = requests.post(
        url=URL, data=param, headers=HEADERS
    )
    json_text = res.json()
    title = jsonpath.jsonpath(json_text, "$..title")
    author = jsonpath.jsonpath(json_text, "$..author")
    url = jsonpath.jsonpath(json_text, "$..url")

    if title:
        logger.info("找到以下歌曲:")
        songs = list(zip(title, author))
        for s in songs:
            logger.info(s[0], s[1])
        print("-------------------------------------------------------")
        index = int(input("请输入您想下载的歌曲版本:"))
        download_music(url[index], title[index], author[index], path=path)
        return True
    else:
        logger.warning("对不起，暂无搜索结果!")
        return False


if __name__ == '__main__':
    main()
