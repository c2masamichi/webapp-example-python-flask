import re

from sqlalchemy.orm import validates

from webapi.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        min_length = 3
        max_length = 20
        pattern = r'[0-9a-zA-Z ]*'

        assert min_length <= len(name) <= max_length
        assert re.fullmatch(pattern, name) is not None
        return name

    @validates('price')
    def validate_price(self, key, price):
        min_num = 0
        max_num = 1000000000  # 10^9
        assert min_num <= price <= max_num
        return price
