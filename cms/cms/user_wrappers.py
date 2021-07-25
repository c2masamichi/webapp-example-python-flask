import re

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from cms.database import db
from cms.models import User


def auth_user(name, password):
    """Auth user.

    Args:
        name (str): user's name
        password (str): user's password

    Returns:
        User: Authenticated user
    """

    user = User.query.filter_by(name=name).first()
    if (user is None or
            not check_password_hash(user.password, password)):
        return None
    return user


def change_password(
        user_id, new_password, old_password=None, old_required=True):
    """Change password.

    Args:
        user_id (int): id of user to change
        new_password (str): password after change
        old_password (str): current password
        old_required (bool): True if current password must be checked

    Returns:
        succeeded (bool): True if password successfully changed
        message (str): description of result
    """
    default_err_msg = 'Incorrect password.'
    if old_required and old_password is None:
        return False, default_err_msg

    if not validate_password(new_password):
        return False, 'Bad data.'

    user = User.query.get(user_id)
    if user is None:
        return False, 'Update failed.'

    if (old_required and
            not check_password_hash(user.password, old_password)):
        return False, default_err_msg

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return True, 'Password Changed.'


def validate_password(password):
    """Validate password for creation or update.

    Args:
        password(str): user's password

    Returns:
        bool: True if password is ok
    """
    max_length = 30
    if len(password) > max_length:
        return False
    pattern = r'[0-9a-zA-Z-_]*'
    if re.fullmatch(pattern, password) is None:
        return False
    return True