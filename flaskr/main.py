import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .auth import login_required
from .db import get_db

bp = Blueprint('main', __name__)

from .auth import login_required

@bp.route('/')
@login_required
def index():
    return render_template('main/index.html')

def select_option():
    if request.form['action'] == "Workout":
        db = get_db()
        print("Workout selected");
        return redirect(url_for("main"))

    if request.form['action'] == "Create Workout":
        db = get_db()
        print("Create Workout Selected");
        return redirect(url_for("main"))

    if request.form['Delete Account'] == "Create Workout":
        db = get_db()
        print("Delete Account Selected");
        return redirect(url_for("main"))



