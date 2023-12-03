import json
from configparser import ConfigParser
from pathlib import Path
from typing import TextIO, Optional, Callable, Any

import yaml

from scripts.utils.jsobj import JSObject


class FileReader:
    __consts = JSObject(
        DEFAULT_CODING='utf-8',
        TYPE_MAP=JSObject(
            none='text', null='text', undefined='text', text='text', txt='text',
            yaml='yaml', yml='yaml',
            json='json',
            ini='ini'
        )
    )
    TYPES = __consts.TYPE_MAP

    def __init__(self, path: str, file_type: str = 'none'):
        self.__file = Path(path)
        self.__file_io = None
        self.__file_name = self.__file.name
        self.__file_type = self.TYPES[file_type.lower()]

    def change_file_type(self, value: str):
        self.__file_type = self.TYPES[value.lower()]

    def read(
            self,
            reader: Optional[Callable] = None,
            *,
            encoding='utf-8',
            load_to_pyobj_first=False
    ) -> Any:
        """
        读取文件, 若传入 reader 则会将文件流传给 reader 并返回 reader 的返回
        若生成实例时未传入 file_type, 则返回包含文件内容的字符串


        :param reader: Optional[Callable]          | 内容处理
        :param encoding: str ='utf-8'              | 编码
        :param load_to_pyobj_first: bool = False   | 是否先将文件内容转换为 python 对象再传给 reader
        :return: Union[str, Any]
        """
        with self.__file.open(encoding=encoding) as f:
            if reader is not None:
                if load_to_pyobj_first:
                    return reader(self.__read(f, self.__file_type))
                return reader(f)
            return self.__read(f, self.__file_type)

    def __read(self, file_io: TextIO, file_type: str) -> Any:
        match file_type:
            case FileReader.TYPES.text:
                return file_io.read()

            case FileReader.TYPES.yaml:
                data = dict()
                for d in yaml.safe_load_all(file_io):
                    data.update(d)
                return data

            case FileReader.TYPES.json:
                return json.load(file_io)

            case FileReader.TYPES.ini:
                config = ConfigParser()
                config.read(self.__file.name)
                return config

    def open(self):
        self.__file_io = self.__file.open()
        return self.__file_io

    def close(self):
        self.__file_io.close()
