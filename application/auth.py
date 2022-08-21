import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from application.db import DBCM

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    """ Login """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

        query = 'SELECT * FROM app_user WHERE username = :1'
        params = [username]
        cursor = DBCM.get_result(query, params)
        error = None
        user = cursor.fetchone()
        cursor.close()

        # Validate login
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['PASSWORD'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['USER_ID']
            return redirect(url_for('index.index'))
        
        
        flash(error)

    return render_template('auth/login.html')



@bp.route('/logout')
def logout():
    """ Logout a user."""
    session.clear()
    return redirect(url_for('index.index'))

@bp.before_app_request
def load_logged_in_user():
    """ 
        Runs before the view function no matter what URL is requested. Checks to see if a user
        is logged in and loads their info if they are.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        query = 'SELECT * FROM app_user WHERE user_id = :1'
        params = [str(user_id)]
        cursor = DBCM.get_result(query, params)
        g.user = cursor.fetchone()
        cursor.close()


def login_required(view):
    """ Decorator that requires login for views that it wraps."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Login required.')
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    """ Decorator that requires admin users for views that it wraps."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['AUTH_LEVEL'] != 'ADMIN':
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view