from flask import current_app

from webapi.db import get_db


class Product(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        result = Result()
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute('SELECT * FROM product')
                data = cursor.fetchall()
            result.value = {
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
            result.code = 500
            result.description = 'Fetchting all products failed.'
        finally:
            return result

    def fetch(self, product_id):
        result = Result()
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM product WHERE id = %s',
                    (product_id,),
                )
                row = cursor.fetchone()
            if row is not None:
                result.value = {
                    'result': {
                        'id': row['id'],
                        'name': row['name'],
                        'price': row['price'],
                    }
                }
        except Exception as e:
            current_app.logger.error('fetching product: {0}'.format(e))
            result.code = 500
            result.description = 'Fetchting a product failed.'
        finally:
            return result

    def create(self, name, price):
        result = Result()
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
            result.code = 500
            result.description = 'Creating a product failed.'
        else:
            result.value = {'result': 'Successfully Created.'}
        finally:
            return result

    def update(self, product_id, name, price):
        result = Result()
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
            result.code = 500
            result.description = 'Updating a product failed.'
        else:
            result.value = {'result': 'Successfully Updated.'}
        finally:
            return result

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
            result.code = 500
            result.description = 'Deleting a product failed.'
        else:
            result.value = {'result': 'Successfully Deleted.'}
        finally:
            return result


class Result(object):
    def __init__(self, code=200, description='', value=None):
        self.code = code
        self.description = description
        if value is None:
            self.value = {}
        else:
            self.value = value
