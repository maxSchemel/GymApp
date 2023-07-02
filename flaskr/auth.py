import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .db import get_db
from .user import User
from .repository import SQLiteRepository, UserAlreadyExistsError, IncorrectUsernameError, IncorrectPasswordError

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

        new_user = User(username, password)
        repo = SQLiteRepository(db)

        if error is None:
            try:
                repo.register_user(new_user)
                repo.connection.commit()
            except UserAlreadyExistsError:
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
        repo = SQLiteRepository(db)

        error = None
        user = User(username, password)
        try:
            repo.login_user(user)
        except IncorrectUsernameError:
            error = 'Incorrect username.'
        except IncorrectPasswordError:
            error = 'Incorrect password.'
        else:
            session.clear()
            session['user_id'] = user.id
            g.user = user
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
    repo = SQLiteRepository(get_db())
    repo.delete_user(g.user)
    repo.commit()

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
        repo = SQLiteRepository(get_db())
        g.user = repo.get_user(user_id)


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