class Entry(object):
    def __init__(self, db):
        self._db = db

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
