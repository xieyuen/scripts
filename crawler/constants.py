from .. import config


URL = "https://music.liuzhijin.cn/"

HEADERS = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    # 判断请求是异步还是同步
    "x-requested-with": "XMLHttpRequest",
}

DEFAULT_SAVE_PATH = "./save/"

