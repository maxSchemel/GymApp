import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('workout', __name__)

from .auth import login_required


@bp.route('/workout', methods=('GET', 'POST'))
@login_required
def workout():
    return render_template('workout/Workout.html')


@bp.route('/create_workout_plan', methods=('GET', 'POST'))
@login_required
def create_workout_plan():
    return render_template('workout/Workout_Plan.html')