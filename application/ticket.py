
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from application.db import DBCM

bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@bp.route('/')
def get_tickets():
    return 'Coming Soon'