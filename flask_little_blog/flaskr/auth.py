import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

""" A view function is the code written to respond to requests to the application. 
    Flask uses patterns to match the incoming request URL to the view that should handle it. 
    The view (the function) returns data that Flask turns into an outgoing response. Flask 
    can also go othe other direction and generate a URL to a view based on its name and
    arguments.
    
    A blueprint is a way to organize a group of related views and other code. Rather than 
    registering views and other code directlu with an application, they, they are registered
    with a blueprint. Then the blueprint is registered with the app when it is available
    in the factory function.

    This app called flaskr has 2 blueprints, one for authentication and another for 
    posts. The code for each blueprint will be in a separate module.
    
    Like the application it needs to know where it is defined so __name__ is passed
    as the second argument.
    The url_prefix will be prepended to all URLs associated with the blueprint
    
    Now this need to be registered with the application on the factory function just 
    before returning the app
    
    This blueprint will have view to register, log in and log out.
"""


bp = Blueprint('auth', __name__, url_prefix='/auth')
# Up to here a Blueprint called "auth" is created


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """ 
        @bp.route: associates the URL /register with the register view function. When flask
            recieves a request to /auth/register, it will call the register view and use the
            return value as the response
        If the user submitted the form, request.method will be 'POST'. In this case, start 
            validating the input.
        request.form: is a special type of dict mapping submitted form keys and values. The
            user input their username and password.
        validate that username and password are not empty
        validate that the username is not already registered by querying the database and 
            checking if a result is returned.
        if validations succeds, the values are inserted in the database. the password is 
            hashed.
        after the values are recorded it redirects to the login page.
        url_for: in this case generates the URL for the login view based on its name.
            this is preferable to writing the URL directly as it allows the developer 
            to change the URL later without changing all code links to it.
        redirect(): generates a redirect response to the generated URL
        if the validation fails than an error is shown. 
            flash stores messages that can be retrieved when rendering the template.
        when the user initially navigates to auth/register, or there was a validation error,
            an HTML page with the registration form shoulf be shown.
            render_template():  will render a template containing the HTML.
"""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
                ).fetchone() is not None:
            error = 'User {} is already registered'.format(username)

        if error is None:
            db.execute(
                    'INSERT INTO user (username, password) VALUES (?,?)', 
                    (username, generate_password_hash(password) ) )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    """
    It is a little different from register!
    The user is queried first and stored in a var for later use.
    check_password_hash(): hashes the submitted password in the same way 
        as the stored hash and securely compares them. if matched than
        is valid.
    session: is a dict that stores data across requests. when validation 
        succeds than the user id is stored in a new session. The data is 
        stored in a coockie that is sent to the browser, and the the 
        browser sends back with further requests. Flask securely signs the 
        data so that it can't be tampered with.

    Now the user is stored in session it will be available for future 
        requests. At the beginning of each request, if the user is logged in
        their information should be loaded and made available to other views.

"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
                ).fetchone()
        if user is None:
            error = 'Incorrect. Try again'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect. Try again'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')



@bp.before_app_request
def load_logged_in_user():
    """
    bp.before_app_request: registers a function that runs before the view function,
        no matter what URL is requested. 
    load_logged_in_user checks if a user id is stored in session and gets that 
        user's data from the db, storing it on g.user, which lasts for the length of
        the request. If there is no user id, or if the id does not exist, g.user 
        will be None.
    """
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)
                ).fetchone()


@bp.route('/logout')
def logout():
    # clears the session and redirects to the index page  
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """ 
    Creating, editing and deleting blogs posts will require a user to be logged
         in. A decoreator can be used to check this for each view it's applied to.
    This decorator returns a new view function that wraps the original view
    it's applied to. The new function checks if a user is loaded and redirects 
    to the login page otherwise.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
