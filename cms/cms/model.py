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

