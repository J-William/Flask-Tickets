import oracledb

import click
from flask import g
from flask.cli import with_appcontext


class Dbcm(object):
    """ Database Connection Manager. """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Dbcm, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.pool = oracledb.create_pool( 
            user="DEV1", 
            password='123', 
            dsn="localhost:1521/XEPDB1", 
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

    def get_result(self, query, params):
        """ Return a cursor with the results of a query already formatted with a row factory."""
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(query, params)
        self.row_factory(cur)
        return cur

    def row_factory(self, cursor):
        """ Setup the row factory for a cursor."""
        columns = [col[0] for col in cursor.description]
        cursor.rowfactory = lambda *args: dict(zip(columns, args))


# Global instance of the DBCM
DBCM = Dbcm()


##### Initialization
def init_db():
    """ First time initialization of the db."""
    db = DBCM.get_conn()
    cur = db.cursor()
    
    # Create the default admin
    from werkzeug.security import generate_password_hash

    cur.execute(
        "INSERT INTO app_user ( user_id, username, password, auth_level) VALUES (:1, :2, :3, :4)",
        [1, 'admin', generate_password_hash('admin') , 'ADMIN']
        )
    
    db.commit()
    cur.close()
    DBCM.close_conn()
    DBCM.shutdown()


@click.command('init-db')           
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # Tells Flask to call this function when ending a response
    app.teardown_appcontext(DBCM.close_conn)
    # Adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)


