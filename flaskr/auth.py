import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    """
    Decorator function to require authentication for a view.
    If a user is logged in, proceed to the view function.
    If no user is logged in, redirect to the login page.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Register a new user.
    If the request method is POST, validate the form data, insert the user into the database,
    and redirect to the login page.
    If the request method is GET, render the registration form.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Log in the user.
    If the request method is POST, validate the form data, check the username and password,
    set the user ID in the session, and redirect to the index page.
    If the request method is GET, render the login form.
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
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


@bp.route('/delete_user', methods=('GET', 'POST'))
@login_required
def delete_user():
    """
    Delete the logged-in user.
    If the request method is POST, delete the user from the database.
    """
    db = get_db()
    flash('User will be deleted')
    db.execute(
        'DELETE FROM user WHERE username = ?', (g.user['username'],)
    )
    db.commit()

    return redirect(url_for('auth.logout'))


@bp.before_app_request
def load_logged_in_user():
    """
    Load the logged-in user based on the user ID stored in the session.
    If a user is logged in, store the user data in g.user for access during the request.
    If no user is logged in, set g.user to None.
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
    """
    Log out the user by clearing the session.
    """
    session.clear()
    g.user = None
    return redirect(url_for('index'))


def login_required(view):
    """
    Decorator function to require authentication for a view.
    If a user is logged in, proceed to the view function.
    If no user is logged in, redirect to the login page.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view