from application.db import DBCM
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users')
def users():
    """ TODO Table of users with button to open form for individual."""
    
    users = DBCM.get_result(
        'SELECT user_id, username, auth_level FROM app_user ORDER BY user_id'
    ).fetchall()
    
    return render_template('admin/users.html', users=users)


@bp.route('/user/<int:user_id>', methods=('GET', 'POST'))
def get_user(user_id):
    """ TODO Get the form to view/edit a given user."""
    if request.method == 'POST':
        user = {}
        user['USER_ID'] = request.form['user_id']
        user['USERNAME'] = request.form['username']
        user['PASSWORD'] = request.form['password']
        user['AUTH_LEVEL'] = request.form['auth_level']

        conn = DBCM.get_conn()
        cur = conn.cursor()
        cur.execute(
            'UPDATE app_user SET username = :1, password = :2, auth_level = :3 WHERE user_id = :4',
            [user['USERNAME'], generate_password_hash(user['PASSWORD']), user['AUTH_LEVEL'], user['USER_ID']]
        )
        conn.commit()
        cur.close()
        # return render_template('admin/user.html', user=user)
        return redirect(url_for('admin.users'))
    
    user = DBCM.get_result(
        'SELECT * FROM app_user WHERE user_id = :1',
        [str(user_id)]
    ).fetchone()

    return render_template('admin/user.html', user=user)

@bp.route('/user/create')
def create_user():
    """ TODO Form to create a new user."""
    conn = DBCM.get_conn()
    cur = conn.cursor()
    cur.execute(
        'SELECT (max(user_id) + 1) as next_id FROM app_user'
    )
    DBCM.row_factory(cur)
    result = cur.fetchone()
    next_id = result['NEXT_ID']
    cur.close()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO app_user ( user_id ) VALUES (:1)',
        [next_id]
    )
    conn.commit()
    cur.close()
    return redirect(url_for('admin.get_user', user_id=next_id))

    


