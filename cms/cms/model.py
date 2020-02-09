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
        user = None
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT id, username FROM user WHERE id = %s',
                (user_id,),
            )
            user = cursor.fetchone()

        return user

    def auth(self, username, password):
        db = self._db
        error = None
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT id, username, password FROM user WHERE username = %s',
                (username,)
            )
            user = cursor.fetchone()

        if (user is None or
                not check_password_hash(user['password'], password)):
            error = 'Incorrect username or password.'
            user = None

        return user, error

    def create(self, username, password):
        db = self._db
        result = Result()

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
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT id, password FROM user WHERE id = %s',
                (user_id,)
            )
            user = cursor.fetchone()

        error = None
        if (user is None or
                not check_password_hash(user['password'], old_password)):
            error = 'Incorrect password.'
        else:
            with db.cursor() as cursor:
                cursor.execute(
                    'UPDATE user SET password = %s WHERE id = %s',
                    (generate_password_hash(new_password), user_id),
                )
            db.commit()

        return error


class Result(object):
    def __init__(self, succeeded=True, description='', value=None):
        self.succeeded = succeeded
        self.description = description
        self.value = value
