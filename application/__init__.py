import os
from flask import Flask, url_for
from flask_bootstrap import Bootstrap4




def create_app(test_config=None):
    """ App factory."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev-4-hire',
    )


    if test_config is None:
        # Load the instance config if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if one is passed
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Initialize the db
    from . import db
    db.init_app(app)

    Bootstrap4(app)

    # Authorization blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    from . import index
    app.register_blueprint(index.bp)
    from . import admin
    app.register_blueprint(admin.bp)
    from . import ticket
    app.register_blueprint(ticket.bp)
    


    return app
        