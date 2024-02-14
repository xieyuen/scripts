import json
from pathlib import Path

import yaml


class TYPES:
    json = 'json'
    yaml = 'yaml'


DEFAULT_ENCODING = 'utf8'

write_methods = {
    TYPES.json: (lambda data, f, **kwargs: json.dump(data, f)),
    TYPES.yaml: (lambda data, f, **kwargs: yaml.dump(data, f, **kwargs)),
}
read_methods = {
    TYPES.json: (lambda f, **kwargs: json.load(f, **kwargs)),
    TYPES.yaml: (lambda f, **kwargs: yaml.safe_load(f)),
}


class ConfigurationManager:
    def __init__(self, path='config.json', file_type=TYPES.json, *, default):
        self._path = Path(path)
        self._default = default
        self._type = file_type
        if not self._path.exists():
            self.create_default()
        self.load()

    def load(self, encoding=DEFAULT_ENCODING):
        with self._path.open(encoding=encoding) as f:
            data = read_methods[self._type](f)
        return data

    def save(self, data, encoding=DEFAULT_ENCODING):
        with self._path.open('w', encoding=encoding) as f:
            write_methods[self._type](data, f, allow_unicode=True)

    def create_default(self, encoding=DEFAULT_ENCODING):
        self.save(self._default, encoding=encoding)
