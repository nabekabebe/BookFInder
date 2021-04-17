import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy.orm import scoped_session, sessionmaker


def get_db():
    if 'db' not in g:
        engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
        conn = engine.connect()
        g.db = scoped_session(sessionmaker(bind=engine))
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db = get_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
