from .db import get_db
import functools
import os
import binascii

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from .auth import login_required

bp = Blueprint('insecure', __name__, url_prefix='/insecure')


@bp.route('/', methods=['GET'])
@login_required
def index():
    user_id = request.args.get('user_id')
    db = get_db()
    user = db.execute('SELECT * FROM user where id = %s' % user_id).fetchone()
    return render_template('web/insecure_dash.html', user=user)


@bp.route('/get_balance', methods=['POST'])
def get_balance():
    user_input = request.form.get('account_number')
    query_string = "SELECT * FROM user WHERE id = '%s' " % user_input # no sanitation on the input at all, vulnerable to ""' OR 1=1; --""
    db = get_db()
    cursor = db.execute(query_string)
    results = cursor.fetchall()
    return render_template('web/insecure_dash.html', results=results, user=g.user)


@bp.route('/send_money', methods=["POST", "GET"])
def send_money():
    db = get_db()
    if request.method == 'GET':
        print(request.args)
        recepient = request.args.get('recepient')
        sender = request.args.get('sender')
        amount = request.args.get('amount')
    else:    
        recepient = request.form.get('recepient')
        sender = request.form.get('sender')
        amount = request.form.get('amount')
    recepient_row = db.execute(f'SELECT * from user where id = {recepient}').fetchone()
    sender_row = db.execute(f'SELECT * from user where id = {sender}').fetchone()
    
    new_recepient_amount = recepient_row['balance'] + int(amount)
    new_sender_amount = sender_row['balance'] - int(amount) 

    db.execute(f'UPDATE user SET balance = {new_recepient_amount} WHERE id={recepient}')
    db.execute(f'UPDATE user SET balance = {new_sender_amount} WHERE id={sender}')
    db.commit()

    return redirect(url_for('insecure.index', user_id=g.user['id']))


@bp.route('/hackersite', methods=['GET'])
def hacker_site():
    return render_template('web/hackersite_insecure.html')

