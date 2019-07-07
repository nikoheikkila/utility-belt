__REPO__ = "https://github.com/nikoheikkila/utility-belt"
__VERSION__ = (0, 3, 0)


def get_version() -> str:
    return ".".join(map(str, __VERSION__))


def get_repo() -> str:
    return __REPO__


if __name__ == "__main__":
    raise NotImplementedError("Do not execute me.")
