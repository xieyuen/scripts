"""
这是 中国保密在线 (www.baomi.org.cn) 的自动学习脚本
"""

# 导入模块
import math
import os
import threading
import time
import webbrowser

import win32api
import win32con

from scripts.auto_learning.中国保密在线.url_and_time import URL_AND_TIME
from scripts.utils.logger import logger


__all__ = ['main']

# 全局变量
x: int
y: int


# 模拟鼠标点击
def mouse_click(__x, __y):
    """
    模拟鼠标点击

    :param __x: 横坐标
    :param __y: 纵坐标
    """
    win32api.SetCursorPos([__x, __y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 子线程
class ChildThread(threading.Thread):  # 继承父类threading.Thread

    def __init__(self, threadID, name, url, video_id=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.url = url
        if name == "play":
            self.video_id = video_id

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数

        if self.name == "chrome":
            time.sleep(0.1)
            url = self.url

            logger.info("已开启浏览器，请不要乱动鼠标")
            webbrowser.open(url)

            logger.info("chrome threading over")

        elif self.name == "play":

            # # 先给线程加一个锁
            # threading.Lock().acquire()

            # 休眠一段时间，确保 chrome 完全加载完成
            time.sleep(10)

            # 模拟鼠标点击
            mouse_click(x, y)  # 点击开始播放图标 不同的人可能不太一样，我是根据我的屏幕浏览器全屏

            logger.info("已点击开始播放，请等待")
            logger.info(f"现在播放视频的 ID 是: {self.video_id}")

            # 获取sleep时间
            video_time = URL_AND_TIME[self.video_id]['time']
            sleep_time = int(video_time) * 60 + int(math.modf(video_time)[0] * 100)
            logger.info("sleep time = %f" % sleep_time)
            time.sleep(sleep_time + 8)  # 多看 8 秒钟，确保容错

            logger.success("视频播放完成")


def main(_x=230, _y=760, typing='edge', kill=None):
    """
    这是中国保密在线网站自动学习软件主程序
    你至少需要提供两个参数作为鼠标点击位置(即播放按钮的坐标)，
    在这之后还有一个参数作为浏览器的类型，暂时仅支持 Edge 浏览器和 Chrome 浏览器的自动开启和关闭
    其他的浏览器需要在参数末尾加上 `kill=浏览器进程名`
    浏览器进程名一般后面有 `.exe`

    :param _x: 播放按钮的 x 坐标
    :param _y: 播放按钮的 y 坐标
    :param typing: 浏览器类型，备选值为 'edge' 或 'chrome'
    :param kill: 浏览器进程名，当 typing 不是备选值时则必须提供
    """

    global x, y
    x, y = _x, _y

    need_jump = False

    for i in URL_AND_TIME:

        # for ignore in config.read('baomi.ignore_list'):
        #     if ignore == i['url'] or ignore == i:
        #         need_jump = True
        #         break
        if need_jump:
            logger.info(f"编号: {i}, url: {i['url']} 视频已跳过")
            need_jump = False
            continue

        url = URL_AND_TIME[i]['url']

        # 先确保chrome被关闭了
        if typing == 'edge':
            os.system("taskkill /f /im msedge.exe")
        elif typing == 'chrome':
            os.system("taskkill /f /im chrome.exe")
        else:
            if kill is None:
                print(f'【ERROR】无法识别参数 “{typing}”')
                return None
            else:
                os.system(f'taskkill /f /im {kill}')
        time.sleep(2.5)

        # 创建子线程
        thread1 = ChildThread(1, "chrome", url)
        thread2 = ChildThread(2, "play", url, video_id=i)

        # 开启线程
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    print("Exiting Main Thread")
    print("请检查所有的必修是否都学完再考试")
