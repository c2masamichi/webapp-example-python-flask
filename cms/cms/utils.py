import json
import sys

from flask import flash

from cms.database import db
from cms.models import Entry
from cms.models import User


def load_data():
    file_path = 'tests/data/user.json'
    rows = load_json_file(file_path)
    for row in rows:
        p = User(**row)
        db.session.add(p)
    db.session.commit()

    file_path = 'tests/data/entry.json'
    rows = load_json_file(file_path)
    for row in rows:
        p = Entry(**row)
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


def flash_error(message):
    flash(message, category='error')


def flash_success(message):
    flash(message, category='success')
