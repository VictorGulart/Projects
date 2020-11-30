import os
from flask import Flask

''' This file has double duty: it contains the application factory and it tells python that the flaskr
dir should be treated as a package '''

def create_app(test_config=None):
    ''' Creating the app as a global will bring problems in the future for the project instead it 
    is created inside a function and returned. This function is known as application factory 
    
    details about this:

    instance_relative_config: tells the app that the configuration files are relative to the instance folder
        (main folder of the project), this folder is outside flaskr and can hold data that shouldn't be committed
        to version control, such as configuration secrets and the database file.
    app.config.from_mapping(): sets some default configuration that the app will use
        SECRET_KEY: used to keep data safe. used for hashing later must be randomized and not 'dev'
        DATABASE: it's where the db will be saved. it's under app.instance_path 
    app.config.from_pyfile(): overrides the default configuration with values taken from config.py in the main folder
        if it exists. for example, when deploying it can be used to randomize the SECRET_KEY.
        test_config: it will be used instead of the instance configuration, when provided. this helps to change 
            configurations for tests that will be written later on. they will be independent of any development values
    os.makedirs(): just makes sure that the main folder exist. not flaskdir but the project folder 
    @app.route(): just sets an example for testing


    to run the project
    some variables need to be set on the command line before running
    set FLASK_APP = 'folder where the app is the __init__.py)
    set FLASK_ENV = 'how to run the project in development mode or production'
    '''
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY = "dev", 
            DATABASE = os.path.join(app.instance_path, "flaskr.sqlite"), )

    if test_config is None:
        # load the instance, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed on
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple  page that says hello
    @app.route('/hello')
    def hello_world():
        return 'Hello world!'
    
    # creates the database and resister to the application
    from . import db
    db.init_app(app)

    # register the blueprint to the application
    from . import auth
    app.register_blueprint(auth.bp)

    # register the blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    """ 
    Unlike the auth blueprint, the blog blueprint does not have a url_prefix. So the index view
    will be at /, the create view at /create, and so on. The blog is the main feature of Flaskr,
    so it makes sense that the blog index will be the main index.
    However, the endpoint for the index view defined below will be blog.index. Some of the 
    authentication views referred to a plain index endpoint.
    app.add_url_rule(): associates the endpoint name 'index' with the / url so that url_for('index')
    or url_for('blog.index') will both work, generating the same / URL either way.
    In another application the blog blueprint might habe a url_prefix and a separate index view 
    would be defined in the app factory, similar to hello view. Then the index and blog.index 
    endpoints and URLs would be also different.
    """
    app.add_url_rule('/', endpoint='index')

    return app



