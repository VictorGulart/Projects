import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

''' Connects to the db using sqlite3
    sqlite3 is nice for smaller projects because it's not needed to setup it is ready to go
        and is built in to python. However, if concurrent requests try to write to the db
        at the same time, they will slow down as each write happens sequentially. small apps
        won't notice this. Once it becomes bigger, it might be needed to switch to a different
        database.
    g: is a special object that is unique to each request. It is used to store data that might be
        accessed by multiple functions during the request. The connection is stored and reused 
        instead of creating a new connection if get_db is called a second time in the same request
    current_app: is another special object that points to the Flask app handling the request. Since
        application factory was used, there is no application object when writting the rest of 
        the code. get_db will be called when the application has been created and is handling a 
        request, so current_app can be used.
    sqlite3.connect(): just establishes a connection to the file pointed by the DATABASE configuration key.
    sqlite3.Row: tells the connection to return rows that behave like dicts. '''

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """ Just runs the schema.sql script that clears all the data and creates the tables again
        open_resource(): opens a file relative to the flaskr package, which is useful since it 
            doen't know where the location is when deploying the app later. get_db() will return
            the db connection, which is used to execute the command read from the file.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables.
    click.command(): defines a command line command called init-db that calls the init-db function
        and shows a success message to the user. There is more to Command Line Interface on flask website
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """ close_db and init_db_command function need to be registered with the application instance;
        otherwise, they won't be used by the app. However, since a application factory is being
        used, that instance isn't available when writing the functions. Instead, write a function
        that takes an app and does the registration. 
        app.teardown_appcontext(): tells flask to call the function when cleaning up after 
            returning the response
        app.cli.add_command(): adds a new command that can be called with the flask command.
        import and call this funtion from the factory. must be placed at the end of the function
        before returning the app.

        After adding to the factory function it the database file must be initialized
        to do it run:
            flask init-db
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
