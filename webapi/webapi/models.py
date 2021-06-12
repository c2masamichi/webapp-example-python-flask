import re

from sqlalchemy.orm import validates

from webapi.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @validates('name')
    def validate_name(self, key, product):
        name_len_min = 3
        name_len_max = 20
        pattern = r'[0-9a-zA-Z ]*'

        assert name_len_min <= len(product) <= name_len_max
        assert re.fullmatch(pattern, product) is not None
        return product

    @validates('price')
    def validate_price(self, key, product):
        price_min = 0
        price_max = 1000000000
        assert price_min <= product <= price_max
        return product
