from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from application.auth import login_required

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    flash('Welcome!')
    return render_template('base.html')