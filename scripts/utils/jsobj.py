class JSObject(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return self[item]

    def __setattr__(self, key, value):
        try:
            setattr(self, key, value)
        finally:
            dict.__setitem__(self, key, value)


def main():
    obj = JSObject({1: 1, 2: 2, 3: 3}, a=1, b=2, c=3)
    print(
        obj.a,
        obj.b,
        obj['c'],
        obj[1],
        obj[2],
        obj[3],
    )


if __name__ == '__main__':
    main()
