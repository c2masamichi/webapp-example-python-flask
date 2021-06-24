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


def make_sorted_roles():
    """Fetch user.

    Returns:
        list: roles
    """
    role_priv_pairs = [(k, v) for k, v in ROLE_PRIV.items()]
    role_priv_pairs.sort(key=itemgetter(1))
    roles = [role for role, _ in role_priv_pairs]
    return roles
