
from .auth import login_required
from flask import (
    Blueprint, render_template
)

bp = Blueprint('workout', __name__)


@bp.route('/workout', methods=('GET', 'POST'))
@login_required
def workout():
    return render_template('workout/Workout.html')


@bp.route('/create_workout_plan', methods=('GET', 'POST'))
@login_required
def create_workout_plan():
    return render_template('workout/Workout_Plan.html')