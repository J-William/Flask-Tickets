from application.auth import admin_required
from application.db import DBCM
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/users')
def users():
    """ Table of users with button to open form for individual."""
    users = DBCM.get_result(
        'SELECT user_id, username, role FROM app_user ORDER BY user_id'
    ).fetchall()
    
    return render_template('admin/users.html', users=users)


@bp.route('/user/<int:user_id>', methods=('GET', 'POST'))
@admin_required
def edit_user(user_id):
    """ The form to view/edit a given user."""    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        conn = DBCM.get_conn()
        cur = conn.cursor()
        cur.execute(
            'UPDATE app_user SET username = :1, password = :2, role = :3 WHERE user_id = :4',
            [ username, generate_password_hash(password), role, user_id]
        )
        conn.commit()
        cur.close()
        return redirect(url_for('admin.users'))
    
    user = DBCM.get_result(
        'SELECT * FROM app_user WHERE user_id = :1',
        [str(user_id)]
    ).fetchone()

    return render_template('admin/view_user.html', user=user)

@bp.route('/user/create', methods=('GET', 'POST'))
@admin_required
def create_user():
    """ Form to create a new user."""
    if request.method == 'POST':
        user = {}
        user['USERNAME'] = request.form['username']
        user['PASSWORD'] = request.form['password']
        user['ROLE'] = request.form['role']

        conn = DBCM.get_conn()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO app_user (username, password, role) VALUES (:1, :2, :3)',
            [user['USERNAME'], generate_password_hash(user['PASSWORD']), user['ROLE']]
        )
        conn.commit()
        cur.close()
        # return render_template('admin/user.html', user=user)
        return redirect(url_for('admin.users'))
    
    return render_template('admin/create_user.html')


