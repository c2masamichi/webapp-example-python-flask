import re

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from cms.db import get_db


class Entry(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        result = Result()
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT title, body, created FROM entry'
                    ' ORDER BY created DESC'
                )
                result.value = cursor.fetchall()
        except Exception as e:
            current_app.logger.error('fetching entries: {0}'.format(e))
            result.succeeded = False
        return result

    def fetch(self, entry_id):
        result = Result()
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id, title, body, created FROM entry WHERE id = %s',
                    (entry_id,),
                )
                result.value = cursor.fetchone()
        except Exception as e:
            current_app.logger.error('fetching an entry: {0}'.format(e))
            result.succeeded = False
        return result

    def create(self, title, body):
        result = Result()
        if not self._validate_data(title, body):
            result.succeeded = False
            result.description = 'Bad data.'
            return result

        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO entry (title, body) VALUES (%s, %s)',
                    (title, body),
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('creating an entry: {0}'.format(e))
            result.succeeded = False
            result.description = 'Creation failed.'
        return result

    def update(self, entry_id, title, body):
        result = Result()
        if not self._validate_data(title, body):
            result.succeeded = False
            result.description = 'Bad data.'
            return result

        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'UPDATE entry SET title = %s, body = %s WHERE id = %s',
                    (title, body, entry_id),
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('updating an entry: {0}'.format(e))
            result.succeeded = False
            result.description = 'Update failed.'
        else:
            result.description = 'Update succeeded.'
        return result

    def delete(self, entry_id):
        result = Result()
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM entry WHERE id = %s',
                    (entry_id,),
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('deleting an entry: {0}'.format(e))
            result.succeeded = False
            result.description = 'Deletion failed.'
        return result

    def _validate_data(self, title, body):
        title_max = 100
        body_max = 10000
        return len(title) <= title_max and len(body) <= body_max


class User(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        result = Result()
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id, username FROM user'
                    ' ORDER BY username'
                )
                result.value = cursor.fetchall()
        except Exception as e:
            current_app.logger.error('fetching users: {0}'.format(e))
            result.succeeded = False
        return result

    def fetch(self, user_id):
        result = Result()
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id, username, password FROM user WHERE id = %s',
                    (user_id,),
                )
                result.value = cursor.fetchone()
        except Exception as e:
            current_app.logger.error('fetching a user: {0}'.format(e))
            result.succeeded = False
        return result

    def auth(self, username, password):
        db = self._db
        result = Result()

        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id, username, password FROM user WHERE username = %s',
                    (username,)
                )
                user = cursor.fetchone()
        except Exception as e:
            current_app.logger.error('fetching a user: {0}'.format(e))
            result.succeeded = False
            result.description = 'Authentication failed.'
            return result

        if (user is None or
                not check_password_hash(user['password'], password)):
            result.succeeded = False
            result.description = 'Incorrect username or password.'
            user = None

        result.value = user
        return result

    def create(self, username, password):
        result = Result()
        if not self._validate_data(username, password):
            result.succeeded = False
            result.description = 'Bad data.'
            return result

        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT id FROM user WHERE username = %s',
                    (username,)
                )
                user = cursor.fetchone()
            if user is not None:
                result.description = 'User {0} is already registered.'.format(username)
                result.succeeded = False
        except Exception as e:
            current_app.logger.error('fetching a user: {0}'.format(e))
            result.succeeded = False
            result.description = 'Creation failed.'

        if result.succeeded:
            try:
                with db.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO user (username, password) VALUES (%s, %s)',
                        (username, generate_password_hash(password)),
                    )
                db.commit()
            except Exception as e:
                db.rollback()
                current_app.logger.error('creating a user: {0}'.format(e))
                result.succeeded = False
                result.description = 'Creation failed.'

        return result

    def delete(self, user_id):
        db = self._db
        result = Result()
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM user WHERE id = %s',
                    (user_id,),
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('deleting a user: {0}'.format(e))
            result.succeeded = False
            result.description = 'Deletion failed.'
        return result

    def change_password(self, user_id, old_password, new_password):
        result = Result()
        if not self._validate_data(password=new_password):
            result.succeeded = False
            result.description = 'Bad data.'
            return result

        db = self._db
        fetch_user_result = self.fetch(user_id)
        if not fetch_user_result.succeeded:
            result.succeeded = False
            result.description = 'Update failed.'
            return result

        user = fetch_user_result.value
        if (user is None or
                not check_password_hash(user['password'], old_password)):
            result.succeeded = False
            result.description = 'Incorrect password.'
            return result

        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'UPDATE user SET password = %s WHERE id = %s',
                    (generate_password_hash(new_password), user_id),
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('updating a password: {0}'.format(e))
            result.succeeded = False
            result.description = 'Update failed.'
        else:
            result.description = 'Password Changed.'

        return result

    def _validate_data(self, username='', password=''):
        username_max = 20
        password_max = 30
        if len(username) > username_max:
            return False
        if len(password) > password_max:
            return False

        username_patten = r'[0-9a-zA-Z-_]*'
        if re.fullmatch(username_patten, username) is None:
            return False
        password_pattern = r'[0-9a-zA-Z-_]*'
        if re.fullmatch(password_pattern, password) is None:
            return False
        return True


class Result(object):
    def __init__(self, succeeded=True, description='', value=None):
        self.succeeded = succeeded
        self.description = description
        self.value = value
