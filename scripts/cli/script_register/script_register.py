import importlib
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.cli.main import ScriptConsole
    from scripts.utils.logger import ConsoleLogger


class Register:
    def __init__(self, logger: "ConsoleLogger", registry_name):
        self._dict = {}
        self._name = registry_name
        self._logger = logger

    def __setitem__(self, key, value):
        if not callable(value):
            raise Exception(f"Value of a Registry must be a callable!\nValue: {value}")
        if key is None:
            key = value.__name__
        if key in self._dict:
            self._logger.warning("Key %s already in registry %s." % (key, self._name))
        self._dict[key] = value

    def register(self, target):
        """Decorator to register a function or class."""

        def add(key, value):
            self[key] = value
            return value

        if callable(target):
            # @reg.register
            return add(None, target)
        # @reg.register('alias')
        return lambda x: add(target, x)

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def keys(self):
        """key"""
        return self._dict.keys()


class ScriptRegister:
    def __init__(self, script_console: "ScriptConsole"):
        self._console = script_console
        self._logger = script_console.logger
        self._scripts = {}
        self._modules = Register(self._logger, 'modules')
        reg_mods = ["models"]
        self.all_mods = [("models", reg_mods)]

    def import_all_modules(self, custom_module_paths=None):
        """Import all modules for register."""
        modules = []
        for base_dir, _modules in self.all_mods:
            for name in _modules:
                full_name = base_dir + "." + name
                modules.append(full_name)
        if isinstance(custom_module_paths, list):
            modules += custom_module_paths
        for module in modules:
            try:
                importlib.import_module(module)
            except ImportError as error:
                self._logger.error("Module {} import failed: {}".format(module, error))
                self._logger.exception(error)
