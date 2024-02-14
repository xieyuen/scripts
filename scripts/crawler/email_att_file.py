"""
未完成
邮件附件批量下载
"""

raise NotImplementedError

from typing import Literal

import yaml


class DateRange:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date


class Configurations:
    def __init__(self, conf_file_path, encoding):
        with open(conf_file_path, encoding=encoding) as config_file:
            self.__config_data = yaml.safe_load(config_file)
        self.__start_date = self.__config_data.get('start_date')
        self.__end_date = self.__config_data.get('end_date')

    @property
    def host(self):
        return self.__config_data['host']

    @property
    def username(self):
        return self.__config_data['username']

    @property
    def permission_code(self):
        return self.__config_data.get('permission_code') or self.__config_data.get('password')

    def get_date_range(self) -> DateRange:
        def _input(msg: Literal['开始', '结束']) -> str:
            return input(f"请输入{msg}时间(使用“YYYYMMDD”格式,例如20000101)\n>>> ")

        if not self.__start_date:
            self.__start_date = _input('开始')
        if not self.__end_date:
            self.__end_date = _input('结束')

        return DateRange(self.__start_date, self.__end_date)

    @staticmethod
    def createDefaultConfigFile():
        pass
