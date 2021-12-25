import json
import sys

from webapi.database import db
from webapi.models import Product


def load_data():
    file_path_list = ['tests/data/product.json']
    for file_path in file_path_list:
        rows = load_json_file(file_path)
        for row in rows:
            p = Product(**row)
            db.session.add(p)
        db.session.commit()


def load_json_file(file_path):
    with open(file_path, encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print('[Loading test data] {0}'.format(e), file=sys.stderr)
            sys.exit(1)

    return data
