from operator import itemgetter
import re

from flask import current_app
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from cms.db import get_db
from cms.role import ROLE_PRIV


class Entry(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        """Fetch entries

        Returns:
            Result: entries info
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT e.id, title, created, author_id, username'
                    ' FROM entry e LEFT JOIN user u ON e.author_id = u.id'
                    ' ORDER BY created DESC'
                )
                entries = cursor.fetchall()
        except Exception as e:
            current_app.logger.error('fetching entries: {0}'.format(e))
            return Result(succeeded=False)

        for entry in entries:
            if entry['author_id'] is None:
                entry['author_id'] = -1
                entry['username'] = 'deleted-user'

        return Result(value=entries)

    def fetch(self, entry_id):
        """Fetch entry

        Args:
            entry_id (int): id of entry to fetch

        Returns:
            Result: entry info
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id, title, body, created, author_id'
                    ' FROM entry WHERE id = %s',
                    (entry_id,)
                )
                entry = cursor.fetchone()
        except Exception as e:
            current_app.logger.error('fetching an entry: {0}'.format(e))
            return Result(succeeded=False)

        return Result(value=entry)

    def create(self, author_id, title, body):
        """Create entry

        Args:
            author_id (int): author's id
            title (str): title of entry
            body (str): body of entry

        Returns:
            Result: Success or failure of creation
        """
        if not self._validate_data(title, body):
            return Result(succeeded=False, description='Bad data.')

        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO entry (author_id, title, body)'
                    ' VALUES (%s, %s, %s)',
                    (author_id, title, body)
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('creating an entry: {0}'.format(e))
            return Result(succeeded=False, description='Creation failed.')

        return Result(description='Creation succeeded.')

    def update(self, entry_id, title, body):
        """Update entry

        Args:
            entry_id (int): id of entry to update
            title (str): title of entry
            body (str): body of entry

        Returns:
            Result: Success or failure of update
        """
        if not self._validate_data(title, body):
            return Result(succeeded=False, description='Bad data.')

        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'UPDATE entry SET title = %s, body = %s WHERE id = %s',
                    (title, body, entry_id)
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('updating an entry: {0}'.format(e))
            return Result(succeeded=False, description='Update failed.')

        return Result(description='Update succeeded.')

    def delete(self, entry_id):
        """Delete entry

        Args:
            entry_id (int): id of entry to delete

        Returns:
            Result: Success or failure of delete
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM entry WHERE id = %s',
                    (entry_id,)
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('deleting an entry: {0}'.format(e))
            return Result(succeeded=False, description='Deletion failed.')

        return Result(description='Deletion succeeded.')

    def _validate_data(self, title, body):
        """Validate input data for creation or update

        Args:
            title (str): title of entry
            body (str): body of entry

        Returns:
            bool: True if data is ok
        """
        title_max = 100
        body_max = 10000
        return len(title) <= title_max and len(body) <= body_max


class User(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        """Fetch users

        Returns:
            Result: users info
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id, role, username FROM user'
                    ' ORDER BY username'
                )
                users = cursor.fetchall()
        except Exception as e:
            current_app.logger.error('fetching users: {0}'.format(e))
            return Result(succeeded=False)

        return Result(value=users)

    def fetch(self, user_id):
        """Fetch user

        Args:
            user_id (int): id of user to fetch

        Returns:
            Result: user info
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id, role, username, password'
                    ' FROM user WHERE id = %s',
                    (user_id,)
                )
                user = cursor.fetchone()
        except Exception as e:
            current_app.logger.error('fetching a user: {0}'.format(e))
            return Result(succeeded=False)

        return Result(value=user)

    def auth(self, username, password):
        """Auth user

        Args:
            username (str): user's name
            password (str): user's password

        Returns:
            Result: user info
        """
        fetch_user_result = self._fetch_by_username(username)
        if not fetch_user_result.succeeded:
            return Result(
                succeeded=False,
                description='Authentication failed.'
            )

        user = fetch_user_result.value
        if (user is None or
                not check_password_hash(user['password'], password)):
            return Result(
                succeeded=False,
                description='Incorrect username or password.'
            )

        return Result(value=user)

    def create(self, role, username, password):
        """Create user

        Args:
            role (str): user's role
            username (str): user's name
            password (str): user's password

        Returns:
            Result: Success or failure of creation
        """
        if role not in ROLE_PRIV:
            return Result(
                succeeded=False,
                description='Role {0} does not exist.'.format(role)
            )

        if (not self._validate_username(username)
                or not self._validate_password(password)):
            return Result(succeeded=False, description='Bad data.')

        fetch_user_result = self._fetch_by_username(username)
        if not fetch_user_result.succeeded:
            return Result(succeeded=False, description='Creation failed.')

        if fetch_user_result.value is not None:
            return Result(
                succeeded=False,
                description='User {0} is already registered.'.format(username)
            )

        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO user (role, username, password)'
                    ' VALUES (%s, %s, %s)',
                    (role, username, generate_password_hash(password))
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('creating a user: {0}'.format(e))
            return Result(succeeded=False, description='Creation failed.')

        return Result(description='Creation succeeded.')

    def update(self, user_id, role, username):
        """Update user

        Args:
            user_id (int): id of user to update
            role (str): user's role
            username (str): user's name

        Returns:
            Result: Success or failure of update
        """
        if role not in ROLE_PRIV:
            return Result(
                succeeded=False,
                description='Role {0} does not exist.'.format(role)
            )

        if not self._validate_username(username):
            return Result(succeeded=False, description='Bad data.')

        fetch_user_result = self._fetch_by_username(username)
        if not fetch_user_result.succeeded:
            return Result(succeeded=False, description='Update failed.')

        if fetch_user_result.value is not None:
            return Result(
                succeeded=False,
                description='User {0} is already registered.'.format(username)
            )

        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'UPDATE user SET role = %s, username = %s'
                    ' WHERE id = %s',
                    (role, username, user_id)
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('updating a user: {0}'.format(e))
            return Result(succeeded=False, description='Update failed.')

        return Result(description='Update succeeded.')

    def delete(self, user_id):
        """Delete user

        Args:
            user_id (int): id of user to delete

        Returns:
            Result: Success or failure of delete
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM user WHERE id = %s',
                    (user_id,)
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('deleting a user: {0}'.format(e))
            return Result(succeeded=False, description='Deletion failed.')

        return Result(description='Deletion succeeded.')

    def change_password(
            self, user_id, new_password,
            old_password=None, old_required=True):
        default_err_msg = 'Incorrect password.'
        if old_required and old_password is None:
            return Result(succeeded=False, description=default_err_msg)

        if not self._validate_password(new_password):
            return Result(succeeded=False, description='Bad data.')

        fetch_user_result = self.fetch(user_id)
        user = fetch_user_result.value
        if not fetch_user_result.succeeded or user is None:
            return Result(succeeded=False, description='Update failed.')

        if (old_required and
                not check_password_hash(user['password'], old_password)):
            return Result(succeeded=False, description=default_err_msg)

        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'UPDATE user SET password = %s WHERE id = %s',
                    (generate_password_hash(new_password), user_id)
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('updating a password: {0}'.format(e))
            return Result(succeeded=False, description='Update failed.')

        return Result(description='Password Changed.')

    def _validate_username(self, username):
        """Validate username for creation or update

        Args:
            username (str): user's name

        Returns:
            bool: True if username is ok
        """
        max_length = 20
        if len(username) > max_length:
            return False
        pattern = r'[0-9a-zA-Z-_]*'
        if re.fullmatch(pattern, username) is None:
            return False
        return True

    def _validate_password(self, password):
        """Validate password for creation or update

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

    def _fetch_by_username(self, username):
        """Fetch user by name

        Args:
            username (str): name of user to fetch

        Returns:
            Result: user info
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id, role, username, password'
                    ' FROM user WHERE username = %s',
                    (username,)
                )
                user = cursor.fetchone()
        except Exception as e:
            current_app.logger.error('fetching a user: {0}'.format(e))
            return Result(succeeded=False)

        return Result(value=user)


class Result(object):
    def __init__(self, succeeded=True, description='', value=None):
        self.succeeded = succeeded
        self.description = description
        self.value = value


def make_sorted_roles():
        """Fetch user

        Returns:
            list: roles
        """
    role_priv_pairs = [(k, v) for k, v in ROLE_PRIV.items()]
    role_priv_pairs.sort(key=itemgetter(1))
    roles = [role for role, _ in role_priv_pairs]
    return roles
