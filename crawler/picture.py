import os

import requests

from .. import logger


def main(url: str, path: str = './img/') -> bool:
    """
    图片爬虫主程序
    :param url: 图片链接
    :param path: 图片保存路径
    :return: 是否成功
    """

    file_path = path + url.split('/')[-1]

    # 创建文件夹（如果 { _root } 不存在的话）
    if not os.path.exists(path):
        os.mkdir(path)

    try:
        if not os.path.exists(file_path):
            req = requests.get(url)
            with open(file_path, 'wb') as f:
                f.write(req.content)
                f.close()
                logger.success('图片已保存')
                return True
        else:
            logger.error('文件爬取失败')
            return False
    except:
        logger.error('爬取失败')
        return False
