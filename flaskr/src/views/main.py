from flask import (
    Blueprint, render_template
)

from GymApp.flaskr.src.views.auth import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('main/index.html')
