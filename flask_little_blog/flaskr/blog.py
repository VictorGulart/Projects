
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    """
    The index will show all of the posts, most recent first. A JOIN is used so that the author
    information from the user table is available in the result.
    """
    db = get_db()
    posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u on p.author_id = u.id'
            ' ORDER BY created DESC').fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """
        The create view works the same as the auth register view. Either the form is displayed, or
        the posted data is validated and the post is added to the database or an error is shown.

        @login_required: decorator written earlier is used on the blog views. A user must be logged
        in to visit these views, otherwise they will be redirected to the login page.
    """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO post (title, body, author_id)' 
                    'VALUES (?,?,?)',
                    (title, body, g.user['id']) )
            db.commit()
            return redirect( url_for('blog.index') )
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    """
        Both the update and delete views will need to fetch a post by id and check if the author 
            matches the logged in user. To avoid duplicating code, you can write a function 
            to get the post and call it from each view.
        abort(): will raise a special exception with the error, otherwise a default message is used.
            404 means "Not Found", and 403 means "Forbidden". (401 means "Unauthorized", but you 
            redirect to the login page instead of returning that status.)
        check_author: is defined so that the function can be used to get a post without checking 
            the author. This would be useful if there was a view to show an individual post on a 
            page, where the user doesn't matter because they're not modifying the post.
    """
    post = get_db().execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?',
            (id,) ).fetchone()

    if post is None:
        abort(404, 'Post id {0} does not exist.'.format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    """
        Unlike the other views, the update function takes an argument, id.
        That corresponds to the <int:id> in the route. A real URL will look like /1/update..
        Flask will capture the 1, ensure it's an int, and pass it as the id argument. If int is not
        specified, id will be a string instead. 
        To generate a URL to the update page, url_for() need to be passed the id so it knows what to 
        fill in: this is whats written on index.html - url_for('blog.update', id=post['id'])
    """
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'UPDATE post SET title = ?, body = ?'
                    ' WHERE id = ?',
                    (title, body, id) )
            db.commit()
            return redirect( url_for('blog.index') )

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,) )
    db.commit()
    return redirect( url_for('blog.index') )
