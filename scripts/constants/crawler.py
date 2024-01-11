URL = "https://music.liuzhijin.cn/"

USER_AGENT = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

HEADERS = {
    **USER_AGENT,
    # 判断请求是异步还是同步
    "x-requested-with": "XMLHttpRequest",
}

BILIBILI_HEADERS = {
    **USER_AGENT,
    "referer": "https://www.bilibili.com/",
}

DEFAULT_SAVE_PATH = "./crawler_downloads/"
