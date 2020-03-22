from enum import IntEnum

from flask import current_app

from webapi.db import get_db


class Product(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute('SELECT * FROM product')
                data = cursor.fetchall()
            value = {
                'result': [
                    {
                        'id': row['id'],
                        'name': row['name'],
                        'price': row['price'],
                    }
                    for row in data
                ]
            }
        except Exception as e:
            current_app.logger.error('fetching all products: {0}'.format(e))
            return Result(
                code=Code.INTERNAL_SERVER_ERROR,
                description='Fetchting all products failed.'
            )

        return Result(value=value)

    def fetch(self, product_id):
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM product WHERE id = %s',
                    (product_id,),
                )
                row = cursor.fetchone()
            value = {}
            if row is not None:
                value = {
                    'result': {
                        'id': row['id'],
                        'name': row['name'],
                        'price': row['price'],
                    }
                }
        except Exception as e:
            current_app.logger.error('fetching product: {0}'.format(e))
            return Result(
                code=Code.INTERNAL_SERVER_ERROR,
                description='Fetchting a product failed.'
            )

        return Result(value=value)

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
            return Result(
                code=Code.INTERNAL_SERVER_ERROR,
                description='Creating a product failed.'
            )

        return Result(value={'result': 'Successfully Created.'})

    def update(self, product_id, name, price):
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'UPDATE product SET name = %s, price = %s WHERE id = %s',
                    (name, price, product_id),
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('updating product: {0}'.format(e))
            return Result(
                code=Code.INTERNAL_SERVER_ERROR,
                description='Updating a product failed.'
            )

        return Result(value={'result': 'Successfully Updated.'})

    def delete(self, product_id):
        result = Result()
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM product WHERE id = %s',
                    (product_id,),
                )
            db.commit()
        except Exception as e:
            db.rollback()
            current_app.logger.error('deleting product: {0}'.format(e))
            return Result(
                code=Code.INTERNAL_SERVER_ERROR,
                description='Deleting a product failed.'
            )

        return Result(value={'result': 'Successfully Updated.'})


class Code(IntEnum):
    OK = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500


class Result(object):
    def __init__(self, code=Code.OK, description='', value=None):
        self.code = code
        self.description = description
        if value is None:
            self.value = {}
        else:
            self.value = value
