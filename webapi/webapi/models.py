from enum import IntEnum
import re

from flask import current_app

from webapi.db import get_db


class Product(object):
    def __init__(self):
        self._db = get_db()

    def fetch_all(self):
        """Fetch products.

        Returns:
            Result: products info
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute('SELECT * FROM product')
                products = cursor.fetchall()
        except Exception as e:
            current_app.logger.error('fetching all products: {0}'.format(e))
            return Result(
                code=Code.INTERNAL_SERVER_ERROR,
                description='Fetchting all products failed.'
            )

        return Result(value=products)

    def fetch(self, product_id):
        """Fetch product.

        Args:
            product_id (int): id of product to fetch

        Returns:
            Result: product info
        """
        db = self._db
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM product WHERE id = %s',
                    (product_id,),
                )
                product = cursor.fetchone()
            if product_id is None:
                product = {}
        except Exception as e:
            current_app.logger.error('fetching product: {0}'.format(e))
            return Result(
                code=Code.INTERNAL_SERVER_ERROR,
                description='Fetchting a product failed.'
            )

        return Result(value=product)

    def create(self, name, price):
        """Create product.

        Args:
            name (str): name of product
            price (int): price of product

        Returns:
            Result: Success or failure of creation
        """
        if not self._validate_data(name, price):
            return Result(
                code=Code.BAD_REQUEST,
                description='Bad data.'
            )

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

        return Result()

    def update(self, product_id, name, price):
        """Update product.

        Args:
            product_id (int): id of product to update
            name (str): name of product
            price (int): price of product

        Returns:
            Result: Success or failure of update
        """
        if not self._validate_data(name, price):
            return Result(
                code=Code.BAD_REQUEST,
                description='Bad data.'
            )

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

        return Result()

    def delete(self, product_id):
        """Delete product.

        Args:
            product_id (int): id of product to delete

        Returns:
            Result: Success or failure of delete
        """
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

        return Result()

    def _validate_data(self, name, price):
        """Validate input data for creation or update.

        Args:
            name (str): name of product
            price (int): price of product

        Returns:
            bool: True if data is ok
        """
        name_len_min = 3
        name_len_max = 20
        price_min = 0
        price_max = 1000000000
        if len(name) < name_len_min or len(name) > name_len_max:
            return False
        if price < price_min or price > price_max:
            return False

        pattern = r'[0-9a-zA-Z ]*'
        if re.fullmatch(pattern, name) is None:
            return False

        return True

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
