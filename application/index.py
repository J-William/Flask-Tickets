from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from application.auth import login_required

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('ticket.submit_ticket'))