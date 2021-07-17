from werkzeug.security import check_password_hash

from cms.models import User


def auth_user(name, password):
    """Auth user.
    Args:
        name (str): user's name
        password (str): user's password
    Returns:
        user: User instance
    """

    user = User.query.filter_by(name=name).first()
    if (user is None or
            not check_password_hash(user.password, password)):
        return None
    return user