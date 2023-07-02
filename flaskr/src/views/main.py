from flask import Blueprint, render_template
from GymApp.flaskr.src.views.auth import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    """Render the index page.

    This route is responsible for rendering the index page template.

    Returns:
        The rendered index page template.
    """
    return render_template('main/index.html')
