class JSObject(dict):
    def __init__(self, *args, **kwargs):
        if all(isinstance(arg, JSObject) for arg in args):
            for arg in args:
                self.__dict__.update(arg)
            super().__init__(**kwargs)
            self.__dict__.update(self)
            return

        super().__init__(*args, **kwargs)
        self.__dict__.update(self)

    def __setitem__(self, key, value, *, from_setattr=False):
        if isinstance(key, str) and not from_setattr:
            self.__setattr__(key, value, from_setitem=True)
        super().__setitem__(key, value)

    def __setattr__(self, key, value, *, from_setitem=False):
        super().__setattr__(key, value)
        if not from_setitem:
            self.__setitem__(key, value, from_setattr=True)

    def __delitem__(self, key, *, from_delattr=False):
        super().__delitem__(key)
        if not from_delattr:
            self.__delattr__(key, from_delitem=True)

    def __delattr__(self, item, *, from_delitem=False):
        super().__delattr__(item)
        if not from_delitem:
            self.__delitem__(item, from_delattr=True)

    def __repr__(self):
        return f"JSObject({super().__repr__()})"

    def copy(self):
        return JSObject(**self)
