import os
from typing import Any

import yaml

from . import constants
from ..utils import logger

try:
    with open(constants.CONFIG_FILE_PATH, encoding="utf-8") as f:
        config = yaml.safe_load(f)
except OSError:
    logger.error("配置文件读取失败, 准备生成默认配置文件")
    with open(constants.CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(constants.DEFAULT_CONFIG)
    config = constants.DEFAULT_CONFIG.copy()


def read(config_root: str) -> Any:
    """
    读取配置文件
    :param config_root: 请输入以点分割的配置路径
    :return: 返回这个配置的值
    """
    def recursive(root_list, relative_config):
        if len(root_list) == 1:
            return relative_config[root_list[0]]
        else:
            return recursive(root_list[1:], relative_config[root_list[0]])

    return recursive(config_root.split('.'), config)


def save():
    with open(constants.CONFIG_FILE_PATH, 'w', encoding='utf-8') as config_file:
        yaml.safe_dump(config, config_file)


def update(config_root: str, value: Any) -> dict[str: Any]:
    """
    更新配置文件
    :param config_root: 请输入以点分割的配置路径
    :param value: 更新后的值
    :return: 返回一个字典，使用 update(root, value)[root] 获取更新后的值, update(root, value)['old'] 获取更新后的值
    """

    def recursive(root_list, relative_config, new_value):
        if len(root_list) == 1:
            old_value = relative_config[root_list[0]]
            relative_config[root_list[0]] = new_value
            return old_value
        else:
            return recursive(root_list[1:], relative_config[root_list[0]], new_value)

    return {
        f"{config_root}": value,
        'old': recursive(config_root.split('.'), config, value)
    }


def get(config_root: str, default=None) -> Any:
    """
    获取配置文件
    :param config_root: 请输入以点分割的配置路径
    :param default: 如果配置文件中没有对应的值，则返回 default
    :return: 返回配置文件中对应的值。若不存在，则返回 default
    """
    try:
        return read(config_root)
    except KeyError:
        return default


def setdefault(config_root: str, default: Any) -> dict[str: Any]:
    """
    设置默认值
    :param config_root: 请输入以点分割的配置路径
    :param default: 设置的默认值
    :return: 返回配置文件的值。若不存在，则返回 default，并且将其值设置为 default
    """

    def recursive(root_list, relative_config, default_value):
        if len(root_list) == 1:
            try:
                return relative_config[root_list[0]]
            except KeyError:
                logger.warning('配置文件中不存在该配置项，已设置默认值')
                relative_config[root_list[0]] = default_value
                return default_value
        else:
            try:
                return recursive(root_list[1:], relative_config[root_list[0]], default_value)
            except KeyError:
                logger.warning(f'配置文件的 {relative_config} 不存在 {root_list[0]} , 已设为空字典')
                relative_config[root_list[0]] = {}
                return recursive(root_list[1:], relative_config[root_list[0]], default_value)

    return recursive(
        os.path.join(*config_root.split('.')).split('\\'),
        config, default
    )


def add(root, key, value, mode=None):
    """
    添加配置
    :param root: 一个以小数点分割的配置路径
    :param key: 在路径下的键
    :param value: 对应的值
    :param mode: 添加模式，默认为 None, 例如输入 'append' 将会调用 .append() 命令
    """

    def recursive(root_list, relative_config):
        if not root_list:
            if mode is None:
                relative_config[key] = value
            else:
                try:
                    constants.MODE_MAP[mode](relative_config, __object=value)
                except ValueError:
                    constants.MODE_MAP[mode](relative_config, key, __object=value)
                except KeyError:
                    logger.error(f'不存在模式: {mode}')
                    logger.debug('使用赋值模式')
                    relative_config[key] = value
        else:
            recursive(root_list[1:], relative_config[root_list[0]])

    recursive(root.split('.'), config)
    return f'{root}.{key}', value
