from GymApp.flaskr.src.views.auth import login_required
from flask import Blueprint, render_template

bp = Blueprint('workout_view', __name__)


@bp.route('/workout', methods=('GET', 'POST'))
@login_required
def workout():
    """Render the Workout page.

    This route is responsible for rendering the Workout page template.

    Returns:
        The rendered Workout page template.
    """
    return render_template('workout/Workout.html')


@bp.route('/create_workout_plan', methods=('GET', 'POST'))
@login_required
def create_workout_plan():
    """Render the Create Workout Plan page.

    This route is responsible for rendering the Create Workout Plan page template.

    Returns:
        The rendered Create Workout Plan page template.
    """
    return render_template('workout/Workout_Plan.html')
