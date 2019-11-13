class Entry(object):
    def __init__(self, db):
        self._db = db

    def fetch_all_entries(self):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT title, body, created FROM post'
                ' ORDER BY created DESC'
            )
            return cursor.fetchall()
