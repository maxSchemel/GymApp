import sqlite3
import click
from flask import current_app, g


def get_db():
    """
    Get a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection to the SQLite database.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Close the database connection.

    Args:
        e: The exception passed to the teardown function (default: None).
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initialize the database by executing the SQL statements in the schema file.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """
    Flask command to initialize the database by executing the 'init_db' function.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Initialize the Flask application with database-related functionality.

    Args:
        app: The Flask application instance.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
