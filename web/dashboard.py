import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from web.auth import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('web/index.html')

