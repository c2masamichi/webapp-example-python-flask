from flask import current_app

from webapi.db import get_db


class Product(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM product')
            data = cursor.fetchall()

        return {
            'result': [
                {
                    'id': row['id'],
                    'name': row['name'],
                    'price': row['price'],
                }
                for row in data
            ]
        }

    def fetch(self, product_id):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM product WHERE id = %s',
                (product_id,),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return {
            'result': {
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
            }
        }

    def create(self, name, price):
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO product (name, price) VALUES (%s, %s)',
                    (name, price),
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('creating product: {0}'.format(e))
            return {
                'error': 'Failed.'
            }
        else:
            return {
                'result': 'Successfully Created.'
            }

    def update(self, product_id, name, price):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'UPDATE product SET name = %s, price = %s WHERE id = %s',
                (name, price, product_id),
            )
        db.commit()

        return {
            'result': 'Successfully Updated.'
        }

    def delete(self, product_id):
        db = self._db
        with db.cursor() as cursor:
            cursor.execute(
                'DELETE FROM product WHERE id = %s',
                (product_id,),
            )
        db.commit()

        return {
            'result': 'Successfully Deleted.'
        }
