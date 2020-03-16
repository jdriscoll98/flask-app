import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from web.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/', methods=['GET'])
def index():
    return render_template('web/index.html')

