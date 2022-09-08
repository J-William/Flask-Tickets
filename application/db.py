from datetime import timedelta
import oracledb
import os
import click
from flask import g, session
from flask.cli import with_appcontext


class Dbcm(object):
    """ Singleton Database Connection Manager. """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Dbcm, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.pool = oracledb.create_pool( 
            user= os.environ.get('DATABASE_USER'),
            password= os.environ.get('DATABASE_PASSWORD'),
            dsn= os.environ.get('DATABASE_DSN'),
            min=1, 
            max=2, 
            increment=1
            )


    def get_conn(self):
        """ Return the active db connection create one if there isn't one active. """
        if 'db' not in g:
            g.db = self.pool.acquire()
        
        return g.db

    def close_conn(self, x = None):
        """ Close the db connection."""
        db = g.pop('db', None)

        if db is not None:
            try:
                self.pool.release(db)
            except NameError:
                pass

    def shutdown(self):
        """ Close the connection pool"""
        try:
            self.pool.close()
        except NameError:
            pass

    def row_factory(self, cursor):
        """ Setup the row factory for a cursor."""
        columns = [col[0] for col in cursor.description]
        cursor.rowfactory = lambda *args: dict(zip(columns, args))

    def get_result(self, query, params = None):
        """ Return a cursor with the results of a query already formatted with a row factory."""
        conn = self.get_conn()
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        self.row_factory(cur)
        return cur




# # Global instance of the DBCM
DBCM = Dbcm()   



########################### Initialization ####################################

def parse_script(filepath):
    """ Parse a sql script into a list of commands."""
    f = open(filepath)
    script = f.read()
    f.close()
    script = script.replace('\n', '')
    script = script.strip()
    return script.split(';')


def init_db():
    """ First time initialization of the db."""
    # Create the default admin
    from werkzeug.security import generate_password_hash
    # from application import DBCM
    conn = DBCM.get_conn()
    cur = conn.cursor()
    commands = parse_script('dm/schema.sql')

    for command in commands:
        if command:
            cur.execute(command)

    cur.execute(
        'INSERT INTO app_user ( username, password, role ) VALUES (:1, :2, :3)',
        [ 'admin', generate_password_hash('admin'), 'ADMIN' ]
    )

    conn.commit()
    cur.close()
    DBCM.close_conn()
    DBCM.shutdown()

def load_sample_data():
    """ Load some sample data for the applicaton."""
    conn = DBCM.get_conn()
    cur = conn.cursor()

    from werkzeug.security import generate_password_hash
    commands = parse_script('dm/sample.sql')
    
    for command in commands:
        if command:
            cur.execute(command)
    
    cur.close()
    conn.commit()
    DBCM.close_conn()
    DBCM.shutdown()
    
    

@click.command('init-db')           
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database.')

@click.command('load-sample-data')
@with_appcontext
def load_sample_data_command():
    """ Load sample data """
    load_sample_data()
    click.echo('Loaded sample data.')

def init_app(app):
    # Tells Flask to call this function when ending a response
    app.teardown_appcontext(DBCM.close_conn)
    # Adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_sample_data_command)

    @app.before_first_request    
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=10)