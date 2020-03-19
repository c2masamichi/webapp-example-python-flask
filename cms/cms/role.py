from enum import IntEnum


class Privilege(IntEnum):
    ADMINISTRATOR = 1000
    EDITOR = 100
    AUTHOR = 10


ROLE_PRIV = {
    'administrator': Privilege.ADMINISTRATOR,
    'editor': Privilege.EDITOR,
    'author': Privilege.AUTHOR,
}
