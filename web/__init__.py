import os

from flask import Flask, url_for, redirect

from . import db, auth, dashboard, secure, insecure

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'web.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(401)
    def csrf_handle(e):
        return "CSRF token missing"
    
    @app.errorhandler(403)
    def permission_denied(e):
        return "You're not allowed to do that!"

    # a simple page that says hello
    @app.route('/')
    def hello():
        return redirect(url_for('dashboard.index'))
    
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(secure.bp)
    app.register_blueprint(insecure.bp)
    
    return app
