import re

from sqlalchemy.orm import validates

from webapi.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @validates('name')
    def validate_name(self, key, product):
        min_length = 3
        max_length = 20
        pattern = r'[0-9a-zA-Z ]*'

        assert min_length <= len(product) <= max_length
        assert re.fullmatch(pattern, product) is not None
        return product

    @validates('price')
    def validate_price(self, key, product):
        min_num = 0
        max_num = 1000000000
        assert min_num <= product <= max_num
        return product
