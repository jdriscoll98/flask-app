import functools
import bcrypt
import random
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != password_confirm:
            error = 'Passwords must match'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
       

        if error is None:
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt(12))
            db.execute(
                'INSERT INTO user (username, password, balance) VALUES (?, ?, ?)',
                (username, hashed_password, random.randint(0, 1000))
            )
            db.commit()
            flash(u"Account Created Successfully!", "success")
            return redirect(url_for('auth.login'))

        flash(error, 'error')

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or password'
        elif not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard.index'))

        flash(error, 'error')

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
