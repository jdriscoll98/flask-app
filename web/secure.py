import functools
import os
import binascii

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from .auth import login_required

bp = Blueprint('secure', __name__, url_prefix='/secure')

from .db import get_db

@bp.route('/', methods=['GET'])
@login_required
def index():
    # Set up tokens for csrf protection
    acct_token = binascii.hexlify(os.urandom(20)).decode()
    session['account_token'] = acct_token
    send_token = binascii.hexlify(os.urandom(20)).decode()
    session['send_token'] = send_token
    return render_template('web/secure_dash.html', acct_token=acct_token, send_token=send_token)

@bp.route('/get_balance', methods=['POST'])
def get_balance():
    user_token = request.form.get('acct_token', None) # Server side csrf prevention using tokens generated on "GET" request
    if user_token != session['account_token']:
        return abort(401)
    
    real_account_number = g.user['id']
    submitted_account_number = int(request.form.get('account_number')) # prevent any sql injection by never touching the database !
    print(real_account_number)
    print(submitted_account_number)
    if real_account_number != submitted_account_number:
        flash("You can't look up someone else's stuff!", 'balance')
        return redirect(url_for('secure.index'))
    
    acct_token = binascii.hexlify(os.urandom(20)).decode()
    session['account_token'] = acct_token
    send_token = binascii.hexlify(os.urandom(20)).decode()
    session['send_token'] = send_token
    results = [g.user]
    return render_template('web/secure_dash.html', results=results, acct_token=acct_token, send_token=send_token)

@bp.route('/send_money', methods=["POST"])
def send_money():
    user_token = request.form.get('send_token')
    if user_token != session['send_token']:
        abort(401)

    to = request.form.get('to_account') # prevent idor by only allowing the money to come from users account
    amount = float(request.form.get('amount'))

    if amount < 0:
        flash('Ammount must be a positive number', 'send')
        redirect(url_for('secure.index'))
    if amount > g.user['balance']:
        flash('You do not have that much to send!', 'send')
        return redirect(url_for('secure.index'))
    db = get_db()


    new_user_balance = g.user['balance'] - amount
    user_id = g.user['id']
    db.execute(f'UPDATE user SET balance = {new_user_balance} where id = {user_id}')
    to_account = db.execute(f'SELECT balance FROM user WHERE id = {to}').fetchone() # format strings directly in to f-strings to escape strings
    new_balance = to_account['balance'] + amount
    db.execute(f'UPDATE user SET balance = {new_balance} WHERE id = {to}')
    db.commit()
    flash('Money sent successfully!', 'send')

    return redirect(url_for('secure.index'))

@bp.route('/hackersite', methods=['GET'])
def hacker_site():
    return render_template('web/hackersite_secure.html')



