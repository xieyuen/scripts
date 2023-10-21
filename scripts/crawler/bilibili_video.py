import os
from typing import Optional

import requests

from scripts.constants import crawler as constants


class Main:
    def __init__(self, sys_argv):
        self.args = {
            key: value
            for item in sys_argv[1:]
            for key, value in item.split('=')
        }
        self.url = self.args.get('url')  # type: Optional[str]
        self.path = self.args.get('path', constants.DEFAULT_SAVE_PATH)  # type: str
        if self.url is None:
            pass

    class Enables:
        enable_cli: bool

    def write(self, data: bytes, name):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        with open(f'{self.path}/{name}', 'wb') as f:
            f.write(data)

    def __main(self, url: str):
        response = requests.get(
            url=url,
            headers=constants.BILIBILI_HEADERS
        )
        json_data = response.json()
        dash = json_data['data']['dash']
        audio_url = dash['audio']['baseUrl']
        video_url = dash['video']['baseUrl']
        audio_con = requests.get(url=audio_url, headers=constants.BILIBILI_HEADERS).content
        video_con = requests.get(url=video_url, headers=constants.BILIBILI_HEADERS).content

        self.write(audio_con, name='audio.mp3')
        self.write(video_con, name='video.mp4')

    def run(self):
        pass


if __name__ == '__main__':
    Main(__import__('sys').argv).run()
