import json
from configparser import ConfigParser
from typing import overload, Dict, Optional, Any

import yaml

from scripts.utils.logger import logger

__all__ = ["ConfigurationManager"]


class Constant:
    class TYPE_MAP:
        def __init__(self):
            self.__MAP = {
                "json": "json",
                "yaml": "yaml",
                "yml": "yaml",
                "ini": "ini",
                None: None,
            }

        def __getitem__(self, key):
            try:
                return self.__MAP[key]
            except KeyError:
                raise ValueError(f"Unsupported file type: {key}")

    TYPE_MAP = TYPE_MAP()


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def save_yaml(file_path, data):
    with open(file_path, "w") as f:
        yaml.dump(data, f)


def load_ini(file_path) -> Dict:
    cfg = ConfigParser()
    cfg.read(file_path)
    return {section: dict(cfg[section]) for section in cfg.sections()}


def save_ini(file_path, data: Dict[str, Any]):
    cfg = ConfigParser()
    for section, options in data.items():
        cfg.add_section(section)
        cfg[section] = options

    with open(file_path, "w") as f:
        cfg.write(f)


class ConfigurationManager:
    @overload
    def __init__(self,
                 file_path: Optional[str] = ...,
                 *,
                 default: Dict):
        ...

    def __init__(self, file_path=None, *, default):
        self.__type = Constant.TYPE_MAP[file_path.split(".")[-1] if file_path else None]
        self.config = {}
        self.__default = default
        if file_path:
            self.__path = file_path
            self.load_config()

    def load_config(self, file_path=None):
        if not self.__path and not file_path:
            raise ValueError("未指定配置文件路径")
        elif self.__path:
            file_path = self.__path
        try:
            if self.__type == "json":
                load_json(file_path)
            elif self.__type == "yaml":
                load_yaml(file_path)
            elif self.__type == "ini":
                load_ini(file_path)
            else:
                assert False, "你是如何使代码运行到这的？"
        except FileNotFoundError:
            logger.error("未找到配置文件, 正在使用默认配置")
            logger.info("默认配置正在创建...")
            self.create_default()

    def save_config(self):
        if self.__type == "json":
            save_json(self.__path, self.config)
        elif self.__type == "yaml":
            save_yaml(self.__path, self.config)
        elif self.__type == "ini":
            save_ini(self.__path, self.config)
        else:
            assert False, "你是如何使代码运行到这的？"

    def create_default(self):

        self.config = self.__default.copy()
        self.save_config()
