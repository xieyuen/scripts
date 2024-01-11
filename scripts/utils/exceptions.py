class MusicNotFoundError(Exception):
    pass


class UnknownErrors(Exception):
    pass


class UnknownError(UnknownErrors):
    pass


class PathNotExistsError(UnknownErrors):
    pass


UnknownPathError = PathNotExistsError
