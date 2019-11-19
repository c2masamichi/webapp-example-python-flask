from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from cms.db import get_db


class Entry(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT title, body, created FROM post'
                ' ORDER BY created DESC'
            )
            return cursor.fetchall()

    def fetch(self, entry_id):
        entry = None
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT id, title, body, created FROM post WHERE id = %s',
                (entry_id,),
            )
            entry = cursor.fetchone()

        return entry

    def create(self, title, body):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'INSERT INTO post (title, body) VALUES (%s, %s)',
                (title, body),
            )
        db.commit()

    def update(self, entry_id, title, body):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'UPDATE post SET title = %s, body = %s WHERE id = %s',
                (title, body, entry_id),
            )
        db.commit()

    def delete(self, entry_id):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'DELETE FROM post WHERE id = %s',
                (entry_id,),
            )
        db.commit()


class User(object):
    def __init__(self):
        self._db = get_db()

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
                'SELECT * FROM user WHERE username = %s', (username,)
            )
            user = cursor.fetchone()

        if (user is None or 
            not check_password_hash(user['password'], password)):
            error = 'Incorrect username or password.'

        return user, error

    def create(self, username, password):
        db = self._db
        error = None

        with db.cursor() as cursor:
            cursor.execute(
                'SELECT id FROM user WHERE username = %s',
                (username,)
            )
            user = cursor.fetchone()
        if user is not None:
            error = 'User {0} is already registered.'.format(username)

        if error is None:
            with db.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO user (username, password) VALUES (%s, %s)',
                    (username, generate_password_hash(password)),
                )
            db.commit()

        return error

    def delete(self, user_id):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'DELETE FROM user WHERE id = %s',
                (user_id,),
            )
        db.commit()
