import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    editor = models.User(name='editor', role='editor')
    editor.set_password('editor')
    dbsession.add(editor)

    banner1 = models.Banner(
        title_name='Sample1',
        position=1,
        status=1,
        url_link='/static/banners',
        image='sample.png',
        creator=editor
        )
    banner1.set_datetime()
    dbsession.add(banner1)

    banner2 = models.Banner(
        title_name='Sample2',
        position=2,
        status=1,
        url_link='/static/banners',
        image='sample2.png',
        creator=editor
        )
    banner2.set_datetime()
    dbsession.add(banner2)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
